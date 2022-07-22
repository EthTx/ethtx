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

import logging
from typing import Optional, List, Tuple

from ethtx.models.semantics_model import (
    FunctionSemantics,
    ParameterSemantics,
    Signature,
    SignatureArg,
)
from ethtx.providers.semantic_providers import SemanticsRepository
from ethtx.providers.signature_provider import SignatureProvider, FourByteProvider

log = logging.getLogger(__name__)


def decode_function_abi_with_repository(
    signature: str, repository: SemanticsRepository
) -> Tuple[bool, Optional[FunctionSemantics]]:
    signature_obj = repository.get_most_used_signature(signature_hash=signature)
    if signature_obj:
        log.info(
            "Function (signature: %s, name: %s) guessed from SemanticsRepository.",
            signature_obj.signature_hash,
            signature_obj.name,
        )
        function_semantics = FunctionSemantics(
            signature=signature,
            name=signature_obj.name,
            inputs=_prepare_parameter_semantics(
                signature_obj.args, signature_obj.tuple, unknown=False
            ),
        )

        return signature_obj.guessed, function_semantics

    return False, None


def decode_function_abi_with_external_source(
    signature: str,
    _provider: Optional[SignatureProvider] = FourByteProvider,
) -> List[Optional[Tuple[bool, FunctionSemantics]]]:
    functions = _provider.get_function(signature=signature)

    return [
        (
            True,
            FunctionSemantics(
                signature=signature,
                name=func.get("name"),
                inputs=_prepare_parameter_semantics(
                    func.get("args"),
                    isinstance(func.get("args"), tuple),
                    unknown=True,
                ),
            ),
        )
        for func in functions
        if func
    ]


def upsert_guessed_function_semantics(
    signature: str,
    function_semantics: FunctionSemantics,
    repository: SemanticsRepository,
) -> None:
    log.info(
        "Function (signature: %s, name: %s) guessed from external source.",
        signature,
        function_semantics.name,
    )

    repository.update_or_insert_signature(
        signature=Signature(
            signature_hash=signature,
            name=function_semantics.name,
            args=[
                SignatureArg(name=f"arg_{i}", type=arg.parameter_type)
                for i, arg in enumerate(function_semantics.inputs)
            ],
            tuple=isinstance(function_semantics.inputs, tuple),
            guessed=True,
        )
    )


def decode_event_abi_name_with_external_source(
    signature: str, _provider: Optional[SignatureProvider] = FourByteProvider
) -> Tuple[bool, str]:
    events = _provider.get_event(signature=signature)

    for event in events:

        if not event:
            return False, signature

        event_name = event.get("name")
        if event_name:
            log.info(
                "Event (signature: %s, name: %s) guessed from external source.",
                signature,
                event_name,
            )
            return True, event.get("name", signature)

    return False, signature


def _prepare_parameter_semantics(
    args, is_tuple: bool, unknown: bool
) -> List[ParameterSemantics]:
    if not args:
        return []

    elif not is_tuple:
        return [
            ParameterSemantics(
                parameter_name=arg.name if not unknown else f"arg_{i}",
                parameter_type=arg.type if not unknown else arg,
            )
            for i, arg in enumerate(args)
        ]

    return [
        ParameterSemantics(
            parameter_name="params",
            parameter_type="tuple",
            components=[
                ParameterSemantics(
                    parameter_name=arg.name if not unknown else f"arg_{i}",
                    parameter_type=arg.type if not unknown else arg,
                )
                for i, arg in enumerate(args)
            ],
        )
    ]
