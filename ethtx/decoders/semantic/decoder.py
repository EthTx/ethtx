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

from typing import Dict, List, Optional

from ethtx.decoders.semantic.abc import ISemanticDecoder
from ethtx.decoders.semantic.balances import SemanticBalancesDecoder
from ethtx.decoders.semantic.calls import SemanticCallsDecoder
from ethtx.decoders.semantic.events import SemanticEventsDecoder
from ethtx.decoders.semantic.metadata import SemanticMetadataDecoder
from ethtx.decoders.semantic.transfers import SemanticTransfersDecoder
from ethtx.models.decoded_model import (
    DecodedTransactionMetadata,
    DecodedTransaction,
    DecodedEvent,
    DecodedTransfer,
    DecodedBalance,
    DecodedCall,
    Proxy,
)
from ethtx.models.objects_model import BlockMetadata


class SemanticDecoder(ISemanticDecoder):
    def decode_transaction(
        self,
        block: BlockMetadata,
        transaction: DecodedTransaction,
        proxies: Dict[str, Proxy],
        chain_id: str,
    ) -> DecodedTransaction:
        transaction.metadata = self.decode_metadata(
            block, transaction.metadata, chain_id
        )
        transaction.events = self.decode_events(
            transaction.events, transaction.metadata, proxies
        )
        transaction.calls = self.decode_calls(
            transaction.calls, transaction.metadata, proxies
        )
        transaction.transfers = self.decode_transfers(
            transaction.transfers, transaction.metadata
        )
        transaction.balances = self.decode_balances(
            transaction.balances, transaction.metadata
        )

        return transaction

    def decode_metadata(
        self,
        block_metadata: BlockMetadata,
        tx_metadata: DecodedTransactionMetadata,
        chain_id: str,
    ) -> DecodedTransactionMetadata:
        return SemanticMetadataDecoder(repository=self.repository).decode(
            block_metadata=block_metadata, tx_metadata=tx_metadata, chain_id=chain_id
        )

    def decode_event(
        self,
        event: DecodedEvent,
        tx_metadata: DecodedTransactionMetadata,
        proxies: Optional[Dict[str, Proxy]] = None,
    ) -> DecodedEvent:
        return SemanticEventsDecoder(repository=self.repository).decode(
            events=event, tx_metadata=tx_metadata, proxies=proxies or {}
        )

    def decode_events(
        self,
        events: List[DecodedEvent],
        tx_metadata: DecodedTransactionMetadata,
        proxies: Optional[Dict[str, Proxy]] = None,
    ) -> List[DecodedEvent]:
        return SemanticEventsDecoder(repository=self.repository).decode(
            events=events, tx_metadata=tx_metadata, proxies=proxies or {}
        )

    def decode_calls(
        self,
        call: DecodedCall,
        tx_metadata: DecodedTransactionMetadata,
        proxies: Optional[Dict[str, Proxy]] = None,
    ) -> DecodedCall:
        return SemanticCallsDecoder(repository=self.repository).decode(
            call=call, tx_metadata=tx_metadata, proxies=proxies or {}
        )

    def decode_call(
        self,
        call: DecodedCall,
        tx_metadata: DecodedTransactionMetadata,
        proxies: Optional[Dict[str, Proxy]] = None,
    ) -> DecodedCall:
        return SemanticCallsDecoder(repository=self.repository).decode(
            call=call, tx_metadata=tx_metadata, proxies=proxies or {}
        )

    def decode_transfers(
        self, transfers: List[DecodedTransfer], tx_metadata: DecodedTransactionMetadata
    ) -> List[DecodedTransfer]:
        return SemanticTransfersDecoder(repository=self.repository).decode(
            transfers=transfers, tx_metadata=tx_metadata
        )

    def decode_balances(
        self, balances: List[DecodedBalance], tx_metadata: DecodedTransactionMetadata
    ) -> List[DecodedBalance]:
        return SemanticBalancesDecoder(repository=self.repository).decode(
            balances=balances, tx_metadata=tx_metadata
        )
