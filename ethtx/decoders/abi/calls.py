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
from typing import Optional, Dict

from ethtx.models.decoded_model import DecodedCall, Proxy, AddressInfo
from ethtx.models.objects_model import Call, TransactionMetadata, BlockMetadata
from ethtx.semantics.solidity.precompiles import precompiles
from ethtx.semantics.standards.erc20 import ERC20_FUNCTIONS
from ethtx.semantics.standards.erc721 import ERC721_FUNCTIONS
from ethtx.utils.measurable import RecursionLimit
from .abc import ABISubmoduleAbc
from .helpers.utils import decode_function_abi_with_external_source
from ..decoders.parameters import decode_function_parameters, decode_graffiti_parameters

log = logging.getLogger(__name__)

RECURSION_LIMIT = 2000


class ABICallsDecoder(ABISubmoduleAbc):
    """Abi Calls Decoder."""

    def decode(
        self,
        call: Call,
        block: BlockMetadata,
        transaction: TransactionMetadata,
        proxies: Optional[Dict[str, Proxy]] = None,
        chain_id: Optional[str] = None,
    ) -> Optional[DecodedCall]:
        """Decode call with sub_calls."""

        if not call:
            return None

        indent = 0
        status = True
        call_id = ""

        decoded_root_call = self.decode_call(
            call, block, transaction, call_id, indent, status, proxies or {}, chain_id
        )

        with RecursionLimit(RECURSION_LIMIT):
            calls_tree = self._decode_nested_calls(
                decoded_root_call,
                block,
                transaction,
                call.subcalls,
                indent,
                status,
                proxies,
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
        proxies: Dict[str, Proxy] = None,
        chain_id: str = None,
    ) -> DecodedCall:
        """Decode single call."""

        guessed = False
        chain_id = chain_id or self._default_chain

        if call.call_data:
            function_signature = call.call_data[:10]
        else:
            function_signature = None

        from_name = self._repository.get_address_label(
            chain_id, call.from_address, proxies
        )

        to_name = self._repository.get_address_label(chain_id, call.to_address, proxies)

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
            standard = self._repository.get_standard(chain_id, call.to_address)

            function_abi = self._repository.get_function_abi(
                chain_id, call.to_address, function_signature
            )

            function_signature = call.call_data[:10] if call.call_data else ""

            if not function_abi and call.to_address in proxies:
                # try to find signature in delegate-called contracts
                for semantic in proxies[call.to_address].semantics:
                    function_abi = (
                        semantic.contract.functions[function_signature]
                        if function_signature in semantic.contract.functions
                        else None
                    )
                    if function_abi:
                        break

            if not function_abi:
                if standard == "ERC20":
                    # decode ERC20 calls if ABI for them is not defined
                    function_abi = ERC20_FUNCTIONS.get(function_signature)
                elif standard == "ERC721":
                    # decode ERC721 calls if ABI for them is not defined
                    function_abi = ERC721_FUNCTIONS.get(function_signature)

            function_name = function_abi.name if function_abi else function_signature

            function_input, function_output = decode_function_parameters(
                call.call_data, call.return_value, function_abi, call.status
            )

            if function_name.startswith("0x") and len(function_signature) > 2:
                functions_abi_provider = decode_function_abi_with_external_source(
                    signature=function_signature, repository=self._repository
                )
                for guessed, function_abi_provider in functions_abi_provider:
                    try:
                        function_abi = function_abi_provider
                        function_name = function_abi.name
                        function_input, function_output = decode_function_parameters(
                            call.call_data, call.return_value, function_abi, call.status
                        )
                    except Exception as e:
                        log.info(
                            "Skipping getting function from external source and trying to get next. Error: %s",
                            e,
                        )
                        continue
                    else:
                        break

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
                call.call_data,
                call.return_value,
                function_semantics,
                call.status,
                strip_signature=False,
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
            from_address=AddressInfo(address=call.from_address, name=from_name),
            to_address=AddressInfo(address=call.to_address, name=to_name),
            value=call.call_value / 10**18,
            function_signature=function_signature,
            function_name=function_name,
            arguments=function_input,
            outputs=function_output,
            gas_used=call.gas_used,
            error=call.error,
            status=status,
            indent=indent,
            function_guessed=guessed,
        )

    def _decode_nested_calls(
        self,
        call: DecodedCall,
        block: BlockMetadata,
        transaction: TransactionMetadata,
        sub_calls,
        indent,
        status,
        proxies,
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
                proxies,
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
                    proxies,
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
