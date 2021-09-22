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
from typing import Iterator, Optional

from ethtx.models.semantics_model import (
    FunctionSemantics,
    ParameterSemantics,
    Signature,
    SignatureArg,
)
from ethtx.providers import FourByteProvider
from ethtx.providers.semantic_providers.semantics_repository import SemanticsRepository
from ethtx.providers.signature_provider import SignatureProvider

log = logging.getLogger(__name__)


def decode_function_abi_with_external_source(
    signature: str,
    repository: SemanticsRepository,
    _provider: Optional[SignatureProvider] = FourByteProvider,
) -> Iterator[FunctionSemantics]:
    function = repository.get_most_common_signature(signature_hash=signature)
    if function:
        log.info(
            "Successfully guessed function from SemanticsRepository - %s.",
            function.json(),
        )
        function_semantics = FunctionSemantics(
            signature,
            function.name,
            [ParameterSemantics(arg["name"], arg["type"], []) for arg in function.args],
            [],
        )
        yield function_semantics

    functions = _provider.get_function(signature=signature)
    for func in functions:

        if not func:
            yield

        function_semantics = FunctionSemantics(
            signature,
            func.get("name"),
            [
                ParameterSemantics(f"arg{i}", arg, [])
                for i, arg in enumerate(func.get("args"))
            ],
            [],
        )

        repository.process_signatures(
            signature=Signature(
                signature_hash=signature,
                name=func.get("name"),
                args=[
                    SignatureArg(name=param.parameter_name, type=param.parameter_type)
                    for param in function_semantics.inputs
                ],
            )
        )
        yield function_semantics


def decode_event_abi_name_with_external_source(
    signature: str, _provider: Optional[SignatureProvider] = FourByteProvider
) -> str:
    events = _provider.get_event(signature=signature)

    for event in events:

        if not event:
            return signature

        return event.get("name", signature)

    return signature
