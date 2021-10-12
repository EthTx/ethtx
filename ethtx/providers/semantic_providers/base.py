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

from abc import ABC
from typing import Dict, Optional, Any, List


class ISemanticsDatabase(ABC):
    """Semantics Database. Represents raw interface required to be
    implemented by a database that provides persistent
    data about semantics"""

    def get_address_semantics(self, chain_id: str, address: str) -> Optional[Dict]:
        ...

    def get_contract_semantics(self, code_hash: str) -> Optional[Dict]:
        ...

    def get_signature_semantics(self, signature_hash: str) -> Optional[List[Dict]]:
        ...

    def insert_contract(self, contract: dict, update_if_exist: bool = False) -> Any:
        ...

    def insert_address(self, address: dict, update_if_exist: bool = False) -> Any:
        ...

    def insert_signature(self, signature, update_if_exist: bool = False) -> Any:
        ...
