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

from typing import List, Dict, Union, Optional

from ethtx.models.decoded_model import DecodedEvent, Proxy, AddressInfo
from ethtx.models.objects_model import BlockMetadata, TransactionMetadata, Event
from ethtx.semantics.standards.erc20 import ERC20_EVENTS
from ethtx.semantics.standards.erc721 import ERC721_EVENTS
from .abc import ABISubmoduleAbc
from .helpers.utils import decode_event_abi_name_with_external_source
from ..decoders.parameters import decode_event_parameters


class ABIEventsDecoder(ABISubmoduleAbc):
    """ABI Events Decoder."""

    def decode(
        self,
        events: Union[Event, List[Event]],
        block: BlockMetadata,
        transaction: TransactionMetadata,
        proxies: Optional[Dict[str, Proxy]] = None,
        chain_id: Optional[str] = None,
    ) -> Union[DecodedEvent, List[DecodedEvent]]:
        """Return list of decoded events."""
        if isinstance(events, list):
            return (
                [
                    self.decode_event(event, block, transaction, proxies, chain_id)
                    for event in events
                ]
                if events
                else []
            )

        return self.decode_event(events, block, transaction, proxies, chain_id)

    def decode_event(
        self,
        event: Event,
        block: BlockMetadata,
        transaction: TransactionMetadata,
        proxies: Dict[str, Proxy] = None,
        chain_id: str = None,
    ) -> DecodedEvent:

        if event.topics:
            event_signature = event.topics[0]
        else:
            event_signature = None

        anonymous, guessed = False, False
        chain_id = chain_id or self._default_chain

        event_abi = self._repository.get_event_abi(
            chain_id, event.contract, event_signature
        )

        if not event_abi:

            if not event_abi:
                # if signature is not known but there is exactly one anonymous event in tha ABI
                # we can assume that this is this the anonymous one (e.g. Maker's LogNote)
                event_abi = self._repository.get_anonymous_event_abi(
                    chain_id, event.contract
                )
                if event_abi:
                    anonymous = True

            if not event_abi and event.contract in proxies:
                # try to find signature in delegate-called contracts
                for semantic in proxies[event.contract].semantics:
                    event_abi = (
                        semantic.contract.events[event_signature]
                        if event_signature in semantic.contract.events
                        else None
                    )
                    if event_abi:
                        break

            if not event_abi and event_signature in ERC20_EVENTS:
                # try standard ERC20 events
                if (
                    len(
                        [
                            parameter
                            for parameter in ERC20_EVENTS[event_signature].parameters
                            if parameter.indexed
                        ]
                    )
                    == len([topic for topic in event.topics if topic]) - 1
                ):
                    event_abi = ERC20_EVENTS[event_signature]
                elif event_signature in ERC721_EVENTS:
                    # try standard ERC721 events
                    if (
                        len(
                            [
                                parameter
                                for parameter in ERC721_EVENTS[
                                    event_signature
                                ].parameters
                                if parameter.indexed
                            ]
                        )
                        == len([topic for topic in event.topics if topic]) - 1
                    ):
                        event_abi = ERC721_EVENTS[event_signature]

        contract_name = self._repository.get_address_label(
            chain_id, event.contract, proxies
        )

        if event_abi:
            event_name = event_abi.name
        elif event_signature:
            event_name = event_signature
        else:
            event_name = "Anonymous"

        parameters = decode_event_parameters(
            event.log_data, event.topics, event_abi, anonymous
        )

        if event_name.startswith("0x") and len(event_name) > 2:
            guessed, event_name = decode_event_abi_name_with_external_source(
                signature=event_signature
            )

        return DecodedEvent(
            chain_id=chain_id,
            tx_hash=transaction.tx_hash,
            timestamp=block.timestamp,
            contract=AddressInfo(address=event.contract, name=contract_name),
            index=event.log_index,
            call_id=event.call_id,
            event_signature=event_signature,
            event_name=event_name,
            parameters=parameters,
            event_guessed=guessed,
        )
