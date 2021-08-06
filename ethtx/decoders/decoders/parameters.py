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
from datetime import datetime

from ethtx.models.decoded_model import Argument
from ethtx.models.semantics_model import ParameterSemantics

log = logging.getLogger(__name__)


def decode_event_parameters(data, topics, abi, anonymous):

    # making copy to avoid modifying of the original list
    amended_topics = topics.copy()

    # for anonymous events shift the list of topics
    if anonymous:
        amended_topics.insert(0, None)

    parameters_abi = abi.parameters if abi else []

    topic_parameters = {}
    data_parameters = {}
    idx_parameters = []
    data = data[2:]

    if parameters_abi:

        idx_parameters = [p.indexed or False for p in parameters_abi]

        # parse indexed parameters
        for i, parameter in enumerate([p for p in parameters_abi if p.indexed]):
            parameter_name = parameter.parameter_name
            parameter_type = parameter.parameter_type
            # assumption that topic parameters can be only static
            if len(amended_topics) > i + 1:
                raw_parameter = (
                    amended_topics[i + 1]
                    if isinstance(amended_topics[i + 1], str)
                    else amended_topics[i + 1].hex()
                )
                if not parameter_type:
                    parameter_value = raw_parameter
                    parameter_type = "unknown"
                else:
                    parameter_value = decode_static_argument(
                        raw_parameter, parameter_type
                    )
                topic_parameters[i] = Argument(
                    parameter_name, parameter_type, parameter_value
                )
            else:
                log.warning("Topics length mismatch.")
                return []

        # parse other (not indexed) parameters
        if len(data):
            parameters, _ = decode_struct(
                data, [p for p in parameters_abi if not p.indexed]
            )
            for (i, parameter) in enumerate(parameters):
                data_parameters[i] = Argument(**parameter)

    else:

        for i, parameter in enumerate(amended_topics[1:]):
            if not amended_topics[i + 1]:
                break
            parameter_name = ""
            parameter_type = "unknown"
            parameter_value = (
                amended_topics[i + 1]
                if isinstance(amended_topics[i + 1], str)
                else amended_topics[i + 1].hex()
            )

            topic_parameters[i] = Argument(
                parameter_name, parameter_type, parameter_value
            )

        no_parameters = len(data) // 64
        for i in range(no_parameters):
            parameter_name = ""
            parameter_type = "unknown"
            parameter_value = data[64 * i : 64 * (i + 1)]

            data_parameters[i] = Argument(
                parameter_name, parameter_type, parameter_value
            )

    # store parameters in original ABI order
    event_parameters = []
    if parameters_abi:
        ni = nd = 0
        for i in range(len(parameters_abi)):
            if idx_parameters[i]:
                if len(topic_parameters) > ni:
                    event_parameters.append(topic_parameters[ni])
                    ni += 1
            else:
                if len(data_parameters) > nd:
                    event_parameters.append(data_parameters[nd])
                    nd += 1
    else:
        for _, parameter in topic_parameters.items():
            event_parameters.append(parameter)
        for _, parameter in data_parameters.items():
            event_parameters.append(parameter)

    return event_parameters


def decode_function_parameters(input_data, output, abi, status=True, strip_signature=True):

    if strip_signature and len(input_data) >= 10:
        stripped_input_data = input_data[10:]
    else:
        stripped_input_data = input_data[2:]

    if abi:
        if len(abi.inputs) == 1 and abi.inputs[0].parameter_type == 'raw':
            input_parameters = [Argument(name=abi.inputs[0].parameter_name, type='bytes', value=input_data)]
        else:
            input_parameters, _ = decode_struct(stripped_input_data, abi.inputs)
            for i, parameter in enumerate(input_parameters):
                input_parameters[i] = Argument(**parameter)
    elif stripped_input_data:
        input_parameters = [
            Argument(name="call_data", type="bytes", value="0x" + stripped_input_data)
        ]
    else:
        input_parameters = []

    if not status and output[:10] == "0x08c379a0":
        error_abi = ParameterSemantics("Error", "string", [], False, True)
        error_parameters, _ = decode_struct(output[10:], [error_abi])
        output_parameters = [Argument(**error_parameters[0])]
    else:
        if abi:
            if abi.outputs and status and output == "0x":
                log.warning("Warning: missing output data...")
                output_parameters = []
            elif output != '0x':
                if len(abi.outputs) == 1 and abi.outputs[0].parameter_type == 'raw':
                    output_parameters = [Argument(name=abi.outputs[0].parameter_name, type='bytes', value=output)]
                else:
                    output_parameters, _ = decode_struct(output[2:], abi.outputs)
                    for i, parameter in enumerate(output_parameters):
                        output_parameters[i] = Argument(**parameter)
            else:
                output_parameters = []
        elif output != "0x":
            output_parameters = [
                Argument(name="output_data", type="bytes", value=output)
            ]
        else:
            output_parameters = []

    return input_parameters, output_parameters


# helper function to decode an argument value based on expected type
def decode_static_argument(raw_value, argument_type):
    decoded_value = raw_value

    if decoded_value:

        if argument_type == "address":
            if len(raw_value) >= 40:
                decoded_value = "0x" + raw_value[-40:]
            else:
                decoded_value = raw_value

        elif argument_type[:4] == "uint":
            if isinstance(raw_value, str):
                decoded_value = int(raw_value, 16)
            else:
                decoded_value = raw_value

        elif argument_type[:3] == "int":
            if isinstance(raw_value, str):
                decoded_value = int(raw_value, 16)
                if decoded_value & (1 << (256 - 1)):
                    decoded_value -= 1 << 256
            else:
                decoded_value = raw_value

        elif argument_type == "bool":
            if int(raw_value, 16) == 0:
                decoded_value = "False"
            else:
                decoded_value = "True"

        elif argument_type == "bytes":
            decoded_value = "0x" + bytes.fromhex(raw_value[2:]).hex()

        elif argument_type[:5] == "bytes":
            decoded_value = "0x" + raw_value

        elif argument_type == "byte":
            decoded_value = "0x" + bytes.fromhex(raw_value[2:])[0].hex()

        elif argument_type in ("string", "string32"):
            try:
                if raw_value[:2] == "0x":
                    raw_value = raw_value[2:]
                decoded_value = (
                    bytes.fromhex(raw_value).decode("utf-8").replace("\x00", "")
                )
            except Exception:
                pass

        elif argument_type == "timestamp":
            if isinstance(raw_value, str):
                decoded_value = str(datetime.utcfromtimestamp(int(raw_value, 16)))
            else:
                decoded_value = str(datetime.utcfromtimestamp(raw_value))

        elif argument_type == "hashmap":
            decoded_value = "[...]"
        elif argument_type == "tuple":
            decoded_value = "(...)"
        elif argument_type == "tuple[]":
            decoded_value = "(...)[]"

    return decoded_value


# helper function to decode ABI 2.0
def decode_tuple(data, argument_abi, is_list):
    slots = 0

    if is_list:
        count = int(data[:64], 16)
        data = data[64:]
        decoded_argument = []

        for c in range(count):
            do_offset = any(a.dynamic for a in argument_abi)
            if do_offset:
                raw_value = data[c * 64 : (c + 1) * 64]
                offset = int(raw_value, 16) * 2
                sub_bytes = data[offset:]
            else:
                sub_bytes = data

            decoded, num = decode_struct(sub_bytes, argument_abi)
            for i, parameter in enumerate(decoded):
                decoded[i] = Argument(**parameter)
            decoded_argument.append(decoded)
            slots += num

    else:
        decoded_argument, num = decode_struct(data, argument_abi)
        for i, parameter in enumerate(decoded_argument):
            decoded_argument[i] = Argument(**parameter)
        slots += num

    return decoded_argument, slots


# helper function to decode dynamic arrays
def decode_dynamic_array(data, array_type):
    count = int(data[:64], 16)
    sub_data = data[64:]
    decoded_argument = []

    for i in range(count):
        if array_type in ("bytes", "string"):
            offset = int(sub_data[64 * i: 64 * (i + 1)], 16) * 2
            decoded = decode_dynamic_argument(sub_data[offset:], array_type)
        else:
            offset = 64 * i
            decoded = decode_static_argument(sub_data[offset: offset+64], array_type)

        decoded_argument.append(decoded)

    return decoded_argument


# helper function to decode a dynamic argument
def decode_dynamic_argument(argument_bytes, argument_type):
    if len(argument_bytes):
        length = int(argument_bytes[:64], 16) * 2
        value = argument_bytes[64 : 64 + length]

        if argument_type == "string":
            decoded_value = (
                bytes.fromhex(value).decode("utf-8").replace("\x00", "")
            )
        else:
            decoded_value = "0x" + value
    else:
        decoded_value = bytes(0).decode()

    return decoded_value


# helper function to decode ABI 2.0 structs
def decode_struct(data, arguments_abi):
    if arguments_abi:
        no_arguments = len(arguments_abi)
    else:
        no_arguments = len(data) // 64 + 1

    arguments_list = []
    slot = 0
    for i in range(no_arguments):
        raw_value = data[slot * 64 : (slot + 1) * 64]

        if arguments_abi:

            argument_name = arguments_abi[i].parameter_name
            argument_type = arguments_abi[i].parameter_type

            if argument_type[:5] == "tuple":
                do_offset = arguments_abi[i].dynamic or any(
                    a.dynamic for a in arguments_abi[i].components
                )
                if do_offset:
                    offset = int(raw_value, 16) * 2
                    sub_arguments = data[offset:]
                else:
                    sub_arguments = data[i * 64 :]

                argument_value, slots = decode_tuple(
                    sub_arguments,
                    arguments_abi[i].components,
                    argument_type[5:] == "[]",
                )

                if do_offset:
                    slot += 1
                else:
                    slot += slots

            elif argument_type in ("bytes", "string"):
                offset = int(raw_value, 16) * 2
                argument_value = decode_dynamic_argument(data[offset:], argument_type)
                slot += 1

            elif argument_type[-1:] == "]":
                array_type = argument_type[:-1].split("[")[0]

                if argument_type[-2:] == "[]":
                    offset = int(raw_value, 16) * 2
                    argument_value = decode_dynamic_array(data[offset:], array_type)
                    slot += 1
                else:
                    array_size = int(argument_type[:-1].split("[")[1])
                    argument_value = []
                    for _ in range(array_size):
                        argument_value.append(
                            decode_static_argument(raw_value, array_type)
                        )
                        slot += 1
                        raw_value = data[slot * 64 : (slot + 1) * 64]

            else:
                argument_value = decode_static_argument(raw_value, argument_type)
                slot += 1
        else:
            argument_name = "arg_%d" % (i + 1)
            argument_type = "unknown"
            argument_value = "0x" + raw_value

        if argument_type != "unknown" or argument_value != "0x":
            arguments_list.append(
                dict(name=argument_name, type=argument_type, value=argument_value)
            )

    return arguments_list, slot


def decode_graffiti_parameters(input_data):
    input_parameters = []

    if input_data and len(input_data) > 2:
        try:
            message = bytearray.fromhex(input_data[2:]).decode()
            input_parameters = [Argument(name="message", type="string", value=message)]
        except Exception as e:
            # log.warning(e)
            pass

    return input_parameters
