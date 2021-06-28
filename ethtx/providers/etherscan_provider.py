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

import json
import logging
from functools import lru_cache
from typing import Dict, Optional

import requests
from web3 import Web3

from ethtx.exceptions import ProcessingException

log = logging.getLogger(__name__)


class EtherscanProvider:
    api_key: str
    endpoints: Dict[str, str]
    default_chain: Optional[str]

    def __init__(
        self, api_key, nodes: Dict[str, str], default_chain_id: Optional[str] = None
    ):
        self.api_key = api_key
        self.endpoints = nodes
        self.default_chain = default_chain_id

    def _get_chain_id(self, chain_id):
        _id = chain_id or self.default_chain

        if _id is None:
            raise ProcessingException(
                "chain_id must be provided as argument or constructor default"
            )
        return _id

    @lru_cache(maxsize=1024)
    def _get_contract_abi(self, chain_id, contract_name) -> Dict:
        # Etherscan connection parameters
        params = dict(
            module="contract",
            action="getsourcecode",
            address=contract_name,
            apikey=self.api_key,
        )

        chain_id = self._get_chain_id(chain_id)
        headers = {"User-Agent": "API"}
        resp = requests.get(
            url=self.endpoints[chain_id], params=params, headers=headers
        )

        if resp.status_code != 200:
            raise Exception(
                "Invalid status code for etherscan get: " + str(resp.status_code)
            )

        return resp.json()

    def get_contract_abi(self, chain_id, contract_name):

        decoded = False
        raw_abi = []

        try:
            resp = self._get_contract_abi(chain_id, contract_name)
            if resp["status"] == "1" and resp["message"] == "OK":
                contract_name = resp["result"][0]["ContractName"]
                if (
                    len(resp["result"][0]["ABI"])
                    and resp["result"][0]["ABI"] != "Contract source code not verified"
                ):
                    raw_abi = json.loads(resp["result"][0]["ABI"])
                    decoded = True

        except Exception as e:
            log.exception(
                "Etherscan connection failed while getting abi for %s on %s",
                contract_name,
                chain_id,
                exc_info=e,
            )

        abi = self._parse_abi(raw_abi)

        return dict(name=contract_name, abi=abi), decoded

    # helper function decoding contract ABI
    @staticmethod
    def _parse_abi(json_abi) -> Dict:

        # helper function to recursively parse components
        def _parse_components(components):

            comp_canonical = "("
            comp_inputs = list()

            for i, component in enumerate(components):

                argument = dict(name=component["name"], type=component["type"])

                if component["type"][:5] == "tuple":
                    sub_canonical, sub_components = _parse_components(
                        component["components"]
                    )
                    comp_canonical += sub_canonical + component["type"][5:]
                    argument["components"] = sub_components
                else:
                    comp_canonical += component["type"]
                    sub_components = []

                if i < len(components) - 1:
                    comp_canonical += ","

                if (
                    component["type"] in ("string", "bytes")
                    or component["type"][-2:] == "[]"
                ):
                    argument["dynamic"] = True
                elif component["type"] == "tuple":
                    argument["dynamic"] = any(c["dynamic"] for c in sub_components)
                else:
                    argument["dynamic"] = False

                if "indexed" in component:
                    argument["indexed"] = component["indexed"]

                comp_inputs.append(argument)

            comp_canonical += ")"

            return comp_canonical, comp_inputs

        functions = dict()
        events = dict()

        for item in json_abi:

            if "type" in item:

                # parse contract functions
                if item["type"] == "constructor":
                    _, inputs = _parse_components(item["inputs"])
                    functions["constructor"] = dict(
                        signature="constructor",
                        name="constructor",
                        inputs=inputs,
                        outputs=[],
                    )

                elif item["type"] == "fallback":
                    functions["fallback"] = {}

                elif item["type"] == "function":
                    canonical, inputs = _parse_components(item["inputs"])
                    canonical = item["name"] + canonical
                    function_hash = Web3.sha3(text=canonical).hex()
                    signature = function_hash[0:10]

                    _, outputs = _parse_components(item["outputs"])

                    functions[signature] = dict(
                        signature=signature,
                        name=item["name"],
                        inputs=inputs,
                        outputs=outputs,
                    )

                # parse contract events
                elif item["type"] == "event":
                    canonical, parameters = _parse_components(item["inputs"])
                    canonical = item["name"] + canonical
                    event_hash = Web3.sha3(text=canonical).hex()
                    signature = event_hash

                    events[signature] = dict(
                        signature=signature,
                        name=item["name"],
                        anonymous=item["anonymous"],
                        parameters=parameters,
                    )

        return dict(functions=functions, events=events)
