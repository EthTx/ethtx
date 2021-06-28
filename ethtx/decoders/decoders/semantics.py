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
                raw_parameter_semantics["name"],
                raw_parameter_semantics["type"],
                components,
                indexed,
                dynamic,
            )
        )
    return parameters_list


def decode_events_and_functions(
    abi: dict,
) -> Tuple[Dict[str, EventSemantics], Dict[str, FunctionSemantics]]:
    events = dict()
    for signature, raw_event_semantics in abi.get("events", {}).items():
        parameters = _decode_parameters_list(raw_event_semantics.get("parameters"))
        events[signature] = EventSemantics(
            signature,
            raw_event_semantics["anonymous"],
            raw_event_semantics["name"],
            parameters,
        )

    functions = dict()
    for signature, raw_function_semantics in abi.get("functions", {}).items():
        if raw_function_semantics:
            inputs = _decode_parameters_list(raw_function_semantics.get("inputs"))
            outputs = _decode_parameters_list(raw_function_semantics.get("outputs"))
            name = raw_function_semantics["name"]
        else:
            inputs = outputs = []
            name = signature

        functions[signature] = FunctionSemantics(signature, name, inputs, outputs)

    return events, functions


def decode_transformations(
    raw_transformations: dict,
) -> Dict[str, Dict[str, TransformationSemantics]]:
    transformations = dict()
    if raw_transformations:
        for signature, transformation in raw_transformations.items():
            transformations[signature] = dict()
            for parameter_name, parameter_transformation in transformation.get(
                "arguments", dict()
            ).items():
                transformations[signature][parameter_name] = TransformationSemantics(
                    parameter_transformation.get("name"),
                    parameter_transformation.get("type"),
                    parameter_transformation.get("value"),
                )
    return transformations
