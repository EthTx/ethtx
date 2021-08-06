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

from typing import Optional, Dict

from ethtx.models.decoded_model import DecodedCall
from ethtx.models.objects_model import Call, TransactionMetadata, BlockMetadata
from ethtx.utils.measurable import RecursionLimit
from ethtx.semantics.solidity.precompiles import precompiles
from .abc import ABISubmoduleAbc
from ..decoders.parameters import decode_function_parameters, decode_graffiti_parameters

RECURSION_LIMIT = 2000


class ABICallsDecoder(ABISubmoduleAbc):
    """Abi Calls Decoder."""

    def decode(
        self,
        call: Call,
        block: BlockMetadata,
        transaction: TransactionMetadata,
        delegations: Optional[Dict[str, set]] = None,
        token_proxies: Optional[Dict[str, dict]] = None,
        chain_id: Optional[str] = None,
    ) -> Optional[DecodedCall]:
        """Decode call with sub_calls."""

        if not call:
            return None

        indent = 0
        status = True
        call_id = ""

        decoded_root_call = self.decode_call(
            call,
            block,
            transaction,
            call_id,
            indent,
            status,
            delegations,
            token_proxies,
            chain_id,
        )

        with RecursionLimit(RECURSION_LIMIT):
            calls_tree = self._decode_nested_calls(
                decoded_root_call,
                block,
                transaction,
                call.subcalls,
                indent,
                status,
                delegations,
                token_proxies,
                chain_id,
            )

        calls_tree = self._prune_delegates(calls_tree)

        return calls_tree

    def decode_call(
        self,
        call: Call,
        block: BlockMetadata,
        transaction: TransactionMetadata,
        call_id: str = "",
        indent: int = 0,
        status: bool = True,
        delegations: Dict[str, set] = None,
        token_proxies: Dict[str, dict] = None,
        chain_id: str = None,
    ) -> DecodedCall:
        """Decode single call."""

        chain_id = chain_id or self._default_chain

        if call.call_data:
            function_signature = call.call_data[:10]
        else:
            function_signature = None

        from_name = self._repository.get_address_label(
            chain_id, call.from_address, token_proxies
        )
        to_name = self._repository.get_address_label(
            chain_id, call.to_address, token_proxies
        )

        delegations = delegations or {}

        if call.call_type == "selfdestruct":
            function_name = call.call_type
            function_input, function_output = [], []
        elif call.call_type == "create2":
            # ToDo: parse constructor
            # ToDo: force semantics reload

            # constructor_abi = self.repository.get_constructor_abi(call.chain_id, call.to_address)
            function_name = "new"
            function_input, function_output = [], []

        elif self._repository.check_is_contract(chain_id, call.to_address):

            function_abi = self._repository.get_function_abi(
                chain_id, call.to_address, function_signature
            )
            if not function_abi and call.to_address in delegations:
                # try to find signature in delegate-called contracts
                for delegate in delegations[call.to_address]:
                    function_abi = self._repository.get_function_abi(
                        chain_id, delegate, function_signature
                    )
                    if function_abi:
                        break

            function_name = function_abi.name if function_abi else function_signature
            function_input, function_output = decode_function_parameters(
                call.call_data, call.return_value, function_abi, call.status
            )
            if (
                not call.status
                and function_output
                and function_output[0].name == "Error"
            ):
                error_description = function_output.pop()
                call.error = f'Failed with "{error_description.value}"'
        elif call.to_address and int(call.to_address, 16) in precompiles:
            function_semantics = precompiles[int(call.to_address, 16)]
            function_name = function_semantics.name
            function_input, function_output = decode_function_parameters(
                call.call_data, call.return_value, function_semantics, call.status,
                strip_signature=False
            )
        else:
            function_name = "fallback"
            function_input = decode_graffiti_parameters(call.call_data)
            function_output = []

        return DecodedCall(
            chain_id=chain_id,
            tx_hash=transaction.tx_hash,
            timestamp=block.timestamp,
            call_id=call_id,
            call_type=call.call_type,
            from_address=call.from_address,
            from_name=from_name,
            to_address=call.to_address,
            to_name=to_name,
            value=call.call_value / 10 ** 18,
            function_signature=function_signature,
            function_name=function_name,
            arguments=function_input,
            outputs=function_output,
            gas_used=call.gas_used,
            error=call.error,
            status=status,
            indent=indent,
        )

    def _decode_nested_calls(
        self,
        call: DecodedCall,
        block: BlockMetadata,
        transaction: TransactionMetadata,
        sub_calls,
        indent,
        status,
        delegations,
        token_proxies,
        chain_id,
    ) -> DecodedCall:
        """Decode nested calls. Call may have sub_calls, if they exist, it will recursively process them."""
        for i, sub_call in enumerate(sub_calls):
            status = status and call.status

            sub_call_id = (
                "_".join([call.call_id, str(i).zfill(4)]) if call.call_id else str(i)
            )
            decoded = self.decode_call(
                sub_call,
                block,
                transaction,
                sub_call_id,
                indent + 1,
                status,
                delegations,
                token_proxies,
                chain_id,
            )
            call.subcalls.append(decoded)

            if sub_call.subcalls:
                self._decode_nested_calls(
                    decoded,
                    block,
                    transaction,
                    sub_call.subcalls,
                    indent + 1,
                    status,
                    delegations,
                    token_proxies,
                    chain_id,
                )

        return call

    def _prune_delegates(self, call: DecodedCall) -> DecodedCall:

        while len(call.subcalls) == 1 and call.subcalls[0].call_type == "delegatecall":
            _value = call.value
            call = call.subcalls[0]
            call.value = _value

        for i, sub_call in enumerate(call.subcalls):
            call.subcalls[i] = self._prune_delegates(sub_call)

        return call
