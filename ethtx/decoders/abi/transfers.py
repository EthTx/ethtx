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

from typing import List

from ethtx.models.decoded_model import DecodedCall, DecodedTransfer, AddressInfo
from ethtx.utils.measurable import RecursionLimit
from .abc import ABISubmoduleAbc

RECURSION_LIMIT = 2000
ZERO_ADDRESS = "0x" + 40 * "0"


class ABITransfersDecoder(ABISubmoduleAbc):
    """Abi Transfers Decoder."""

    def decode(self, call: DecodedCall, events, proxies) -> List:
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

            # signatures of Transfer event valid for ERC20 and ERC721 and
            # TransferSingle for ERC1155
            if (
                    event.event_signature in
                    ("0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
                     "0xc3d58168c5ae7397731d063d5bbf3d657854427343f4c083240f7aacaa2d0f62")
            ):

                # Transfer event
                if event.event_signature == "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef":
                    from_address = '0x' + event.parameters[0].value[-40:]
                    to_address = '0x' + event.parameters[1].value[-40:]
                    token_id = event.parameters[2].value
                    value = event.parameters[2].value
                # TransferSingle event
                else:

                    from_address = '0x' + event.parameters[1].value[-40:]
                    to_address = '0x' + event.parameters[2].value[-40:]
                    token_id = event.parameters[3].value
                    value = event.parameters[4].value

                from_name = self._repository.get_address_label(
                    event.chain_id, from_address, proxies
                )
                to_name = self._repository.get_address_label(
                    event.chain_id, to_address, proxies
                )

                standard = self._repository.get_standard(
                    event.chain_id, event.contract.address
                )

                if event.event_signature == "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef" and \
                        (standard == "ERC20" or event.contract.address in proxies):

                    (
                        _,
                        token_symbol,
                        token_decimals,
                        _,
                    ) = self._repository.get_token_data(
                        event.chain_id, event.contract.address, proxies
                    )
                    try:
                        value = value / 10 ** token_decimals
                    except:
                        value = 0

                    transfers.append(
                        DecodedTransfer(
                            from_address=AddressInfo(
                                address=from_address, name=from_name
                            ),
                            to_address=AddressInfo(address=to_address, name=to_name),
                            token_standard=standard,
                            token_address=event.contract.address,
                            token_symbol=token_symbol,
                            value=value,
                        )
                    )
                else:

                    (
                        _,
                        token_symbol,
                        token_decimals,
                        _,
                    ) = self._repository.get_token_data(
                        event.chain_id, event.contract.address, proxies
                    )

                    if event.event_signature == "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef":
                        value = 1
                    else:
                        value = int(value, 16) if type(value) == str else value

                    if token_symbol == 'Unknown':

                        token_symbol = 'NFT'

                    if len(str(token_id)) > 8:
                        token_symbol = (
                            f"{token_symbol} {str(token_id)[:6]}..."
                            f"{str(token_id)[-2:]}"
                        )
                    else:
                        token_symbol = f"{token_symbol} {token_id}"
                    token_address = f"{event.contract.address}?a={token_id}#inventory"
                    transfers.append(
                        DecodedTransfer(
                            from_address=AddressInfo(
                                address=from_address, name=from_name
                            ),
                            to_address=AddressInfo(address=to_address, name=to_name),
                            token_standard=standard,
                            token_address=token_address,
                            token_symbol=token_symbol,
                            value=value,
                        )
                    )

        return transfers
