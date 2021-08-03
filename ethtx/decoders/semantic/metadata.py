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

from ethtx.models.decoded_model import DecodedTransactionMetadata, AddressInfo
from ethtx.models.objects_model import BlockMetadata, TransactionMetadata
from .abc import SemanticSubmoduleAbc
from .helpers.utils import get_eth_price


class SemanticMetadataDecoder(SemanticSubmoduleAbc):
    """Semantic Metadata Decoder."""

    def decode(
        self,
        block_metadata: BlockMetadata,
        tx_metadata: TransactionMetadata,
        chain_id: str,
    ) -> DecodedTransactionMetadata:
        """Semantically decode metadata."""

        decoded_metadata = DecodedTransactionMetadata(
            chain_id=chain_id,
            tx_hash=tx_metadata.tx_hash,
            block_number=block_metadata.block_number,
            block_hash=block_metadata.block_hash,
            timestamp=block_metadata.timestamp,
            gas_price=tx_metadata.gas_price / 10 ** 9,
            sender=AddressInfo(
                tx_metadata.from_address,
                self.repository.get_address_label(chain_id, tx_metadata.from_address),
                "sender",
            ),
            receiver=AddressInfo(
                tx_metadata.to_address,
                self.repository.get_address_label(chain_id, tx_metadata.to_address),
                "receiver",
            ),
            tx_index=tx_metadata.tx_index,
            tx_value=tx_metadata.tx_value,
            eth_price=get_eth_price(),
            gas_limit=tx_metadata.gas_limit,
            gas_used=tx_metadata.gas_used,
            success=tx_metadata.success,
        )

        return decoded_metadata
