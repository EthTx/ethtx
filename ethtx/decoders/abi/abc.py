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

from abc import ABC, abstractmethod
from typing import Optional, Any, List, Dict

from ethtx.models.decoded_model import DecodedCall, DecodedTransfer, Proxy
from ethtx.models.objects_model import (
    Block,
    Transaction,
    Call,
    Event,
    TransactionMetadata,
    BlockMetadata,
)
from ethtx.providers.semantic_providers import SemanticsRepository


class ABIBasic:
    def __init__(self, repository: SemanticsRepository, chain_id: str):
        self._default_chain = chain_id
        self._repository: SemanticsRepository = repository


class ABISubmoduleAbc(ABC, ABIBasic):
    @abstractmethod
    def decode(self, *args, **kwargs) -> Any:
        ...


class IABIDecoder(ABC, ABIBasic):
    def __init__(
        self,
        repository: SemanticsRepository,
        chain_id: str,
        strict: Optional[bool] = False,
    ):
        super().__init__(repository, chain_id)
        self.strict = strict

    @abstractmethod
    def decode_transaction(
        self, block: Block, transaction: Transaction, proxies: Dict[str, Proxy]
    ):
        ...

    @abstractmethod
    def decode_calls(
        self,
        call: Call,
        block: BlockMetadata,
        transaction: TransactionMetadata,
        proxies: Dict[str, Proxy],
    ) -> ABISubmoduleAbc.decode:
        ...

    @abstractmethod
    def decode_events(
        self,
        events: [Event],
        block: BlockMetadata,
        transaction: TransactionMetadata,
        proxies: Dict[str, Proxy],
    ) -> ABISubmoduleAbc.decode:
        ...

    @abstractmethod
    def decode_transfers(
        self, call: DecodedCall, events: [Event], proxies: Dict[str, Proxy]
    ) -> ABISubmoduleAbc.decode:
        ...

    @abstractmethod
    def decode_balances(
        self, transfers: List[DecodedTransfer]
    ) -> ABISubmoduleAbc.decode:
        ...
