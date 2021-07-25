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

from typing import List

from ethtx.models.decoded_model import DecodedCall, DecodedTransfer, AddressInfo
from ethtx.utils.measurable import RecursionLimit
from .abc import ABISubmoduleAbc

RECURSION_LIMIT = 2000
ZERO_ADDRESS = "0x" + 40 * "0"


class ABITransfersDecoder(ABISubmoduleAbc):
    """Abi Transfers Decoder."""

    def decode(
        self,
        call: DecodedCall,
        events, token_proxies
    ) -> List:
        """Decode transfers."""
        transfers = []

        def _transfers_calls(decoded_call):
            if decoded_call.status and decoded_call.value:
                transfers.append(
                    DecodedTransfer(
                        from_address=decoded_call.from_address,
                        to_address=decoded_call.to_address,
                        token_standard="ETH",
                        token_address=ZERO_ADDRESS,
                        token_symbol="ETH",
                        value=decoded_call.value,
                    )
                )
            if decoded_call.subcalls:
                for sub_call in decoded_call.subcalls:
                    _transfers_calls(sub_call)

        if call:
            with RecursionLimit(RECURSION_LIMIT):
                _transfers_calls(call)

        for event in events:

            if event.event_name == "Transfer":

                from_address = event.parameters[0].value
                from_name = self._repository.get_address_label(
                    event.chain_id, from_address, token_proxies
                )
                to_address = event.parameters[1].value
                to_name = self._repository.get_address_label(
                    event.chain_id, to_address, token_proxies
                )

                standard = self._repository.get_standard(
                    event.chain_id, event.contract.address
                )

                if standard == "ERC20" or event.contract.address in token_proxies:

                    _, token_symbol, token_decimals = self._repository.get_token_data(
                        event.chain_id, event.contract.address, token_proxies
                    )
                    value = event.parameters[2].value / 10 ** token_decimals
                    transfers.append(
                        DecodedTransfer(
                            from_address=AddressInfo(from_address, from_name),
                            to_address=AddressInfo(to_address, to_name),
                            token_standard=standard,
                            token_address=event.contract.address,
                            token_symbol=token_symbol,
                            value=value,
                        )
                    )
                elif standard == "ERC721":
                    if len(str(event.parameters[2].value)) > 8:
                        token_symbol = (
                            f"NFT {str(event.parameters[2].value)[:6]}..."
                            f"{str(event.parameters[2].value)[-2:]}"
                        )
                    else:
                        token_symbol = f"NFT {event.parameters[2].value}"
                    token_address = f"{event.contract.address}?a={event.parameters[2].value}#inventory"
                    transfers.append(
                        DecodedTransfer(
                            from_address=AddressInfo(from_address, from_name),
                            to_address=AddressInfo(to_address, to_name),
                            token_standard=standard,
                            token_address=token_address,
                            token_symbol=token_symbol,
                            value=1,
                        )
                    )

        return transfers
