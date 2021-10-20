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
    FunctionSemantics,
    ParameterSemantics,
    TransformationSemantics,
)

erc721_transfer_event = EventSemantics(
    signature="0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
    anonymous=False,
    name="Transfer",
    parameters=[
        ParameterSemantics(
            parameter_name="from", parameter_type="address", components=[], indexed=True
        ),
        ParameterSemantics(
            parameter_name="to", parameter_type="address", components=[], indexed=True
        ),
        ParameterSemantics(
            parameter_name="tokenId",
            parameter_type="uint256",
            components=[],
            indexed=True,
        ),
    ],
)

erc721_transfer_event_transformation = {
    "__input2__": TransformationSemantics(
        transformed_type="nft", transformation="decode_nft(__input2__)"
    )
}

erc721_approval_event = EventSemantics(
    signature="0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925",
    anonymous=False,
    name="Approval",
    parameters=[
        ParameterSemantics(
            parameter_name="owner",
            parameter_type="address",
            components=[],
            indexed=True,
        ),
        ParameterSemantics(
            parameter_name="approved",
            parameter_type="address",
            components=[],
            indexed=True,
        ),
        ParameterSemantics(
            parameter_name="tokenId",
            parameter_type="uint256",
            components=[],
            indexed=True,
        ),
    ],
)

erc721_approval_event_transformation = {
    "__input2__": TransformationSemantics(
        transformed_type="nft", transformation="decode_nft(__input2__)"
    )
}

erc721_approvalForAll_event = EventSemantics(
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

erc721_balanceOf_function = FunctionSemantics(
    signature="0x70a08231",
    name="balanceOf",
    inputs=[ParameterSemantics(parameter_name="owner", parameter_type="address")],
    outputs=[ParameterSemantics(parameter_name="", parameter_type="uint256")],
)

erc721_ownerOf_function = FunctionSemantics(
    signature="0x6352211e",
    name="ownerOf",
    inputs=[ParameterSemantics(parameter_name="tokenId", parameter_type="uint256")],
    outputs=[ParameterSemantics(parameter_name="", parameter_type="address")],
)

erc721_ownerOf_function_transformation = {
    "__input0__": TransformationSemantics(
        transformed_type="nft", transformation="decode_nft(__input0__)"
    )
}

erc721_transferFrom_function = FunctionSemantics(
    signature="0x23b872dd",
    name="transferFrom",
    inputs=[
        ParameterSemantics(parameter_name="from", parameter_type="address"),
        ParameterSemantics(parameter_name="to", parameter_type="address"),
        ParameterSemantics(parameter_name="tokenId", parameter_type="uint256"),
    ],
)

erc721_transferFrom_function_transformation = {
    "__input2__": TransformationSemantics(
        transformed_type="nft", transformation="decode_nft(__input2__)"
    )
}

erc721_safeTransferFrom_function = FunctionSemantics(
    signature="0x42842e0e",
    name="safeTransferFrom",
    inputs=[
        ParameterSemantics(parameter_name="from", parameter_type="address"),
        ParameterSemantics(parameter_name="to", parameter_type="address"),
        ParameterSemantics(parameter_name="tokenId", parameter_type="uint256"),
    ],
)

erc721_safeTransferFrom_function_transformation = {
    "__input2__": TransformationSemantics(
        transformed_type="nft", transformation="decode_nft(__input2__)"
    )
}

erc721_safeTransferFrom_with_data_function = FunctionSemantics(
    signature="0xb88d4fde",
    name="safeTransferFrom",
    inputs=[
        ParameterSemantics(parameter_name="from", parameter_type="address"),
        ParameterSemantics(parameter_name="to", parameter_type="address"),
        ParameterSemantics(parameter_name="tokenId", parameter_type="uint256"),
        ParameterSemantics(
            parameter_name="data", parameter_type="bytes", components=[], dynamic=True
        ),
    ],
)

erc721_safeTransferFrom_with_data_function_transformation = {
    "__input2__": TransformationSemantics(
        transformed_type="nft", transformation="decode_nft(__input2__)"
    )
}

erc721_approve_function = FunctionSemantics(
    signature="0x095ea7b3",
    name="approve",
    inputs=[
        ParameterSemantics(parameter_name="operator", parameter_type="address"),
        ParameterSemantics(parameter_name="tokenId", parameter_type="uint256"),
    ],
)

erc721_approve_function_transformation = {
    "__input1__": TransformationSemantics(
        transformed_type="nft", transformation="decode_nft(__input1__)"
    )
}

erc721_setApprovalForAll_function = FunctionSemantics(
    signature="0xa22cb465",
    name="setApprovalForAll",
    inputs=[
        ParameterSemantics(parameter_name="address", parameter_type="address"),
        ParameterSemantics(parameter_name="approved", parameter_type="bool"),
    ],
)

erc721_getApproved_function = FunctionSemantics(
    signature="0x081812fc",
    name="getApproved",
    inputs=[ParameterSemantics(parameter_name="tokenId", parameter_type="uint256")],
    outputs=[ParameterSemantics(parameter_name="", parameter_type="address")],
)

erc721_getApproved_function_transformation = {
    "__input0__": TransformationSemantics(
        transformed_type="nft", transformation="decode_nft(__input0__)"
    )
}

erc721_isApprovedForAll_function = FunctionSemantics(
    signature="0xe985e9c5",
    name="isApprovedForAll",
    inputs=[
        ParameterSemantics(parameter_name="owner", parameter_type="address"),
        ParameterSemantics(parameter_name="operator", parameter_type="address"),
    ],
    outputs=[ParameterSemantics(parameter_name="", parameter_type="bool")],
)

ERC721_EVENTS = {
    erc721_transfer_event.signature: erc721_transfer_event,
    erc721_approval_event.signature: erc721_approval_event,
    erc721_approvalForAll_event.signature: erc721_approvalForAll_event,
}

ERC721_FUNCTIONS = {
    erc721_balanceOf_function.signature: erc721_balanceOf_function,
    erc721_ownerOf_function.signature: erc721_ownerOf_function,
    erc721_transferFrom_function.signature: erc721_transferFrom_function,
    erc721_safeTransferFrom_function.signature: erc721_safeTransferFrom_function,
    erc721_safeTransferFrom_with_data_function.signature: erc721_safeTransferFrom_with_data_function,
    erc721_approve_function.signature: erc721_approve_function,
    erc721_setApprovalForAll_function.signature: erc721_setApprovalForAll_function,
    erc721_getApproved_function.signature: erc721_getApproved_function,
    erc721_isApprovedForAll_function.signature: erc721_isApprovedForAll_function,
}

ERC721_TRANSFORMATIONS = {
    erc721_transfer_event.signature: erc721_transfer_event_transformation,
    erc721_approval_event.signature: erc721_approval_event_transformation,
    erc721_ownerOf_function.signature: erc721_ownerOf_function_transformation,
    erc721_transferFrom_function.signature: erc721_transferFrom_function_transformation,
    erc721_safeTransferFrom_function.signature: erc721_safeTransferFrom_function_transformation,
    erc721_safeTransferFrom_with_data_function.signature: erc721_safeTransferFrom_with_data_function_transformation,
    erc721_approve_function.signature: erc721_approve_function_transformation,
    erc721_getApproved_function.signature: erc721_getApproved_function_transformation,
}
