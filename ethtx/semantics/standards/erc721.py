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
    "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
    False,
    "Transfer",
    [
        ParameterSemantics("from", "address", [], True),
        ParameterSemantics("to", "address", [], True),
        ParameterSemantics("tokenId", "uint256", [], True),
    ],
)

erc721_transfer_event_transformation = {
    "__input2__": TransformationSemantics(
        transformed_type="nft", transformation="decode_nft(__input2__)"
    )
}

erc721_approval_event = EventSemantics(
    "0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925",
    False,
    "Approval",
    [
        ParameterSemantics("owner", "address", [], True),
        ParameterSemantics("approved", "address", [], True),
        ParameterSemantics("tokenId", "uint256", [], True),
    ],
)

erc721_approval_event_transformation = {
    "__input2__": TransformationSemantics(
        transformed_type="nft", transformation="decode_nft(__input2__)"
    )
}

erc721_approvalForAll_event = EventSemantics(
    "0x17307eab39ab6107e8899845ad3d59bd9653f200f220920489ca2b5937696c31",
    False,
    "ApprovalForAll",
    [
        ParameterSemantics("owner", "address", [], True),
        ParameterSemantics("operator", "address", [], True),
        ParameterSemantics("approved", "bool", [], False),
    ],
)

erc721_balanceOf_function = FunctionSemantics(
    "0x70a08231",
    "balanceOf",
    [ParameterSemantics("owner", "address", [])],
    [ParameterSemantics("", "uint256", [])],
)

erc721_ownerOf_function = FunctionSemantics(
    "0x6352211e",
    "ownerOf",
    [ParameterSemantics("tokenId", "uint256", [])],
    [ParameterSemantics("", "address", [])],
)

erc721_ownerOf_function_transformation = {
    "__input0__": TransformationSemantics(
        transformed_type="nft", transformation="decode_nft(__input0__)"
    )
}

erc721_transferFrom_function = FunctionSemantics(
    "0x23b872dd",
    "transferFrom",
    [
        ParameterSemantics("from", "address", []),
        ParameterSemantics("to", "address", []),
        ParameterSemantics("tokenId", "uint256", []),
    ],
    [],
)

erc721_transferFrom_function_transformation = {
    "__input2__": TransformationSemantics(
        transformed_type="nft", transformation="decode_nft(__input2__)"
    )
}

erc721_safeTransferFrom_function = FunctionSemantics(
    "0x42842e0e",
    "safeTransferFrom",
    [
        ParameterSemantics("from", "address", []),
        ParameterSemantics("to", "address", []),
        ParameterSemantics("tokenId", "uint256", []),
    ],
    [],
)

erc721_safeTransferFrom_function_transformation = {
    "__input2__": TransformationSemantics(
        transformed_type="nft", transformation="decode_nft(__input2__)"
    )
}

erc721_safeTransferFrom_with_data_function = FunctionSemantics(
    "0xb88d4fde",
    "safeTransferFrom",
    [
        ParameterSemantics("from", "address", []),
        ParameterSemantics("to", "address", []),
        ParameterSemantics("tokenId", "uint256", []),
        ParameterSemantics("data", "bytes", [], dynamic=True),
    ],
    [],
)

erc721_safeTransferFrom_with_data_function_transformation = {
    "__input2__": TransformationSemantics(
        transformed_type="nft", transformation="decode_nft(__input2__)"
    )
}

erc721_approve_function = FunctionSemantics(
    "0x095ea7b3",
    "approve",
    [
        ParameterSemantics("operator", "address", []),
        ParameterSemantics("tokenId", "uint256", []),
    ],
    [],
)

erc721_approve_function_transformation = {
    "__input1__": TransformationSemantics(
        transformed_type="nft", transformation="decode_nft(__input1__)"
    )
}

erc721_setApprovalForAll_function = FunctionSemantics(
    "0xa22cb465",
    "setApprovalForAll",
    [
        ParameterSemantics("address", "address", []),
        ParameterSemantics("approved", "bool", []),
    ],
    [],
)

erc721_getApproved_function = FunctionSemantics(
    "0x081812fc",
    "getApproved",
    [ParameterSemantics("tokenId", "uint256", [])],
    [ParameterSemantics("", "address", [])],
)

erc721_getApproved_function_transformation = {
    "__input0__": TransformationSemantics(
        transformed_type="nft", transformation="decode_nft(__input0__)"
    )
}

erc721_isApprovedForAll_function = FunctionSemantics(
    "0xe985e9c5",
    "isApprovedForAll",
    [
        ParameterSemantics("owner", "address", []),
        ParameterSemantics("operator", "address", []),
    ],
    [ParameterSemantics("", "bool", [])],
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
