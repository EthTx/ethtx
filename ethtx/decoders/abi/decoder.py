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
from typing import Optional, Dict, List

from ethtx.models.decoded_model import (
    DecodedTransaction,
    DecodedCall,
    DecodedEvent,
    DecodedTransfer,
    Proxy,
)
from ethtx.models.objects_model import (
    Block,
    BlockMetadata,
    Transaction,
    TransactionMetadata,
    Call,
    Event,
)
from ethtx.utils.measurable import ExecutionTimer
from .abc import IABIDecoder
from .balances import ABIBalancesDecoder
from .calls import ABICallsDecoder
from .events import ABIEventsDecoder
from .transfers import ABITransfersDecoder

log = logging.getLogger(__name__)


def prune_delegates(call: DecodedCall) -> DecodedCall:
    while len(call.subcalls) == 1 and call.subcalls[0].call_type == "delegatecall":
        _value = call.value
        call = call.subcalls[0]
        call.value = _value

    for i, sub_call in enumerate(call.subcalls):
        call.subcalls[i] = prune_delegates(sub_call)

    return call


class ABIDecoder(IABIDecoder):
    def decode_transaction(
        self,
        block: Block,
        transaction: Transaction,
        chain_id: str,
        proxies: Optional[Dict[str, Proxy]] = None,
    ) -> Optional[DecodedTransaction]:

        with ExecutionTimer(f"ABI decoding for " + transaction.metadata.tx_hash):
            log.info(
                "ABI decoding for %s / %s.", transaction.metadata.tx_hash, chain_id
            )
            full_decoded_transaction = self._decode_transaction(
                block.metadata, transaction, chain_id, proxies
            )

        return full_decoded_transaction

    def decode_calls(
        self,
        root_call: Call,
        block: BlockMetadata,
        transaction: TransactionMetadata,
        proxies: Optional[Dict[str, Proxy]] = None,
        chain_id: Optional[str] = None,
    ) -> Optional[DecodedCall]:
        return ABICallsDecoder(
            repository=self._repository, chain_id=chain_id or self._default_chain
        ).decode(
            call=root_call,
            block=block,
            transaction=transaction,
            proxies=proxies,
            chain_id=chain_id or self._default_chain,
        )

    def decode_call(
        self,
        root_call: Call,
        block: BlockMetadata,
        transaction: TransactionMetadata,
        proxies: Optional[Dict[str, Proxy]] = None,
    ) -> Optional[DecodedCall]:
        return ABICallsDecoder(
            repository=self._repository, chain_id=self._default_chain
        ).decode(call=root_call, block=block, transaction=transaction, proxies=proxies)

    def decode_events(
        self,
        events: [Event],
        block: BlockMetadata,
        transaction: TransactionMetadata,
        proxies: Optional[Dict[str, Proxy]] = None,
        chain_id: Optional[str] = None,
    ) -> List[DecodedEvent]:
        return ABIEventsDecoder(
            repository=self._repository, chain_id=chain_id or self._default_chain
        ).decode(
            events=events,
            block=block,
            transaction=transaction,
            proxies=proxies or {},
            chain_id=chain_id or self._default_chain,
        )

    def decode_event(
        self,
        events: Event,
        block: BlockMetadata,
        transaction: TransactionMetadata,
        proxies: Optional[Dict[str, Proxy]] = None,
        chain_id: Optional[str] = None,
    ) -> DecodedEvent:
        return ABIEventsDecoder(
            repository=self._repository, chain_id=chain_id or self._default_chain
        ).decode(
            events=events,
            block=block,
            transaction=transaction,
            proxies=proxies or {},
            chain_id=chain_id or self._default_chain,
        )

    def decode_transfers(
        self,
        call: DecodedCall,
        events: List[DecodedEvent],
        proxies: Optional[Dict[str, Proxy]] = None,
        chain_id: Optional[str] = None,
    ):
        return ABITransfersDecoder(
            repository=self._repository, chain_id=chain_id or self._default_chain
        ).decode(call=call, events=events, proxies=proxies or {})

    def decode_balances(self, transfers: List[DecodedTransfer]):
        return ABIBalancesDecoder(
            repository=self._repository, chain_id=self._default_chain
        ).decode(transfers=transfers)

    def _decode_transaction(
        self,
        block: BlockMetadata,
        transaction: Transaction,
        chain_id: str,
        proxies: Optional[Dict[str, Proxy]] = None,
    ) -> DecodedTransaction:

        full_decoded_transaction = DecodedTransaction(
            block_metadata=block,
            metadata=transaction.metadata,
            events=[],
            calls=None,
            transfers=[],
            balances=[],
        )

        try:
            full_decoded_transaction.events = self.decode_events(
                transaction.events, block, transaction.metadata, proxies, chain_id
            )
        except Exception as e:
            log.exception(
                "ABI decoding of events for %s / %s failed.",
                transaction.metadata.tx_hash,
                chain_id,
            )
            raise e

        try:
            full_decoded_transaction.calls = self.decode_calls(
                transaction.root_call, block, transaction.metadata, proxies, chain_id
            )
        except Exception as e:
            log.exception(
                "ABI decoding of calls tree for %s / %s failed.",
                transaction.metadata.tx_hash,
                chain_id,
            )
            raise e

        try:
            full_decoded_transaction.transfers = self.decode_transfers(
                full_decoded_transaction.calls,
                full_decoded_transaction.events,
                proxies,
                chain_id,
            )
        except Exception as e:
            log.exception(
                "ABI decoding of transfers for %s / %s failed.",
                transaction.metadata.tx_hash,
                chain_id,
            )
            raise e

        try:
            full_decoded_transaction.balances = self.decode_balances(
                full_decoded_transaction.transfers
            )
        except Exception as e:
            log.exception(
                "ABI decoding of balances for %s / %s failed.",
                transaction.metadata.tx_hash,
                chain_id,
            )
            raise e

        # remove chained delegatecalls from the tree
        prune_delegates(full_decoded_transaction.calls)

        full_decoded_transaction.status = True

        return full_decoded_transaction
