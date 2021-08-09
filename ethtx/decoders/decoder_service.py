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

from typing import Dict, List, Union

from ..models.decoded_model import DecodedTransaction
from ..models.objects_model import Block, Call


class DecoderService:
    def __init__(self, abi_decoder, semantic_decoder, web3provider, default_chain):
        self.abi_decoder = abi_decoder
        self.semantic_decoder = semantic_decoder
        self.web3provider = web3provider
        self.default_chain = default_chain

    def get_delegations(
            self,
            calls: Union[Call, List[Call]]
    ) -> Dict[str, set]:

        delegations = {}

        if not calls:
            return delegations

        if isinstance(calls, list):
            for call in calls:
                if call.call_type == "delegatecall":
                    if call.from_address not in delegations:
                        delegations[call.from_address] = set()
                    delegations[call.from_address].add(call.to_address)
        else:
            calls_queue = [calls]

            while calls_queue:
                call = calls_queue.pop()
                for _, sub_call in enumerate(call.subcalls):
                    calls_queue.insert(0, sub_call)

                if call.call_type == "delegatecall":
                    if call.from_address not in delegations:
                        delegations[call.from_address] = set()
                    delegations[call.from_address].add(call.to_address)

        return delegations

    def get_token_proxies(self, delegations: Dict[str, set]) -> Dict[str, Dict]:
        token_proxies = {}

        for delegator in delegations:
            delegator_semantic = self.semantic_decoder.repository.get_token_data(
                self.default_chain, delegator
            )
            if (
                delegator_semantic[0] == delegator
                and delegator_semantic[1] == "Unknown"
            ):
                for delegate in delegations[delegator]:
                    delegate_semantic = self.semantic_decoder.repository.get_token_data(
                        self.default_chain, delegate
                    )
                    if (
                        delegate_semantic[0] != delegate
                        and delegate_semantic[1] != "Unknown"
                    ):
                        token_proxies[delegator] = delegate_semantic
                        break
            elif all(delegator_semantic):
                token_proxies[delegator] = delegator_semantic

        return token_proxies

    def decode_transaction(self, chain_id: str, tx_hash: str) -> DecodedTransaction:

        # verify the transaction hash
        tx_hash = tx_hash if tx_hash.startswith("0x") else "0x" + tx_hash

        chain_id = chain_id or self.default_chain

        # read a raw transaction from a node
        transaction = self.web3provider.get_full_transaction(
            tx_hash=tx_hash, chain_id=chain_id
        )
        # read a raw block from a node
        block = Block.from_raw(
            w3block=self.web3provider.get_block(transaction.metadata.block_number, chain_id),
            chain_id=chain_id,
        )

        # prepare lists of delegations to properly decode delegate-calling contracts
        delegations = self.get_delegations(transaction.root_call)
        token_proxies = self.get_token_proxies(delegations)

        # decode transaction using ABI
        abi_decoded_tx = self.abi_decoder.decode_transaction(
            block=block,
            transaction=transaction,
            delegations=delegations,
            token_proxies=token_proxies,
            chain_id=chain_id,
        )

        # decode transaction using additional semantics
        semantically_decoded_tx = self.semantic_decoder.decode_transaction(
            block=block.metadata,
            transaction=abi_decoded_tx,
            token_proxies=token_proxies,
            chain_id=chain_id,
        )

        return semantically_decoded_tx
