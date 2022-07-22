# Copyright 2021 DAI FOUNDATION (the original version https://github.com/daifoundation/ethtx_ce)
# Copyright 2021-2022 Token Flow Insights SA (modifications to the original software as recorded
# in the changelog https://github.com/EthTx/ethtx/blob/master/CHANGELOG.md)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.
#
# The product contains trademarks and other branding elements of Token Flow Insights SA which are
# not licensed under the Apache 2.0 license. When using or reproducing the code, please remove
# the trademark and/or other branding elements.

import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Iterator, TypedDict, Union, Tuple, Optional

import requests
import requests_cache

log = logging.getLogger(__name__)


class SignatureReturnType(TypedDict):
    name: str
    args: Union[List[str], Tuple[str]]


class SignatureProvider(ABC):
    @abstractmethod
    def list_function_signatures(self, filters: Dict):
        ...

    @abstractmethod
    def list_event_signatures(self, filters: Dict):
        ...

    @abstractmethod
    def get_function(self, signature: str):
        ...

    @abstractmethod
    def get_event(self, signature: str):
        ...


class FourByteProvider(SignatureProvider):
    API_URL: str = "https://www.4byte.directory/api/v1"
    FUNCTION_ENDPOINT: str = "signatures"
    EVENT_ENDPOINT: str = "event-signatures"

    def list_function_signatures(self, filters: Dict = None) -> List[Dict]:
        return self._get_all(endpoint=self.FUNCTION_ENDPOINT, filters=filters)

    def list_event_signatures(self, filters: Dict = None) -> List[Dict]:
        return self._get_all(endpoint=self.EVENT_ENDPOINT, filters=filters)

    def get_function(self, signature: str) -> Iterator[Optional[SignatureReturnType]]:
        if signature == "0x":
            raise ValueError(f"Signature can not be: {signature}")

        with requests_cache.enabled("4byte_function_cache", expire_after=120):
            data = self._get_all(
                endpoint=self.FUNCTION_ENDPOINT, filters={"hex_signature": signature}
            )

        for function in reversed(data):
            if parsed := self._parse_text_signature_response(function):
                yield parsed

    def get_event(self, signature: str) -> Iterator[Optional[SignatureReturnType]]:
        if signature == "0x":
            raise ValueError(f"Signature can not be: {signature}")

        with requests_cache.enabled("4byte_event_cache", expire_after=120):
            data = self._get_all(
                endpoint=self.EVENT_ENDPOINT, filters={"hex_signature": signature}
            )

        for event in reversed(data):
            if parsed := self._parse_text_signature_response(event):
                yield parsed

    def url(self, endpoint: str) -> str:
        return f"{self.API_URL}/{endpoint}/"

    def _get_all(self, endpoint: str, filters: Dict = None) -> List[Dict]:
        page = 1
        results = []

        while True:
            res = self._get(endpoint, page, filters)
            next_url = res.get("next")
            results.extend(res.get("results", []))

            if not next_url:
                break
            page += 1

        return results

    def _get(
        self, endpoint: str, page: int = 0, filters: Dict = None
    ) -> Dict[str, Any]:
        if filters is None:
            filters = {}

        if page:
            filters["page"] = page

        try:
            response = requests.get(self.url(endpoint), params=filters, timeout=3)
            return response.json()

        except requests.exceptions.RequestException as e:
            log.warning("Could not get data from 4byte.directory: %s", e)
            return {}

        except Exception as e:
            log.warning("Unexpected error from 4byte.directory: %s", e)
            return {}

    def _parse_text_signature_response(
        self, data: Dict
    ) -> Optional[SignatureReturnType]:
        text_sig = data.get("text_signature", "")

        name = text_sig.split("(")[0] if text_sig else ""

        types = (
            text_sig[text_sig.find("(") + 1 : text_sig.rfind(")")] if text_sig else ""
        )

        if not name and not types:
            return None

        if "(" in types:
            args = tuple(types[types.find("(") + 1 : types.rfind(")")].split(","))
            if any("(" in arg for arg in args):
                log.warning(
                    "Could not parse %s signature: %s",
                    data.get("hex_signature"),
                    data.get("text_signature"),
                )
                return None
        else:
            args = list(filter(None, types.split(",")))

        return {"name": name, "args": args}


FourByteProvider = FourByteProvider()
