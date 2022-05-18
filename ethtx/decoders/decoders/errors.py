from ethtx.models.semantics_model import ParameterSemantics


ERRORS = {
    '0x08c379a0': {
        'name': 'Error',
        'abi': [
            ParameterSemantics(
                parameter_name="Error",
                parameter_type="string",
                components=[],
                indexed=False,
                dynamic=True,
            )
        ]
    },
    '0xfdb6ca8d': {
        'name': 'OrderStatusError',
        'abi': [
            ParameterSemantics(
                parameter_name="orderHash",
                parameter_type="bytes32",
            ),
            ParameterSemantics(
                parameter_name="orderStatus",
                parameter_type="uint8"
            )
        ]
    },
    '0x990174d2': {
        'name': 'IncompleteTransformERC20Error',
        'abi':
            [
                ParameterSemantics(
                    parameter_name="outputToken",
                    parameter_type="address"
                ),
                ParameterSemantics(
                    parameter_name="outputTokenAmount",
                    parameter_type="uint256"
                ),
                ParameterSemantics(
                    parameter_name="minOutputTokenAmount",
                    parameter_type="uint256"
                )
            ]
    },
    '0x4678472b': {
        'name': 'AssetProxyTransferError',
        'abi':
            [
                ParameterSemantics(
                    parameter_name="orderHash",
                    parameter_type="bytes32"
                ),
                ParameterSemantics(
                    parameter_name="assetData",
                    parameter_type="bytes"
                ),
                ParameterSemantics(
                    parameter_name="errorData",
                    parameter_type="bytes"
                )
            ]
    },
    '0x87cb1e75': {
        'name': 'PayProtocolFeeError',
        'abi':
            [
                ParameterSemantics(
                    parameter_name="orderHash",
                    parameter_type="bytes32"
                ),
                ParameterSemantics(
                    parameter_name="protocolFee",
                    parameter_type="uint256"
                ),
                ParameterSemantics(
                    parameter_name="makerAddress",
                    parameter_type="address"
                ),
                ParameterSemantics(
                    parameter_name="takerAddress",
                    parameter_type="address"
                ),
                ParameterSemantics(
                    parameter_name="errorData",
                    parameter_type="bytes"
                )
            ]
    },
    '0x339f3de2': {
        'name': 'RoundingError',
        'abi':
            [
                ParameterSemantics(
                    parameter_name="numerator",
                    parameter_type='uint256'
                ),
                ParameterSemantics(
                    parameter_name="denominator",
                    parameter_type='uint256'
                ),
                ParameterSemantics(
                    parameter_name="target",
                    parameter_type='uint256'
                ),
            ]
    },
    '0x18e4b141': {
        'name': 'IncompleteFillError',
        'abi': [
            ParameterSemantics(
                parameter_name='errorCode',
                parameter_type='uint8'
            ),
            ParameterSemantics(
                parameter_name='expectedAssetFillAmount',
                parameter_type='uint256'
            ),
            ParameterSemantics(
                parameter_name='actualAssetFillAmount',
                parameter_type='uint256'
            )
        ]
    }
}