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

import logging
import traceback
from typing import Optional, Dict, List

from ethtx.models.decoded_model import (
    DecodedTransaction,
    DecodedCall,
    DecodedEvent,
    DecodedTransfer,
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


class ABIDecoder(IABIDecoder):
    def decode_transaction(
        self,
        block: Block,
        transaction: Transaction,
        chain_id: str,
        delegations: Optional[Dict[str, set]] = None,
        token_proxies: Optional[Dict[str, dict]] = None,
    ) -> Optional[DecodedTransaction]:

        log.info("ABI decoding for %s / %s.", transaction.metadata.tx_hash, chain_id)

        try:
            with ExecutionTimer(f"ABI decoding for " + transaction.metadata.tx_hash):
                log.info(
                    "ABI decoding for %s / %s.", transaction.metadata.tx_hash, chain_id
                )
                full_decoded_transaction = self._decode_transaction(
                    block.metadata, transaction, chain_id, delegations, token_proxies
                )
                return full_decoded_transaction
        except Exception as e:
            log.warning(
                "ABI decoding of %s / %s failed.",
                transaction.metadata.tx_hash,
                chain_id,
            )
            traceback.print_exc(e)
            return None

    def decode_calls(
        self,
        root_call: Call,
        block: BlockMetadata,
        transaction: TransactionMetadata,
        delegations: Optional[Dict[str, set]] = None,
        token_proxies: Optional[Dict[str, dict]] = None,
        chain_id: Optional[str] = None,
    ) -> Optional[DecodedCall]:
        return ABICallsDecoder(
            repository=self._repository, chain_id=chain_id or self._default_chain
        ).decode(
            call=root_call,
            block=block,
            transaction=transaction,
            delegations=delegations,
            token_proxies=token_proxies,
            chain_id=chain_id or self._default_chain
        )

    def decode_call(
        self,
        root_call: Call,
        block: BlockMetadata,
        transaction: TransactionMetadata,
        delegations: Optional[Dict[str, set]] = None,
        token_proxies: Optional[Dict[str, dict]] = None,
    ) -> Optional[DecodedCall]:
        return ABICallsDecoder(
            repository=self._repository, chain_id=self._default_chain
        ).decode(
            call=root_call,
            block=block,
            transaction=transaction,
            delegations=delegations,
            token_proxies=token_proxies,
        )

    def decode_events(
        self,
        events: [Event],
        block: BlockMetadata,
        transaction: TransactionMetadata,
        delegations: Optional[Dict[str, set]] = None,
        token_proxies: Optional[Dict[str, dict]] = None,
        chain_id: Optional[str] = None,
    ) -> List[DecodedEvent]:
        return ABIEventsDecoder(
            repository=self._repository, chain_id=chain_id or self._default_chain
        ).decode(
            events=events,
            block=block,
            transaction=transaction,
            delegations=delegations or {},
            token_proxies=token_proxies or {},
            chain_id=chain_id or self._default_chain
        )

    def decode_event(
        self,
        events: Event,
        block: BlockMetadata,
        transaction: TransactionMetadata,
        delegations: Optional[Dict[str, set]] = None,
        token_proxies: Optional[Dict[str, dict]] = None,
        chain_id: Optional[str] = None,
    ) -> DecodedEvent:
        return ABIEventsDecoder(
            repository=self._repository, chain_id=chain_id or self._default_chain
        ).decode(
            events=events,
            block=block,
            transaction=transaction,
            delegations=delegations or {},
            token_proxies=token_proxies or {},
            chain_id=chain_id or self._default_chain
        )

    def decode_transfers(
        self,
        call: DecodedCall,
        events: List[DecodedEvent],
        token_proxies: Optional[Dict[str, dict]] = None,
        chain_id: Optional[str] = None,
    ):
        return ABITransfersDecoder(
            repository=self._repository, chain_id=chain_id or self._default_chain
        ).decode(
            call=call,
            events=events,
            token_proxies=token_proxies or {},
        )

    def decode_balances(self, transfers: List[DecodedTransfer]):
        return ABIBalancesDecoder(
            repository=self._repository, chain_id=self._default_chain
        ).decode(transfers=transfers)

    def _decode_transaction(
        self,
        block: BlockMetadata,
        transaction: Transaction,
        chain_id: str,
        delegations: Optional[Dict[str, set]] = None,
        token_proxies: Optional[Dict[str, dict]] = None,
    ) -> DecodedTransaction:

        full_decoded_transaction = DecodedTransaction(
            block_metadata=block,
            tx_metadata=transaction.metadata,
            events=[],
            calls=None,
            transfers=[],
            balances=[],
        )

        self._repository.record()

        try:
            full_decoded_transaction.events = self.decode_events(
                transaction.events,
                block,
                transaction.metadata,
                delegations,
                token_proxies,
                chain_id
            )
        except Exception as e:
            log.warning(
                "ABI decoding of events for %s / %s failed.",
                transaction.metadata.tx_hash,
                chain_id,
            )
            log.warning(e)
            return full_decoded_transaction

        try:
            full_decoded_transaction.calls = self.decode_calls(
                transaction.root_call,
                block,
                transaction.metadata,
                delegations,
                token_proxies,
                chain_id
            )
        except Exception as e:
            log.warning(
                "ABI decoding of calls tree for %s / %s failed.",
                transaction.metadata.tx_hash,
                chain_id,
            )
            log.warning(e)
            return full_decoded_transaction

        try:
            full_decoded_transaction.transfers = self.decode_transfers(
                full_decoded_transaction.calls,
                full_decoded_transaction.events,
                token_proxies,
                chain_id
            )
        except Exception as e:
            log.warning(
                "ABI decoding of transfers for %s / %s failed.",
                transaction.metadata.tx_hash,
                chain_id,
            )
            log.warning(e)
            return full_decoded_transaction

        try:
            full_decoded_transaction.balances = self.decode_balances(
                full_decoded_transaction.transfers
            )
        except Exception as e:
            log.warning(
                "ABI decoding of balances for %s / %s failed.",
                transaction.metadata.tx_hash,
                chain_id,
            )
            log.warning(e)
            return full_decoded_transaction

        used_semantics = self._repository.end_record()
        log.info(
            f"Semantics used in decoding {transaction.metadata.tx_hash}: "
            + ", ".join(used_semantics)
        )

        full_decoded_transaction.status = True

        return full_decoded_transaction
