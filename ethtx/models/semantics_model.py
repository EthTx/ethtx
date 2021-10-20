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

from typing import List, Dict, Optional, Union

from ethtx.models.base_model import BaseModel


class TransformationSemantics(BaseModel):
    transformed_name: Optional[str]
    transformed_type: Optional[str]
    transformation: str = ""


class ParameterSemantics(BaseModel):
    parameter_name: str
    parameter_type: str
    components: list = []
    indexed: bool = False
    dynamic: bool = False


class EventSemantics(BaseModel):
    signature: str
    anonymous: bool
    name: str
    parameters: List[ParameterSemantics]


class FunctionSemantics(BaseModel):
    signature: str
    name: str
    inputs: List[ParameterSemantics]
    outputs: List[ParameterSemantics] = []


class SignatureArg(BaseModel):
    name: str
    type: str


class Signature(BaseModel):
    signature_hash: str
    name: str
    args: List[SignatureArg]
    count: int = 1
    tuple: bool = False


class ERC20Semantics(BaseModel):
    name: str
    symbol: str
    decimals: int


class ContractSemantics(BaseModel):
    code_hash: str
    name: str
    events: Dict[str, EventSemantics] = {}
    functions: Dict[str, FunctionSemantics] = {}
    transformations: Dict[str, Dict[str, TransformationSemantics]] = {}


class AddressSemantics(BaseModel):
    chain_id: str
    address: str
    name: str
    is_contract: bool
    contract: ContractSemantics
    standard: Optional[str]
    erc20: Optional[ERC20Semantics]

    class Config:
        allow_mutation = True

    # def json_str(self, entire: Optional[bool] = True) -> str:
    #     """Return object as encoded json."""
    #     if entire:
    #         return jsonpickle.encode(self, unpicklable=False)
    #
    #     new_obj = deepcopy(self)
    #     new_obj.contract = new_obj.contract.code_hash
    #
    #     return jsonpickle.encode(new_obj, unpicklable=False)
    #
    # def json(self, entire: Optional[bool] = True) -> Dict:
    #     """Return object as decoded dict."""
    #     if entire:
    #         return jsonpickle.decode(self.json_str(entire))
    #
    #     new_obj = deepcopy(self)
    #     new_obj.contract = new_obj.contract.code_hash
    #     return jsonpickle.decode(self.json_str(entire))
