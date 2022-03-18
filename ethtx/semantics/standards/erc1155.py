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

from inspect import Parameter
from ethtx.models.semantics_model import (
    EventSemantics,
    FunctionSemantics,
    ParameterSemantics,
    TransformationSemantics,
)

erc1155_transferSingle_event = EventSemantics(
    signature="0xc3d58168c5ae7397731d063d5bbf3d657854427343f4c083240f7aacaa2d0f62",
    anonymous=False,
    name="TransferSingle",
    parameters=[
        ParameterSemantics(
            parameter_name="operator", parameter_type="address", components=[], indexed=True
        ),
        ParameterSemantics(
            parameter_name="from", parameter_type="address", components=[], indexed=True
        ),
        ParameterSemantics(
            parameter_name="to", parameter_type="address", components=[], indexed=True
        ),
        ParameterSemantics(
            parameter_name="id",
            parameter_type="uint256",
            components=[],
            indexed=False,
        ),
        ParameterSemantics(
            parameter_name="value",
            parameter_type="uint256",
            components=[],
            indexed=False,
        ),
    ],
)

erc1155_transferSingle_event_transformation = {
    "__input3__": TransformationSemantics(
        transformed_type="nft", transformation="decode_nft(__input3__)"
    )
}

erc1155_transferBatch_event = EventSemantics(
    signature="0x4a39dc06d4c0dbc64b70af90fd698a233a518aa5d07e595d983b8c0526c8f7fb",
    anonymous=False,
    name="TransferBatch",
    parameters=[
        ParameterSemantics(
            parameter_name="operator", parameter_type="address", components=[], indexed=True
        ),
        ParameterSemantics(
            parameter_name="from", parameter_type="address", components=[], indexed=True
        ),
        ParameterSemantics(
            parameter_name="to", parameter_type="address", components=[], indexed=True
        ),
        ParameterSemantics(
            parameter_name="ids",
            parameter_type="uint256[]",
            components=[],
            indexed=False,
        ),
        ParameterSemantics(
            parameter_name="values",
            parameter_type="uint256[]",
            components=[],
            indexed=False,
        ),
    ],
)

erc1155_transferBatch_event_transformation = {
    "__input3__": TransformationSemantics(
        transformed_type="nft", transformation="decode_nft(__input3__)"
    )
}

erc1155_approvalForAll_event = EventSemantics(
    signature="0x17307eab39ab6107e8899845ad3d59bd9653f200f220920489ca2b5937696c31",
    anonymous=False,
    name="ApprovalForAll",
    parameters=[
        ParameterSemantics(
            parameter_name="owner",
            parameter_type="address",
            components=[],
            indexed=True,
        ),
        ParameterSemantics(
            parameter_name="operator",
            parameter_type="address",
            components=[],
            indexed=True,
        ),
        ParameterSemantics(
            parameter_name="approved",
            parameter_type="bool",
            components=[],
            indexed=False,
        ),
    ],
)

erc1155_URI_event = EventSemantics(
    signature="0x6bb7ff708619ba0610cba295a58592e0451dee2622938c8755667688daf3529b",
    anonymous=False,
    name="URI",
    parameters=[
        ParameterSemantics(
            parameter_name="value",
            parameter_type="string",
            components=[],
            indexed=False,
            dynamic=False
        ),
        ParameterSemantics(
            parameter_name="id",
            parameter_type="uint256",
            components=[],
            indexed=True,
        )
    ],
)

erc1155_URI_event_transformation = {
    "__input1__": TransformationSemantics(
        transformed_type="nft", transformation="decode_nft(__input1__)"
    )
}


erc1155_balanceOf_function = FunctionSemantics(
    signature="0x00fdd58e",
    name="balanceOf",
    inputs=[
        ParameterSemantics(parameter_name="owner", parameter_type="address"),
        ParameterSemantics(parameter_name="id", parameter_type="uint256"),
    ],
    outputs=[ParameterSemantics(parameter_name="", parameter_type="uint256")],
)

erc1155_balanceOfBatch_function = FunctionSemantics(
    signature="0x4e1273f4",
    name="balanceOfBatch",
    inputs=[
        ParameterSemantics(parameter_name="ownes", parameter_type="address[]"),
        ParameterSemantics(parameter_name="ids", parameter_type="uint256[]"),
    ],
    outputs=[ParameterSemantics(parameter_name="", parameter_type="uint256[]")],
)

erc1155_safeTransferFrom_function = FunctionSemantics(
    signature="0xf242432a",
    name="safeTransferFrom",
    inputs=[
        ParameterSemantics(parameter_name="from", parameter_type="address"),
        ParameterSemantics(parameter_name="to", parameter_type="address"),
        ParameterSemantics(parameter_name="id", parameter_type="uint256"),
        ParameterSemantics(parameter_name="value", parameter_type="uint256"),
        ParameterSemantics(
            parameter_name="data", parameter_type="bytes", components=[], dynamic=True
        ),
    ],
)

erc1155_safeTransferFrom_function_transformation = {
    "__input2__": TransformationSemantics(
        transformed_type="nft", transformation="decode_nft(__input2__)"
    )
}

erc1155_safeBatchTransferFrom_function = FunctionSemantics(
    signature="0x2eb2c2d6",
    name="safeBatchTransferFrom",
    inputs=[
        ParameterSemantics(parameter_name="from", parameter_type="address"),
        ParameterSemantics(parameter_name="to", parameter_type="address"),
        ParameterSemantics(parameter_name="ids", parameter_type="uint256[]"),
        ParameterSemantics(parameter_name="values", parameter_type="uint256[]"),
        ParameterSemantics(
            parameter_name="data", parameter_type="bytes", components=[], dynamic=True
        ),
    ],
)

erc1155_safeBatchTransferFrom_function_transformation = {
    "__input2__": TransformationSemantics(
        transformed_type="nft", transformation="decode_nft(__input2__)"
    )
}

erc1155_setApprovalForAll_function = FunctionSemantics(
    signature="0xa22cb465",
    name="setApprovalForAll",
    inputs=[
        ParameterSemantics(parameter_name="address", parameter_type="address"),
        ParameterSemantics(parameter_name="approved", parameter_type="bool"),
    ],
)

erc1155_isApprovedForAll_function = FunctionSemantics(
    signature="0xe985e9c5",
    name="isApprovedForAll",
    inputs=[
        ParameterSemantics(parameter_name="owner", parameter_type="address"),
        ParameterSemantics(parameter_name="operator", parameter_type="address"),
    ],
    outputs=[ParameterSemantics(parameter_name="", parameter_type="bool")],
)

ERC1155_EVENTS = {
    erc1155_transferSingle_event.signature: erc1155_transferSingle_event,
    erc1155_transferBatch_event.signature: erc1155_transferBatch_event,
    erc1155_approvalForAll_event.signature: erc1155_approvalForAll_event,
    erc1155_URI_event.signature: erc1155_URI_event,
}

ERC1155_FUNCTIONS = {
    erc1155_balanceOf_function.signature: erc1155_balanceOf_function,
    erc1155_safeTransferFrom_function.signature: erc1155_safeTransferFrom_function,
    erc1155_setApprovalForAll_function.signature: erc1155_setApprovalForAll_function,
    erc1155_isApprovedForAll_function.signature: erc1155_isApprovedForAll_function,
}

ERC1155_TRANSFORMATIONS = {
    erc1155_safeTransferFrom_function.signature: erc1155_safeTransferFrom_function_transformation,
    erc1155_safeBatchTransferFrom_function.signature: erc1155_safeBatchTransferFrom_function_transformation,
    erc1155_URI_event.signature: erc1155_URI_event_transformation,
}
