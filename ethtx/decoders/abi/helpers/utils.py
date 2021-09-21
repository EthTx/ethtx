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
from typing import Iterator, Optional

from ethtx.models.semantics_model import FunctionSemantics, ParameterSemantics
from ethtx.providers import FourByteProvider
from ethtx.providers.signature_provider import SignatureProvider


def decode_function_abi_with_provider(
    signature: str, _provider: Optional[SignatureProvider] = FourByteProvider
) -> Iterator[FunctionSemantics]:
    functions = _provider.get_function(signature=signature)
    for func in functions:
        if not func:
            yield

        yield FunctionSemantics(
            signature,
            func.get("name"),
            [
                ParameterSemantics(f"arg{i}", arg, [])
                for i, arg in enumerate(func.get("args"))
            ],
            [],
        )


def decode_event_abi_name_with_provider(
    signature: str, _provider: Optional[SignatureProvider] = FourByteProvider
) -> str:
    events = _provider.get_event(signature=signature)

    for event in events:
        if not event:
            yield

        yield event.get("name")
