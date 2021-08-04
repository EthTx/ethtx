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

from functools import lru_cache
from typing import Optional, List

from ethtx.decoders.decoders.semantics import decode_events_and_functions
from ethtx.models.semantics_model import (
    AddressSemantics,
    ContractSemantics,
    ParameterSemantics,
    ERC20Semantics,
    TransformationSemantics,
    FunctionSemantics,
    EventSemantics,
)
from ethtx.providers.etherscan_provider import EtherscanProvider
from ethtx.providers.semantic_providers.semantics_database import ISemanticsDatabase
from ethtx.providers.web3_provider import Web3Provider
from ethtx.semantics.protocols_router import amend_contract_semantics
from ethtx.semantics.standards.erc20 import ERC20_FUNCTIONS, ERC20_EVENTS
from ethtx.semantics.standards.erc721 import ERC721_FUNCTIONS, ERC721_EVENTS
from ethtx.semantics.solidity.precompiles import precompiles


class SemanticsRepository:
    def __init__(
        self,
        database_connection: ISemanticsDatabase,
        etherscan_provider: EtherscanProvider,
        web3provider: Web3Provider,
    ):
        self.database = database_connection
        self.etherscan = etherscan_provider
        self._web3provider = web3provider
        self._records: Optional[List] = None

    def record(self):
        """Records is an array used to hold semantics used in tx decing process.
        This recording is used just for logging"""
        self._records = []

    def end_record(self) -> List:
        tmp_records = self._records
        self._records = None
        return tmp_records

    def _read_stored_semantics(self, address: str, chain_id: str):

        def decode_parameter(_parameter):
            components_semantics = []
            for component in _parameter["components"]:
                components_semantics.append(decode_parameter(component))

            decoded_parameter = ParameterSemantics(
                _parameter["parameter_name"],
                _parameter["parameter_type"],
                components_semantics,
                _parameter["indexed"],
                _parameter["dynamic"],
            )

            return decoded_parameter

        if not address:
            return None

        ZERO_HASH = "0xc5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470"

        raw_address_semantics = self.database.get_address_semantics(chain_id, address)

        if raw_address_semantics:

            if raw_address_semantics.get("erc20"):
                erc20_semantics = ERC20Semantics(
                    raw_address_semantics["erc20"]["name"],
                    raw_address_semantics["erc20"]["symbol"],
                    raw_address_semantics["erc20"]["decimals"],
                )
            else:
                erc20_semantics = None

            if raw_address_semantics["contract"] == ZERO_HASH:
                contract_semantics = ContractSemantics(
                    raw_address_semantics["contract"], "EOA", dict(), dict(), dict()
                )

            else:

                raw_contract_semantics = self.database.get_contract_semantics(
                    raw_address_semantics["contract"]
                )
                events = dict()

                for signature, event in raw_contract_semantics["events"].items():

                    parameters_semantics = []
                    for parameter in event["parameters"]:
                        parameters_semantics.append(decode_parameter(parameter))

                    events[signature] = EventSemantics(
                        signature,
                        event["anonymous"],
                        event["name"],
                        parameters_semantics,
                    )

                functions = dict()
                for signature, function in raw_contract_semantics["functions"].items():

                    inputs_semantics = []
                    for parameter in function["inputs"]:
                        inputs_semantics.append(decode_parameter(parameter))
                    outputs_semantics = []
                    for parameter in function["outputs"]:
                        outputs_semantics.append(decode_parameter(parameter))

                    functions[signature] = FunctionSemantics(
                        signature, function["name"], inputs_semantics, outputs_semantics
                    )

                transformations = dict()
                for signature, parameters_transformations in raw_contract_semantics[
                    "transformations"
                ].items():
                    transformations[signature] = dict()
                    for parameter, transformation in parameters_transformations.items():
                        transformations[signature][parameter] = TransformationSemantics(
                            transformation["transformed_name"],
                            transformation["transformed_type"],
                            transformation["transformation"],
                        )

                contract_semantics = ContractSemantics(
                    raw_contract_semantics["code_hash"],
                    raw_contract_semantics["name"],
                    events,
                    functions,
                    transformations,
                )

            address_semantics = AddressSemantics(
                chain_id,
                address,
                raw_address_semantics["name"],
                raw_address_semantics["is_contract"],
                contract_semantics,
                raw_address_semantics["standard"],
                erc20_semantics,
            )

            return address_semantics

        else:
            return None

    @lru_cache(maxsize=128)
    def get_semantics(self, chain_id: str, address: str) -> Optional[AddressSemantics]:

        if not address:
            return None

        ZERO_HASH = "0xc5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470"

        address_semantics = self._read_stored_semantics(address, chain_id)
        if not address_semantics:

            # try to read the semantics form the Etherscan provider
            provider = self._web3provider
            code_hash = provider.get_code_hash(address)

            if code_hash != ZERO_HASH:
                # smart contract
                raw_semantics, decoded = self.etherscan.get_contract_abi(
                    chain_id, address
                )
                if decoded and raw_semantics:
                    # raw semantics received from Etherscan
                    events, functions = decode_events_and_functions(
                        raw_semantics["abi"]
                    )
                    standard, standard_semantics = self._decode_standard_semantics(
                        address, raw_semantics["name"], events, functions
                    )
                    if standard == "ERC20":
                        erc20_semantics = standard_semantics
                    else:
                        proxy_erc20 = provider.guess_erc20_proxy(address)
                        if proxy_erc20:
                            erc20_semantics = ERC20Semantics(**proxy_erc20)
                        else:
                            erc20_semantics = None
                    contract_semantics = ContractSemantics(
                        code_hash, raw_semantics["name"], events, functions, dict()
                    )
                    address_semantics = AddressSemantics(
                        chain_id,
                        address,
                        raw_semantics["name"],
                        True,
                        contract_semantics,
                        standard,
                        erc20_semantics,
                    )

                else:
                    # try to guess if the address is a toke
                    potential_erc20_semantics = provider.guess_erc20_token(address)
                    if potential_erc20_semantics:
                        standard = "ERC20"
                        erc20_semantics = ERC20Semantics(
                            potential_erc20_semantics["name"],
                            potential_erc20_semantics["symbol"],
                            potential_erc20_semantics["decimals"],
                        )
                    else:
                        standard = None
                        erc20_semantics = None

                    contract_semantics = ContractSemantics(
                        code_hash, address, dict(), dict(), dict()
                    )
                    address_semantics = AddressSemantics(
                        chain_id,
                        address,
                        address,
                        True,
                        contract_semantics,
                        standard,
                        erc20_semantics,
                    )

            else:
                # externally owned address
                contract_semantics = ContractSemantics(
                    ZERO_HASH, "EOA", dict(), dict(), dict()
                )
                address_semantics = AddressSemantics(
                    chain_id, address, address, False, contract_semantics, None, None
                )

        self.update_semantics(address_semantics)

        # amend semantics with locally stored updates
        amend_contract_semantics(address_semantics.contract)

        return address_semantics

    def _decode_standard_semantics(self, address, name, events, functions):
        standard = None
        standard_semantics = None

        if not address:
            return standard, standard_semantics

        if all(erc20_event in events for erc20_event in ERC20_EVENTS) and all(
            erc20_function in functions for erc20_function in ERC20_FUNCTIONS
        ):
            standard = "ERC20"
            try:
                provider = self._web3provider
                token_data = provider.get_erc20_token(address, name, functions)
                standard_semantics = ERC20Semantics(
                    token_data["name"], token_data["symbol"], token_data["decimals"]
                )
            except Exception:
                standard_semantics = ERC20Semantics(name, name, 18)
        elif all(erc721_event in events for erc721_event in ERC721_EVENTS) and all(
            erc721_function in functions for erc721_function in ERC721_FUNCTIONS
        ):
            standard = "ERC721"
            standard_semantics = None

        return standard, standard_semantics

    @lru_cache(maxsize=128)
    def get_event_abi(self, chain_id, address, signature):

        if not address:
            return None

        semantics = self.get_semantics(chain_id, address)
        event_semantics = (
            semantics.contract.events.get(signature) if semantics else None
        )

        return event_semantics

    @lru_cache(maxsize=128)
    def get_transformations(self, chain_id, address, signature):

        if not address:
            return None

        semantics = self.get_semantics(chain_id, address)
        if semantics:
            transformations = semantics.contract.transformations.get(signature)
        else:
            transformations = None

        return transformations

    @lru_cache(maxsize=128)
    def get_anonymous_event_abi(self, chain_id, address):

        if not address:
            return None

        semantics = self.get_semantics(chain_id, address)
        event_semantics = None
        if semantics:
            anonymous_events = {
                signature
                for signature, event in semantics.contract.events.items()
                if event.anonymous
            }
            if len(anonymous_events) == 1:
                event_signature = anonymous_events.pop()
                event_semantics = semantics.contract.events[event_signature]

        return event_semantics

    @lru_cache(maxsize=128)
    def get_function_abi(self, chain_id, address, signature):

        if not address:
            return None

        semantics = self.get_semantics(chain_id, address)
        function_semantics = (
            semantics.contract.functions.get(signature) if semantics else None
        )

        return function_semantics

    @lru_cache(maxsize=128)
    def get_constructor_abi(self, chain_id, address):

        if not address:
            return None

        semantics = self.get_semantics(chain_id, address)
        constructor_semantics = (
            semantics.contract.functions.get("constructor") if semantics else None
        )
        if constructor_semantics:
            constructor_semantics.outputs.append(
                ParameterSemantics("__create_output__", "ignore", [], False, True)
            )

        return constructor_semantics

    def get_address_label(self, chain_id, address, token_proxies=None):

        if not address:
            return ''

        if int(address, 16) in precompiles:
            contract_label = 'Precompiled'
        else:
            semantics = self.get_semantics(chain_id, address)
            if semantics.erc20:
                contract_label = semantics.erc20.symbol
            elif token_proxies and address in token_proxies:
                contract_label = token_proxies[address][1] + "_proxy"
            else:
                contract_label = semantics.name if semantics and semantics.name else address

        return contract_label

    @lru_cache(maxsize=128)
    def check_is_contract(self, chain_id, address):

        if not address:
            return False

        semantics = self.get_semantics(chain_id, address)
        is_contract = semantics is not None and semantics.is_contract

        return is_contract

    @lru_cache(maxsize=128)
    def get_standard(self, chain_id, address):

        if not address:
            return None

        semantics = self.get_semantics(chain_id, address)
        standard = semantics.standard if semantics is not None else None

        return standard

    def get_token_data(self, chain_id, address, token_proxies=None):

        if not address:
            return None, None, None

        semantics = self.get_semantics(chain_id, address)
        if semantics and semantics.erc20:
            token_name = (
                semantics.erc20.name if semantics and semantics.erc20 else address
            )
            token_symbol = (
                semantics.erc20.symbol if semantics and semantics.erc20 else "Unknown"
            )
            token_decimals = (
                semantics.erc20.decimals if semantics and semantics.erc20 else 18
            )
        elif token_proxies and address in token_proxies:
            token_name, token_symbol, token_decimals = token_proxies[address]
        else:
            token_name = address
            token_symbol = "Unknown"
            token_decimals = 18

        return token_name, token_symbol, token_decimals

    def update_address(self, chain_id, address, contract):

        updated_address = {"network": chain_id, "address": address, **contract}
        self.database.insert_address(address_data=updated_address, update_if_exist=True)

        return updated_address

    def update_semantics(self, semantics):

        if not semantics:
            return

        address_semantics = semantics.json(False)
        contract_semantics = semantics.contract.json()

        self.database.insert_contract(contract_semantics, update_if_exist=True)
        self.database.insert_address(address_semantics, update_if_exist=True)
