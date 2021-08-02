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

from ethtx.models.decoded_model import DecodedTransfer, DecodedTransactionMetadata
from .helpers.utils import get_badge
from .abc import SemanticSubmoduleAbc


class SemanticTransfersDecoder(SemanticSubmoduleAbc):
    def decode(
        self, transfers: List[DecodedTransfer], tx_metadata: DecodedTransactionMetadata
    ) -> List[DecodedTransfer]:

        for transfer in transfers:

            # decode proper from and to addresses badges
            transfer.from_address.badge = get_badge(
                transfer.from_address.address,
                tx_metadata.sender.address,
                tx_metadata.receiver.address,
            )
            transfer.to_address.badge = get_badge(
                transfer.to_address.address,
                tx_metadata.sender.address,
                tx_metadata.receiver.address,
            )

            # format the transfer value
            transfer.value = f"{transfer.value:,.4f}"

        return transfers
