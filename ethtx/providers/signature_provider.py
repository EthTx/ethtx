#  Copyright 2021 DAI Foundation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from abc import ABC, abstractmethod
from typing import Dict, List, Any

import requests


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

    def get_function(self, signature: str) -> Dict[str, List[str]]:
        if signature == "0x":
            raise ValueError(f"Signature can not be: {signature}")

        data = self._get_all(
            endpoint=self.FUNCTION_ENDPOINT, filters={"hex_signature": signature}
        )

        return self._parse_text_signature_response(data)

    def get_event(self, signature: str) -> Dict[str, List[str]]:
        if signature == "0x":
            raise ValueError(f"Signature can not be: {signature}")

        data = self._get_all(
            endpoint=self.EVENT_ENDPOINT, filters={"hex_signature": signature}
        )

        return self._parse_text_signature_response(data)

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

        return requests.get(self.url(endpoint), params=filters).json()

    @staticmethod
    def _parse_text_signature_response(response: List) -> Dict[str, List[str]]:
        text_sig = response[0].get("text_signature", "") if response else ""
        if text_sig:
            func_name = text_sig.split("(")[0]
            types = text_sig[text_sig.find("(") + 1 : text_sig.rfind(")")]
            if "(" in types:
                types = types[types.find("(") + 1 : types.rfind(")")]

            return {func_name: types.split(",")}

        return {}
