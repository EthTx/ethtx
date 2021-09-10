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
from typing import Dict

import requests


class SignatureProvider(ABC):
    @abstractmethod
    def list_function_signatures(self, filters: Dict, **kwargs):
        ...

    @abstractmethod
    def list_event_signatures(self, filters: Dict, **kwargs):
        ...

    @abstractmethod
    def get_text_function_signatures(self, hex_signature: str):
        ...

    @abstractmethod
    def get_text_event_signatures(self, hex_signature: str):
        ...


class FourBytesDirectoryProvider(SignatureProvider):
    API_URL: str = "https://www.4byte.directory/api/v1"

    def list_function_signatures(
        self, endpoint: str = "signatures", filters: Dict = None
    ):
        return self._get_all(endpoint=endpoint, filters=filters)

    def list_event_signatures(
        self, endpoint: str = "event-signatures", filters: Dict = None
    ):
        return self._get_all(endpoint=endpoint, filters=filters)

    def get_text_function_signatures(self, hex_signature: str):
        pass

    def get_text_event_signatures(self, hex_signature: str):
        pass

    def url(self, endpoint: str):
        return "{url}/{endpoint}/".format(url=self.API_URL, endpoint=endpoint)

    def _get_all(self, endpoint: str, filters: Dict = None):
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

    def _get(self, endpoint: str, page: int = 0, filters: Dict = None):
        if filters is None:
            filters = {}
        filters["page"] = page

        return requests.get(self.url(endpoint), params=filters).json()


if __name__ == "__main__":
    t = FourBytesDirectoryProvider()
    print(t.list_function_signatures())
