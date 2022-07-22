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
from typing import List, Union, Dict

from web3 import Web3

from ethtx.decoders.semantic.helpers.utils import (
    create_transformation_context,
    semantically_decode_parameter,
    get_badge,
)
from ethtx.models.decoded_model import DecodedEvent, DecodedTransactionMetadata, Proxy
from ethtx.semantics.protocols.anonymous import anonymous_events
from ethtx.semantics.standards.erc20 import ERC20_EVENTS, ERC20_TRANSFORMATIONS
from ethtx.semantics.standards.erc721 import ERC721_TRANSFORMATIONS, ERC721_EVENTS
from .abc import SemanticSubmoduleAbc

log = logging.getLogger(__name__)


class SemanticEventsDecoder(SemanticSubmoduleAbc):
    """Semantic Events Decoder."""

    def decode(
        self,
        events: Union[DecodedEvent, List[DecodedEvent]],
        tx_metadata: DecodedTransactionMetadata,
        proxies: Dict[str, Proxy],
    ) -> Union[DecodedEvent, List[DecodedEvent]]:
        """Semantically decode events."""
        if isinstance(events, list):
            return (
                [self.decode_event(event, tx_metadata, proxies) for event in events]
                if events
                else []
            )

        return self.decode_event(events, tx_metadata, proxies)

    def decode_event(
        self,
        event: DecodedEvent,
        tx_metadata: DecodedTransactionMetadata,
        proxies: Dict[str, Proxy],
    ) -> DecodedEvent:
        """Semantically decode event"""

        def _get_parameters_str(parameters):
            parameters_types = []
            for parameter in parameters:
                if parameter.type == "tuple":
                    parameters_types.append(_get_parameters_str(parameter.value))
                else:
                    parameters_types.append(parameter.type)
            return f'({",".join(parameters_types)})'

        if event.event_name != event.event_signature:
            # calculate signature to account for anonymous events
            parameters_str = _get_parameters_str(event.parameters)
            calculated_event_signature = Web3.keccak(
                text=f"{event.event_name}{parameters_str}"
            ).hex()
        else:
            calculated_event_signature = event.event_signature

        if (
            event.event_signature
            and event.event_name != event.event_signature
            and calculated_event_signature != event.event_signature
            and calculated_event_signature not in anonymous_events
            and not event.event_guessed
        ):
            log.warning(
                "Event signature mismatch: %s / %s.",
                calculated_event_signature,
                event.event_signature,
            )

        # read transformations from the repository
        event_transformations = self.repository.get_transformations(
            event.chain_id, event.contract.address, calculated_event_signature
        )

        if event_transformations:
            event.event_name = event_transformations.get("name") or event.event_name
        else:
            if calculated_event_signature in anonymous_events and (
                not event_transformations
                or event.event_signature not in event_transformations
            ):
                event_transformations = anonymous_events[calculated_event_signature]
            else:
                event_transformations = {}

        # prepare context for transformations
        context = create_transformation_context(
            event.contract.address, event.parameters, [], tx_metadata, self.repository
        )
        standard = self.repository.get_standard(event.chain_id, event.contract.address)
        if (
            not standard
            and event.contract.address in proxies
            and proxies[event.contract.address].token
        ):
            standard = "ERC20"

        # perform parameters transformation
        for i, parameter in enumerate(event.parameters):
            semantically_decode_parameter(
                self.repository,
                parameter,
                f"__input{i}__",
                event_transformations,
                proxies,
                context,
            )

        if standard == "ERC20":
            # decode ERC20 events if transformations for them are not defined
            if event.event_signature in ERC20_EVENTS and (
                not event_transformations
                or event.event_signature not in event_transformations
            ):
                event_transformations = ERC20_TRANSFORMATIONS.get(event.event_signature)
                if event_transformations:
                    for i, parameter in enumerate(event.parameters):
                        semantically_decode_parameter(
                            self.repository,
                            parameter,
                            f"__input{i}__",
                            event_transformations,
                            proxies,
                            context,
                        )
        elif standard == "ERC721":
            # decode ERC721 events if transformations for them are not defined
            if event.event_signature in ERC721_EVENTS and (
                not event_transformations
                or event.event_signature not in event_transformations
            ):
                event_transformations = ERC721_TRANSFORMATIONS.get(
                    event.event_signature
                )
                if event_transformations:
                    for i, parameter in enumerate(event.parameters):
                        semantically_decode_parameter(
                            self.repository,
                            parameter,
                            f"__input{i}__",
                            event_transformations,
                            proxies,
                            context,
                        )

        # decode proper emitter badge
        event.contract.badge = get_badge(
            event.contract.address, tx_metadata.sender, tx_metadata.receiver
        )

        # remove ignored parameters
        event.parameters = [
            parameter for parameter in event.parameters if parameter.type != "ignore"
        ]

        return event
