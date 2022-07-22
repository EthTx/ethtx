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

from collections import defaultdict
from typing import List

from ethtx.models.decoded_model import DecodedTransfer, DecodedBalance, AddressInfo
from .abc import ABISubmoduleAbc

ZERO_ADDRESS = "0x" + 40 * "0"


class ABIBalancesDecoder(ABISubmoduleAbc):
    """Abi Balances Decoder."""

    def decode(self, transfers: List[DecodedTransfer]) -> List:
        """Decode balances."""

        balance_holders = {}
        balance_tokens = {}

        for transfer in transfers:
            if transfer.from_address.address != ZERO_ADDRESS:
                balance_holders[
                    transfer.from_address.address
                ] = transfer.from_address.name
            if transfer.to_address.address != ZERO_ADDRESS:
                balance_holders[transfer.to_address.address] = transfer.to_address.name
            balance_tokens[transfer.token_address] = (
                transfer.token_standard,
                transfer.token_symbol,
            )

        balance_sheet: dict = {address: defaultdict(int) for address in balance_holders}

        for transfer in transfers:
            if transfer.from_address.address != ZERO_ADDRESS:
                balance_sheet[transfer.from_address.address][
                    transfer.token_address
                ] -= transfer.value
            if transfer.to_address.address != ZERO_ADDRESS:
                balance_sheet[transfer.to_address.address][
                    transfer.token_address
                ] += transfer.value

        balances = []
        for holder_address in balance_holders:
            tokens = []
            for token_address in balance_sheet[holder_address]:
                if balance_sheet[holder_address][token_address]:
                    token_standard, token_symbol = balance_tokens[token_address]
                    tokens.append(
                        dict(
                            token_address=token_address,
                            token_symbol=token_symbol,
                            token_standard=token_standard,
                            balance=balance_sheet[holder_address][token_address],
                        )
                    )
            if tokens:
                holder_name = balance_holders[holder_address]
                balances.append(
                    DecodedBalance(
                        holder=AddressInfo(address=holder_address, name=holder_name),
                        tokens=tokens,
                    )
                )

        return balances
