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

from typing import List, Dict, Optional, TYPE_CHECKING

from ethtx.models.base_model import BaseModel

if TYPE_CHECKING:
    from ethtx.providers.semantic_providers import ISemanticsDatabase


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
    guessed: bool = False


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

    @staticmethod
    def from_mongo_record(
        raw_address_semantics: Dict, database: "ISemanticsDatabase"
    ) -> "AddressSemantics":

        ZERO_HASH = "0xc5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470"

        def decode_parameter(_parameter):
            components_semantics = []
            if "components" in _parameter:
                for component in _parameter["components"]:
                    components_semantics.append(decode_parameter(component))

            decoded_parameter = ParameterSemantics(
                parameter_name=_parameter["parameter_name"],
                parameter_type=_parameter["parameter_type"],
                components=components_semantics,
                indexed=_parameter["indexed"],
                dynamic=_parameter["dynamic"],
            )

            return decoded_parameter

        if raw_address_semantics.get("erc20"):
            erc20_semantics = ERC20Semantics(
                name=raw_address_semantics["erc20"]["name"],
                symbol=raw_address_semantics["erc20"]["symbol"],
                decimals=raw_address_semantics["erc20"]["decimals"],
            )
        else:
            erc20_semantics = None

        if raw_address_semantics["contract"] == ZERO_HASH:
            contract_semantics = ContractSemantics(
                code_hash=raw_address_semantics["contract"], name="EOA"
            )

        else:

            raw_contract_semantics = database.get_contract_semantics(
                raw_address_semantics["contract"]
            )
            events = {}

            for signature, event in raw_contract_semantics["events"].items():

                parameters_semantics = []
                for parameter in event["parameters"]:
                    parameters_semantics.append(decode_parameter(parameter))

                events[signature] = EventSemantics(
                    signature=signature,
                    anonymous=event["anonymous"],
                    name=event["name"],
                    parameters=parameters_semantics,
                )

            functions = {}
            for signature, function in raw_contract_semantics["functions"].items():

                inputs_semantics = []
                for parameter in function["inputs"]:
                    inputs_semantics.append(decode_parameter(parameter))
                outputs_semantics = []
                for parameter in function["outputs"]:
                    outputs_semantics.append(decode_parameter(parameter))

                functions[signature] = FunctionSemantics(
                    signature=signature,
                    name=function["name"],
                    inputs=inputs_semantics,
                    outputs=outputs_semantics,
                )

            transformations = {}
            for signature, parameters_transformations in raw_contract_semantics[
                "transformations"
            ].items():
                transformations[signature] = {}
                for parameter, transformation in parameters_transformations.items():
                    transformations[signature][parameter] = TransformationSemantics(
                        transformed_name=transformation["transformed_name"],
                        transformed_type=transformation["transformed_type"],
                        transformation=transformation["transformation"],
                    )

            contract_semantics = ContractSemantics(
                code_hash=raw_contract_semantics["code_hash"],
                name=raw_contract_semantics["name"],
                events=events,
                functions=functions,
                transformations=transformations,
            )

        address = raw_address_semantics.get("address")
        chain_id = raw_address_semantics.get("chain_id")
        name = raw_address_semantics.get("name", address)

        address_semantics = AddressSemantics(
            chain_id=chain_id,
            address=address,
            name=name,
            is_contract=raw_address_semantics["is_contract"],
            contract=contract_semantics,
            standard=raw_address_semantics["standard"],
            erc20=erc20_semantics,
        )

        return address_semantics
