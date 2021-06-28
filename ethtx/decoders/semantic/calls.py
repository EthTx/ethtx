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

from typing import Dict

from ethtx.models.decoded_model import DecodedCall, DecodedTransactionMetadata
from ethtx.semantics.standards.erc20 import ERC20_FUNCTIONS, ERC20_TRANSFORMATIONS
from ethtx.semantics.standards.erc721 import ERC721_FUNCTIONS, ERC721_TRANSFORMATIONS
from ethtx.utils.measurable import RecursionLimit
from .abc import SemanticSubmoduleAbc
from .helpers.utils import (
    create_transformation_context,
    semantically_decode_parameter,
    get_badge,
)

RECURSION_LIMIT = 2000


class SemanticCallsDecoder(SemanticSubmoduleAbc):
    """Semantic Calls Decoder."""

    def decode(
        self,
        call: DecodedCall,
        tx_metadata: DecodedTransactionMetadata,
        token_proxies: Dict[str, Dict],
    ) -> DecodedCall:

        function_transformations = self.repository.get_transformations(
            call.chain_id, call.to_address.address, call.function_signature
        )

        if function_transformations:
            call.function_name = (
                function_transformations.get("name") or call.function_name
            )
        else:
            function_transformations = dict()

        # prepare context for transformations
        context = create_transformation_context(
            call.to_address.address,
            call.arguments,
            call.outputs,
            tx_metadata,
            self.repository,
        )
        standard = self.repository.get_standard(call.chain_id, call.to_address.address)

        # perform parameters transformations
        for i, parameter in enumerate(call.arguments):
            semantically_decode_parameter(
                self.repository,
                parameter,
                f"__input{i}__",
                function_transformations,
                token_proxies,
                context,
            )
        for i, parameter in enumerate(call.outputs):
            semantically_decode_parameter(
                self.repository,
                parameter,
                f"__output{i}__",
                function_transformations,
                token_proxies,
                context,
            )

        if standard == "ERC20":
            # decode ERC20 calls if transformations for them are not defined
            if call.function_signature in ERC20_FUNCTIONS and (
                not function_transformations
                or call.function_signature not in function_transformations
            ):
                function_transformations = ERC20_TRANSFORMATIONS.get(
                    call.function_signature
                )
                if function_transformations:
                    for i, parameter in enumerate(call.arguments):
                        semantically_decode_parameter(
                            self.repository,
                            parameter,
                            f"__input{i}__",
                            function_transformations,
                            token_proxies,
                            context,
                        )
                    for i, parameter in enumerate(call.outputs):
                        semantically_decode_parameter(
                            self.repository,
                            parameter,
                            f"__output{i}__",
                            function_transformations,
                            token_proxies,
                            context,
                        )
        elif standard == "ERC721":
            # decode ERC721 calls if transformations for them are not defined
            if call.function_signature in ERC721_FUNCTIONS and (
                not function_transformations
                or call.function_signature not in function_transformations
            ):
                function_transformations = ERC721_TRANSFORMATIONS.get(
                    call.function_signature
                )
                if function_transformations:
                    for i, parameter in enumerate(call.arguments):
                        semantically_decode_parameter(
                            self.repository,
                            parameter,
                            f"__input{i}__",
                            function_transformations,
                            token_proxies,
                            context,
                        )
                    for i, parameter in enumerate(call.outputs):
                        semantically_decode_parameter(
                            self.repository,
                            parameter,
                            f"__output{i}__",
                            function_transformations,
                            token_proxies,
                            context,
                        )

        # decode proper from and to addresses badges
        call.from_address.badge = get_badge(
            call.from_address.address, tx_metadata.sender, tx_metadata.receiver
        )
        call.to_address.badge = get_badge(
            call.to_address.address, tx_metadata.sender, tx_metadata.receiver
        )

        # remove ignored parameters
        call.arguments = [
            parameter for parameter in call.arguments if parameter.type != "ignore"
        ]
        call.outputs = [
            parameter for parameter in call.outputs if parameter.type != "ignore"
        ]

        with RecursionLimit(RECURSION_LIMIT):
            if call.subcalls:
                for sub_call in call.subcalls:
                    self.decode(sub_call, tx_metadata, token_proxies)

        return call
