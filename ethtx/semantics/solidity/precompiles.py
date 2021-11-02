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


from ethtx.models.semantics_model import FunctionSemantics, ParameterSemantics

precompiles = {
    1: FunctionSemantics(
        signature="",
        name="ecrecover",
        inputs=[
            ParameterSemantics(parameter_name="hash", parameter_type="bytes32"),
            ParameterSemantics(parameter_name="v", parameter_type="bytes8"),
            ParameterSemantics(parameter_name="r", parameter_type="bytes32"),
            ParameterSemantics(parameter_name="s", parameter_type="bytes32"),
        ],
        outputs=[ParameterSemantics(parameter_name="", parameter_type="address")],
    ),
    2: FunctionSemantics(
        signature="",
        name="sha256",
        inputs=[ParameterSemantics(parameter_name="data", parameter_type="raw")],
        outputs=[ParameterSemantics(parameter_name="", parameter_type="bytes32")],
    ),
    3: FunctionSemantics(
        signature="",
        name="ripemd160",
        inputs=[ParameterSemantics(parameter_name="data", parameter_type="raw")],
        outputs=[ParameterSemantics(parameter_name="", parameter_type="bytes32")],
    ),
    4: FunctionSemantics(
        signature="",
        name="datacopy",
        inputs=[ParameterSemantics(parameter_name="data", parameter_type="raw")],
        outputs=[ParameterSemantics(parameter_name="", parameter_type="raw")],
    ),
    5: FunctionSemantics(
        signature="",
        name="bigModExp",
        inputs=[
            ParameterSemantics(parameter_name="base", parameter_type="bytes32"),
            ParameterSemantics(parameter_name="exp", parameter_type="bytes32"),
            ParameterSemantics(parameter_name="mod", parameter_type="bytes32"),
        ],
        outputs=[ParameterSemantics(parameter_name="", parameter_type="bytes32")],
    ),
    6: FunctionSemantics(
        signature="",
        name="bn256Add",
        inputs=[
            ParameterSemantics(parameter_name="ax", parameter_type="bytes32"),
            ParameterSemantics(parameter_name="ay", parameter_type="bytes32"),
            ParameterSemantics(parameter_name="bx", parameter_type="bytes32"),
            ParameterSemantics(parameter_name="by", parameter_type="bytes32"),
        ],
        outputs=[ParameterSemantics(parameter_name="", parameter_type="bytes32[2]")],
    ),
    7: FunctionSemantics(
        signature="",
        name="bn256ScalarMul",
        inputs=[
            ParameterSemantics(parameter_name="x", parameter_type="bytes32"),
            ParameterSemantics(parameter_name="y", parameter_type="bytes32"),
            ParameterSemantics(parameter_name="scalar", parameter_type="bytes32"),
        ],
        outputs=[ParameterSemantics(parameter_name="", parameter_type="bytes32[2]")],
    ),
    8: FunctionSemantics(
        signature="",
        name="bn256Pairing",
        inputs=[ParameterSemantics(parameter_name="input", parameter_type="raw")],
        outputs=[ParameterSemantics(parameter_name="", parameter_type="bytes32")],
    ),
}
