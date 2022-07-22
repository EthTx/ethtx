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

from typing import List, Dict, Tuple

from ethtx.models.semantics_model import (
    ParameterSemantics,
    EventSemantics,
    FunctionSemantics,
    TransformationSemantics,
)


def _decode_parameters_list(raw_parameters_list: list) -> List[ParameterSemantics]:
    parameters_list = []

    if not raw_parameters_list:
        return parameters_list

    for raw_parameter_semantics in raw_parameters_list:

        if "indexed" in raw_parameter_semantics:
            indexed = raw_parameter_semantics["indexed"]
        else:
            indexed = False

        if "dynamic" in raw_parameter_semantics:
            dynamic = raw_parameter_semantics["dynamic"]
        else:
            dynamic = False

        if raw_parameter_semantics["type"] == "tuple":
            components = _decode_parameters_list(raw_parameter_semantics["components"])
        else:
            components = []

        parameters_list.append(
            ParameterSemantics(
                parameter_name=raw_parameter_semantics["name"],
                parameter_type=raw_parameter_semantics["type"],
                components=components,
                indexed=indexed,
                dynamic=dynamic,
            )
        )
    return parameters_list


def decode_events_and_functions(
    abi: dict,
) -> Tuple[Dict[str, EventSemantics], Dict[str, FunctionSemantics]]:
    events = {}
    for signature, raw_event_semantics in abi.get("events", {}).items():
        parameters = _decode_parameters_list(raw_event_semantics.get("parameters"))
        events[signature] = EventSemantics(
            signature=signature,
            anonymous=raw_event_semantics["anonymous"],
            name=raw_event_semantics["name"],
            parameters=parameters,
        )

    functions = {}
    for signature, raw_function_semantics in abi.get("functions", {}).items():
        if raw_function_semantics:
            inputs = _decode_parameters_list(raw_function_semantics.get("inputs"))
            outputs = _decode_parameters_list(raw_function_semantics.get("outputs"))
            name = raw_function_semantics["name"]
        else:
            inputs = outputs = []
            name = signature

        functions[signature] = FunctionSemantics(
            signature=signature, name=name, inputs=inputs, outputs=outputs
        )

    return events, functions


def decode_transformations(
    raw_transformations: dict,
) -> Dict[str, Dict[str, TransformationSemantics]]:
    transformations = {}
    if raw_transformations:
        for signature, transformation in raw_transformations.items():
            transformations[signature] = {}
            for parameter_name, parameter_transformation in transformation.get(
                "arguments", {}
            ).items():
                transformations[signature][parameter_name] = TransformationSemantics(
                    transformed_name=parameter_transformation.get("name"),
                    transformed_type=parameter_transformation.get("type"),
                    transformation=parameter_transformation.get("value"),
                )
    return transformations
