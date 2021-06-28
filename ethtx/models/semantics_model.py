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

from copy import deepcopy
from typing import List, Dict, Optional, Union

import jsonpickle

from ethtx.utils.pickable import JsonObject


class TransformationSemantics:
    transformed_name: Optional[str]
    transformed_type: Optional[str]
    transformation: Optional[str]

    def __init__(
        self,
        transformed_name: Optional[str] = None,
        transformed_type: Optional[str] = None,
        transformation: Optional[str] = "",
    ):
        self.transformed_name = transformed_name
        self.transformed_type = transformed_type
        self.transformation = transformation


class ParameterSemantics:
    parameter_name: str
    parameter_type: str
    indexed: bool
    dynamic: bool
    components: list

    def __init__(
        self,
        parameter_name: str,
        parameter_type: str,
        components: list,
        indexed: bool = False,
        dynamic: bool = False,
    ):
        self.parameter_name = parameter_name
        self.parameter_type = parameter_type
        self.components = components
        self.indexed = indexed
        self.dynamic = dynamic


class EventSemantics:
    signature: str
    anonymous: bool
    name: str
    parameters: List[ParameterSemantics]

    def __init__(
        self,
        signature: str,
        anonymous: bool,
        name: str,
        parameters: List[ParameterSemantics],
    ):
        self.signature = signature
        self.anonymous = anonymous
        self.name = name
        self.parameters = parameters


class FunctionSemantics:
    signature: str
    name: str
    inputs: List[ParameterSemantics]
    outputs: List[ParameterSemantics]

    def __init__(
        self,
        signature: str,
        name: str,
        inputs: List[ParameterSemantics],
        outputs: List[ParameterSemantics],
    ):
        self.signature = signature
        self.name = name
        self.inputs = inputs
        self.outputs = outputs


class ERC20Semantics:
    name: str
    symbol: str
    decimals: int

    def __init__(self, name: str, symbol: str, decimals: int):
        self.name = name
        self.symbol = symbol
        self.decimals = decimals


class ContractSemantics(JsonObject):
    code_hash: str
    name: str
    events: Dict[str, EventSemantics]
    functions: Dict[str, FunctionSemantics]
    transformations: [Dict[str, Dict[str, TransformationSemantics]]]

    def __init__(
        self,
        code_hash: str,
        name: str,
        events: Dict[str, EventSemantics],
        functions: Dict[str, FunctionSemantics],
        transformations: [Dict[str, TransformationSemantics]],
    ):
        self.code_hash = code_hash
        self.name = name
        self.events = events
        self.functions = functions
        self.transformations = transformations


class AddressSemantics(JsonObject):
    chain_id: str
    address: str
    name: str
    is_contract: bool
    contract: Union[ContractSemantics, str]
    standard: Optional[str]
    erc20: Optional[ERC20Semantics]

    def __init__(
        self,
        chain_id: str,
        address: str,
        name: str,
        is_contract: bool,
        contract: ContractSemantics,
        standard: Optional[str],
        erc20: Optional[ERC20Semantics],
    ):
        self.chain_id = chain_id
        self.address = address
        self.name = name
        self.is_contract = is_contract
        self.contract = contract
        self.standard = standard
        self.erc20 = erc20

    def json_str(self, entire: Optional[bool] = True) -> str:
        """Return object as encoded json."""
        if entire:
            return jsonpickle.encode(self, unpicklable=False)

        new_obj = deepcopy(self)
        new_obj.contract = new_obj.contract.code_hash

        return jsonpickle.encode(new_obj, unpicklable=False)

    def json(self, entire: Optional[bool] = True) -> Dict:
        """Return object as decoded dict."""
        if entire:
            return jsonpickle.decode(self.json_str(entire))

        new_obj = deepcopy(self)
        new_obj.contract = new_obj.contract.code_hash
        return jsonpickle.decode(self.json_str(entire))
