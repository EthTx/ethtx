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
from typing import Dict, List, Union

from .abi.decoder import ABIDecoder
from .semantic.decoder import SemanticDecoder
from ..models.decoded_model import DecodedTransaction, Proxy
from ..models.objects_model import Block, Call
from ..providers.web3_provider import NodeDataProvider
from ..semantics.standards.eip1969 import is_eip1969_proxy, is_eip1969_beacon_proxy

log = logging.getLogger(__name__)


class DecoderService:
    def __init__(
        self,
        abi_decoder: ABIDecoder,
        semantic_decoder: SemanticDecoder,
        web3provider: NodeDataProvider,
        default_chain: str,
    ):
        self.abi_decoder: ABIDecoder = abi_decoder
        self.semantic_decoder: SemanticDecoder = semantic_decoder
        self.web3provider: NodeDataProvider = web3provider
        self.default_chain: str = default_chain

    def decode_transaction(self, chain_id: str, tx_hash: str) -> DecodedTransaction:

        # verify the transaction hash
        tx_hash = tx_hash if tx_hash.startswith("0x") else "0x" + tx_hash

        chain_id = chain_id or self.default_chain

        self.semantic_decoder.repository.record()
        # read a raw transaction from a node
        transaction = self.web3provider.get_full_transaction(
            tx_hash=tx_hash, chain_id=chain_id
        )
        # read a raw block from a node
        block = Block.from_raw(
            w3block=self.web3provider.get_block(
                transaction.metadata.block_number, chain_id
            ),
            chain_id=chain_id,
        )

        # prepare lists of delegations to properly decode delegate-calling contracts
        delegations = self.get_delegations(transaction.root_call)
        proxies = self.get_proxies(delegations, chain_id)

        # decode transaction using ABI
        abi_decoded_tx = self.abi_decoder.decode_transaction(
            block=block, transaction=transaction, proxies=proxies, chain_id=chain_id
        )

        # decode transaction using additional semantics
        semantically_decoded_tx = self.semantic_decoder.decode_transaction(
            block=block.metadata,
            transaction=abi_decoded_tx,
            proxies=proxies,
            chain_id=chain_id,
        )

        used_semantics = self.semantic_decoder.repository.end_record()
        log.info(
            "Semantics used in decoding %s: %s",
            tx_hash,
            ", ".join(used_semantics) if used_semantics else "",
        )

        return semantically_decoded_tx

    def get_proxies(
        self, delegations: Dict[str, List[str]], chain_id: str
    ) -> Dict[str, Proxy]:

        proxies = {}
        chain = self.web3provider._get_node_connection(chain_id)

        for delegator in delegations:

            delegator_semantics = self.semantic_decoder.repository.get_semantics(
                chain_id, delegator
            )

            if is_eip1969_proxy(chain, delegator, delegations[delegator][0]):
                proxy_type = "EIP1969Proxy"
                fallback_name = "EIP1969_Proxy"

            elif is_eip1969_beacon_proxy(chain, delegator, delegations[delegator][0]):
                proxy_type = "EIP1969Beacon"
                fallback_name = "EIP1969_BeaconProxy"

            else:
                proxy_type = "GenericProxy"
                fallback_name = "Proxy"

            delegates_semantics = [
                self.semantic_decoder.repository.get_semantics(chain_id, delegate)
                for delegate in delegations[delegator]
            ]

            token_semantics = delegator_semantics.erc20
            if not token_semantics:
                for delegate_semantics in delegates_semantics:
                    if delegate_semantics.erc20:
                        token_semantics = delegate_semantics.erc20
                        break

            proxies[delegator] = Proxy(
                address=delegator,
                name=delegator_semantics.name
                if delegator_semantics and delegator_semantics.name != delegator
                else fallback_name,
                type=proxy_type,
                semantics=[semantics for semantics in delegates_semantics if semantics],
                token=token_semantics,
            )

        return proxies

    @staticmethod
    def get_delegations(calls: Union[Call, List[Call]]) -> Dict[str, List[str]]:

        delegations = {}

        if not calls:
            return delegations

        if isinstance(calls, list):
            for call in calls:
                if call.call_type == "delegatecall":
                    if call.from_address not in delegations:
                        delegations[call.from_address] = []
                    if call.to_address not in delegations[call.from_address]:
                        delegations[call.from_address].append(call.to_address)
        else:
            calls_queue = [calls]

            while calls_queue:
                call = calls_queue.pop()
                for _, sub_call in enumerate(call.subcalls):
                    calls_queue.insert(0, sub_call)

                if call.call_type == "delegatecall":
                    if call.from_address not in delegations:
                        delegations[call.from_address] = []
                    if call.to_address not in delegations[call.from_address]:
                        delegations[call.from_address].append(call.to_address)

        return delegations
