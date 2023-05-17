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

    def delete_semantics_by_address(self, chain_id: str, address: str) -> None:
        ...
