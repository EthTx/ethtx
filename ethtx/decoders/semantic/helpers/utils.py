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

import json
import logging
import time
from functools import partial
from typing import Optional

import requests

from ethtx.decoders.decoders.parameters import decode_function_parameters
from ethtx.models.decoded_model import AddressInfo
from ethtx.semantics.utilities.functions import add_utils_to_context
from ethtx.models.semantics_model import FunctionSemantics

log = logging.getLogger(__name__)

eth_price: Optional[float] = None
eth_price_update: Optional[float] = None


def get_eth_price() -> Optional[float]:
    global eth_price, eth_price_update

    current_time = time.time()
    if (
        eth_price is None
        or eth_price_update is None
        or (current_time - eth_price_update) > 60
    ):
        response = requests.get("https://api.coinbase.com/v2/prices/ETH-USD/buy")
        if response.status_code == 200:
            eth_price = float(json.loads(response.content)["data"]["amount"])
            eth_price_update = time.time()

    return eth_price


def get_badge(address, sender, receiver):

    sender_address = sender.address if isinstance(sender, AddressInfo) else sender
    receiver_address = (
        receiver.address if isinstance(receiver, AddressInfo) else receiver
    )

    if address == sender_address:
        badge = "sender"
    elif address == receiver_address:
        badge = "receiver"
    else:
        badge = None

    return badge


def semantically_decode_parameter(
    repository, parameter, indexed_name, transformations, proxies, context
):
    if parameter.name in transformations:
        transformation = transformations[parameter.name]
    elif indexed_name in transformations:
        transformation = transformations[indexed_name]
    else:
        transformation = None

    if transformation:
        parameter.name = transformation.transformed_name or parameter.name
        parameter.type = transformation.transformed_type or parameter.type

        if transformation.transformation:
            parameter.value = (
                evaluate_transformation(
                    parameter.value, transformation.transformation, context
                )
                or parameter.value
            )

    if parameter.type == "address" and not isinstance(parameter.value, AddressInfo):
        address = parameter.value
        name = repository.get_address_label(
            context["__transaction__"].chain_id, address, proxies
        )
        badge = get_badge(
            address,
            context["__transaction__"].sender,
            context["__transaction__"].receiver,
        )
        parameter.value = AddressInfo(address, name, badge)
    elif parameter.type == "bytes" and isinstance(parameter.value, str):
        if len(parameter.value) > 66:
            parameter.value = parameter.value[:60] + "..." + parameter.value[-6:]
    elif parameter.type == "tuple" and isinstance(parameter.value, list):
        for i, sub_parameter in enumerate(parameter.value):
            semantically_decode_parameter(
                repository,
                sub_parameter,
                f"__input{i}__",
                transformations,
                proxies,
                context,
            )


def evaluate_transformation(value, transformation, context):
    try:
        new_value = eval(transformation, context)
    except Exception as e:
        log.warning("Transformation: %s failed.", transformation, exc_info=e)
        new_value = value

    return new_value


def decode_call(transaction, repository, contract_address, data):
    if not data or len(data) <= 2:
        return None

    function_signature = data[:10]

    contract_name = repository.get_address_label(transaction.chain_id, contract_address)
    contract_badge = get_badge(
        contract_address, transaction.sender, transaction.receiver
    )
    contract = AddressInfo(contract_address, contract_name, contract_badge)

    if repository.check_is_contract(transaction.chain_id, contract_address):

        # read function ABI and semantics and use them for decoding
        function_abi = repository.get_function_abi(
            transaction.chain_id, contract_address, function_signature
        )
        function_transformations = repository.get_transformations(
            transaction.chain_id, contract_address, function_signature
        )
        function_name = function_abi.name if function_abi else function_signature
        stripped_function_abi = FunctionSemantics(signature=function_abi.signature, name=function_abi.name,
                                                  inputs=function_abi.inputs, outputs=[])
        function_input, _ = decode_function_parameters(data, "0x", stripped_function_abi)

        # perform arguments transformations
        context = create_transformation_context(
            contract.address, function_input, [], transaction, repository
        )
        for i, argument in enumerate(function_input):
            semantically_decode_parameter(
                repository,
                argument,
                f"__input{i}__",
                function_transformations or dict(),
                None,
                context,
            )

        decoded_argument = dict(
            contract=contract, function_name=function_name, arguments=function_input
        )
    else:
        decoded_argument = dict(
            contract=contract,
            function_name=function_signature,
            arguments="0x" + data[10:],
        )

    return decoded_argument


def create_transformation_context(
    contract, input_variables, output_variables, transaction, repository
):
    # create a context for transformations
    context = dict()
    for i, parameter in enumerate(input_variables):
        if parameter.name:
            context[parameter.name] = parameter.value
        context[f"__input{i}__"] = parameter.value

    for i, parameter in enumerate(output_variables):
        if parameter.name:
            context[parameter.name] = parameter.value
        context[f"__output{i}__"] = parameter.value

    # register context variables
    context["__transaction__"] = transaction
    context["__contract__"] = contract
    context["__repository__"] = repository

    # register additional functions available for transformations
    context["decode_call"] = partial(
        decode_call, context["__transaction__"], context["__repository__"]
    )
    add_utils_to_context(context)

    # ToDo: remove compatibility hooks
    # compatibility hooks
    context["_transaction"] = transaction
    context["_contract"] = contract
    context["network"] = transaction.chain_id
    context["_print_input"] = decode_call
    context["__print_input__"] = decode_call

    return context
