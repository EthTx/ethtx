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
from typing import Dict, Optional

from .contracts import EtherscanContract


class EtherscanProvider:
    api_key: str
    endpoints: Dict[str, str]
    default_chain: Optional[str]

    def __init__(
        self,
        api_key: str,
        nodes: Dict[str, str],
        default_chain_id: Optional[str] = None,
    ):
        self.api_key = api_key
        self.endpoints = nodes
        self.default_chain = default_chain_id

        self._contract = EtherscanContract(
            api_key=self.api_key,
            nodes=self.endpoints,
            default_chain_id=self.default_chain,
        )

    @property
    def contract(self) -> EtherscanContract:
        return self._contract
