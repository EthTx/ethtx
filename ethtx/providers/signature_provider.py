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


class SignatureProvider(ABC):
    @abstractmethod
    def list_function_signatures(self, filters: Dict):
        ...

    @abstractmethod
    def list_event_signatures(self, filters: Dict):
        ...

    @abstractmethod
    def get_text_function_signatures(self, hex_signature: str):
        ...

    @abstractmethod
    def get_text_event_signatures(self, hex_signature: str):
        ...


class FourBytesDirectoryProvider(SignatureProvider):
    def list_function_signatures(self, filters: Dict):
        pass

    def list_event_signatures(self, filters: Dict):
        pass

    def get_text_function_signatures(self, hex_signature: str):
        pass

    def get_text_event_signatures(self, hex_signature: str):
        pass
