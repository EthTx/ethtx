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
from typing import Any, List, Dict

from ethtx.models.decoded_model import (
    DecodedTransaction,
    DecodedCall,
    DecodedEvent,
    DecodedTransfer,
    DecodedBalance,
)
from ethtx.models.objects_model import BlockMetadata, TransactionMetadata
from ethtx.providers.semantic_providers.semantics_repository import SemanticsRepository


class SemanticSubmoduleAbc(ABC):
    def __init__(self, repository: SemanticsRepository):
        self.repository = repository

    @abstractmethod
    def decode(self, *args, **kwargs) -> Any:
        ...


class ISemanticDecoder(ABC):
    def __init__(self, repository: SemanticsRepository, chain_id: str):
        self.repository = repository
        self._default_chain = chain_id

    @abstractmethod
    def decode_transaction(
        self,
        block: BlockMetadata,
        transaction: DecodedTransaction,
        token_proxies: Dict[str, Dict],
        chain_id: str,
    ) -> DecodedTransaction:
        ...

    @abstractmethod
    def decode_metadata(
        self,
        block_metadata: BlockMetadata,
        tx_metadata: TransactionMetadata,
        chain_id: str
    ):
        ...

    @abstractmethod
    def decode_calls(
        self,
        call: DecodedCall,
        tx_metadata: TransactionMetadata,
        token_proxies: Dict[str, Dict],
    ) -> SemanticSubmoduleAbc.decode:
        ...

    @abstractmethod
    def decode_events(
        self,
        events: List[DecodedEvent],
        tx_metadata: TransactionMetadata,
        token_proxies: Dict[str, Dict],
    ) -> SemanticSubmoduleAbc.decode:
        ...

    @abstractmethod
    def decode_transfers(
        self, transfers: List[DecodedTransfer], tx_metadata: TransactionMetadata
    ) -> SemanticSubmoduleAbc.decode:
        ...

    @abstractmethod
    def decode_balances(
        self, balances: List[DecodedBalance], tx_metadata: TransactionMetadata
    ) -> SemanticSubmoduleAbc.decode:
        ...
