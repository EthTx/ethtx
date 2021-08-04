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
            "",
            "ecrecover",
            [
                ParameterSemantics("hash", "bytes32", []),
                ParameterSemantics("v", "bytes8", []),
                ParameterSemantics("r", "bytes32", []),
                ParameterSemantics("s", "bytes32", []),
            ],
            [ParameterSemantics("", "address", [])],
        ),
    2: FunctionSemantics(
            "",
            "sha256",
            [
                ParameterSemantics("data", "raw", [])
            ],
            [ParameterSemantics("", "bytes32", [])],
        ),
    3: FunctionSemantics(
            "",
            "ripemd160",
            [
                ParameterSemantics("data", "raw", [])
            ],
            [ParameterSemantics("", "bytes32", [])],
        ),
    4: FunctionSemantics(
            "",
            "datacopy",
            [
                ParameterSemantics("data", "raw", [])
            ],
            [ParameterSemantics("", "raw", [])],
        ),
    5: FunctionSemantics(
            "",
            "bigModExp",
            [
                ParameterSemantics("base", "bytes32", []),
                ParameterSemantics("exp", "bytes32", []),
                ParameterSemantics("mod", "bytes32", [])
            ],
            [ParameterSemantics("", "bytes32", [])],
        ),
    6: FunctionSemantics(
            "",
            "bn256Add",
            [
                ParameterSemantics("ax", "bytes32", []),
                ParameterSemantics("ay", "bytes32", []),
                ParameterSemantics("bx", "bytes32", []),
                ParameterSemantics("by", "bytes32", [])
            ],
            [ParameterSemantics("", "bytes32[2]", [])],
        ),
    7: FunctionSemantics(
            "",
            "bn256ScalarMul",
            [
                ParameterSemantics("x", "bytes32", []),
                ParameterSemantics("y", "bytes32", []),
                ParameterSemantics("scalar", "bytes32", [])
            ],
            [ParameterSemantics("", "bytes32[2]", [])],
        ),
    8: FunctionSemantics(
            "",
            "bn256Pairing",
            [
                ParameterSemantics("input", "raw", [])
            ],
            [ParameterSemantics("", "bytes32", [])],
        ),
}
