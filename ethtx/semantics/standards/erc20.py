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
    signature="0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
    anonymous=False,
    name="Transfer",
    parameters=[
        ParameterSemantics(
            parameter_name="src", parameter_type="address", indexed=True
        ),
        ParameterSemantics(
            parameter_name="dst", parameter_type="address", indexed=True
        ),
        ParameterSemantics(
            parameter_name="value", parameter_type="uint256", indexed=False
        ),
    ],
)

erc20_transfer_event_transformation = {
    "__input2__": TransformationSemantics(
        transformation="__input2__ / 10**token_decimals(__contract__)"
    )
}

erc20_approval_event = EventSemantics(
    signature="0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925",
    anonymous=False,
    name="Approval",
    parameters=[
        ParameterSemantics(
            parameter_name="src", parameter_type="address", indexed=True
        ),
        ParameterSemantics(
            parameter_name="dst", parameter_type="address", indexed=True
        ),
        ParameterSemantics(
            parameter_name="value", parameter_type="uint256", indexed=False
        ),
    ],
)

erc20_approval_event_transformation = {
    "__input2__": TransformationSemantics(
        transformation="__input2__ / 10**token_decimals(__contract__)"
    )
}

erc20_transfer_function = FunctionSemantics(
    signature="0xa9059cbb",
    name="transfer",
    inputs=[
        ParameterSemantics(parameter_name="recipient", parameter_type="address"),
        ParameterSemantics(parameter_name="amount", parameter_type="uint256"),
    ],
    outputs=[ParameterSemantics(parameter_name="", parameter_type="bool")],
)

erc20_transfer_function_transformation = {
    "__input1__": TransformationSemantics(
        transformation="__input1__ / 10**token_decimals(__contract__)"
    )
}

erc20_transferFrom_function = FunctionSemantics(
    signature="0x23b872dd",
    name="transferFrom",
    inputs=[
        ParameterSemantics(parameter_name="sender", parameter_type="address"),
        ParameterSemantics(parameter_name="recipient", parameter_type="address"),
        ParameterSemantics(parameter_name="amount", parameter_type="uint256"),
    ],
    outputs=[ParameterSemantics(parameter_name="", parameter_type="bool")],
)

erc20_transferFrom_function_transformation = {
    "__input2__": TransformationSemantics(
        transformation="__input2__ / 10**token_decimals(__contract__)"
    )
}

erc20_approve_function = FunctionSemantics(
    signature="0x095ea7b3",
    name="approve",
    inputs=[
        ParameterSemantics(parameter_name="spender", parameter_type="address"),
        ParameterSemantics(parameter_name="amount", parameter_type="uint256"),
    ],
    outputs=[ParameterSemantics(parameter_name="", parameter_type="bool")],
)

erc20_approve_function_transformation = {
    "__input1__": TransformationSemantics(
        transformation="__input1__ / 10**token_decimals(__contract__)"
    )
}

erc20_balanceOf_function = FunctionSemantics(
    signature="0x70a08231",
    name="balanceOf",
    inputs=[ParameterSemantics(parameter_name="holder", parameter_type="address")],
    outputs=[ParameterSemantics(parameter_name="", parameter_type="uint256")],
)

erc20_balanceOf_function_transformation = {
    "__output0__": TransformationSemantics(
        transformation="__output0__ / 10**token_decimals(__contract__)"
    )
}

erc20_totalSupply_function = FunctionSemantics(
    signature="0x18160ddd",
    name="totalSupply",
    inputs=[],
    outputs=[ParameterSemantics(parameter_name="", parameter_type="uint256")],
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
