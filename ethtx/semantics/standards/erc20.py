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

from ethtx.models.semantics_model import (
    EventSemantics,
    ParameterSemantics,
    TransformationSemantics,
    FunctionSemantics,
)

erc20_transfer_event = EventSemantics(
    "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
    False,
    "Transfer",
    [
        ParameterSemantics("src", "address", [], True),
        ParameterSemantics("dst", "address", [], True),
        ParameterSemantics("value", "uint256", [], False),
    ],
)

erc20_transfer_event_transformation = {
    "__input2__": TransformationSemantics(
        transformation="__input2__ / 10**token_decimals(__contract__)"
    )
}

erc20_approval_event = EventSemantics(
    "0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925",
    False,
    "Approval",
    [
        ParameterSemantics("src", "address", [], True),
        ParameterSemantics("dst", "address", [], True),
        ParameterSemantics("value", "uint256", [], False),
    ],
)

erc20_approval_event_transformation = {
    "__input2__": TransformationSemantics(
        transformation="__input2__ / 10**token_decimals(__contract__)"
    )
}

erc20_transfer_function = FunctionSemantics(
    "0xa9059cbb",
    "transfer",
    [
        ParameterSemantics("recipient", "address", []),
        ParameterSemantics("amount", "uint256", []),
    ],
    [ParameterSemantics("", "bool", [])],
)

erc20_transfer_function_transformation = {
    "__input1__": TransformationSemantics(
        transformation="__input1__ / 10**token_decimals(__contract__)"
    )
}

erc20_transferFrom_function = FunctionSemantics(
    "0x23b872dd",
    "transferFrom",
    [
        ParameterSemantics("sender", "address", []),
        ParameterSemantics("recipient", "address", []),
        ParameterSemantics("amount", "uint256", []),
    ],
    [ParameterSemantics("", "bool", [])],
)

erc20_transferFrom_function_transformation = {
    "__input2__": TransformationSemantics(
        transformation="__input2__ / 10**token_decimals(__contract__)"
    )
}

erc20_approve_function = FunctionSemantics(
    "0x095ea7b3",
    "approve",
    [
        ParameterSemantics("spender", "address", []),
        ParameterSemantics("amount", "uint256", []),
    ],
    [ParameterSemantics("", "bool", [])],
)

erc20_approve_function_transformation = {
    "__input1__": TransformationSemantics(
        transformation="__input1__ / 10**token_decimals(__contract__)"
    )
}

erc20_balanceOf_function = FunctionSemantics(
    "0x70a08231",
    "balanceOf",
    [ParameterSemantics("holder", "address", [])],
    [ParameterSemantics("", "uint256", [])],
)

erc20_balanceOf_function_transformation = {
    "__output0__": TransformationSemantics(
        transformation="__output0__ / 10**token_decimals(__contract__)"
    )
}

erc20_totalSupply_function = FunctionSemantics(
    "0x18160ddd", "totalSupply", [], [ParameterSemantics("", "uint256", [])]
)

erc20_totalSupply_function_transformation = {
    "__output0__": TransformationSemantics(
        transformation="__output0__ / 10**token_decimals(__contract__)"
    )
}

ERC20_EVENTS = {
    erc20_transfer_event.signature: erc20_transfer_event,
    erc20_approval_event.signature: erc20_approval_event,
}

ERC20_FUNCTIONS = {
    erc20_transfer_function.signature: erc20_transfer_function,
    erc20_transferFrom_function.signature: erc20_transferFrom_function,
    erc20_approve_function.signature: erc20_approve_function,
    erc20_balanceOf_function.signature: erc20_balanceOf_function,
    erc20_totalSupply_function.signature: erc20_totalSupply_function,
}

ERC20_TRANSFORMATIONS = {
    erc20_transfer_event.signature: erc20_transfer_event_transformation,
    erc20_approval_event.signature: erc20_approval_event_transformation,
    erc20_transfer_function.signature: erc20_transfer_function_transformation,
    erc20_transferFrom_function.signature: erc20_transferFrom_function_transformation,
    erc20_approve_function.signature: erc20_approve_function_transformation,
    erc20_balanceOf_function.signature: erc20_balanceOf_function_transformation,
    erc20_totalSupply_function.signature: erc20_totalSupply_function_transformation,
}
