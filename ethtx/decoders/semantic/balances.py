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

from ethtx.models.decoded_model import DecodedBalance, DecodedTransactionMetadata
from .helpers.utils import get_badge
from .abc import SemanticSubmoduleAbc


class SemanticBalancesDecoder(SemanticSubmoduleAbc):
    """Semantic Balances Decoder."""

    def decode(
        self, balances: List[DecodedBalance], tx_metadata: DecodedTransactionMetadata
    ) -> List[DecodedBalance]:
        """Semantically decode balances."""

        for balance in balances:

            # decode the proper holder badge
            balance.holder.badge = get_badge(
                balance.holder.address,
                tx_metadata.sender.address,
                tx_metadata.receiver.address,
            )

            for token in balance.tokens:
                token["balance"] = f"{token['balance']:,.4f}"

        return balances
