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
from typing import Dict, Tuple, Union, Any, Optional

from web3 import Web3

from ethtx.exceptions import InvalidEtherscanReturnCodeException
from .client import EtherscanClient
from ...utils.cache_tools import cache

log = logging.getLogger(__name__)


class EtherscanContract(EtherscanClient):
    def __init__(
        self,
        api_key: str,
        nodes: Dict[str, str],
        default_chain_id: Optional[str] = None,
    ):
        EtherscanClient.__init__(
            self, api_key=api_key, nodes=nodes, default_chain_id=default_chain_id
        )
        self.contract_dict = self.url_dict.copy()
        self.contract_dict[self.MODULE] = "contract"

    def get_contract_abi(
        self, chain_id, contract_name
    ) -> Tuple[Dict[str, Union[dict, Any]], bool]:
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

    @cache
    def _get_contract_abi(self, chain_id, contract_name) -> Dict:
        url_dict = self.contract_dict.copy()
        url_dict[self.ACTION] = "getsourcecode"
        url_dict[self.ADDRESS] = contract_name
        url = self.build_url(chain_id=self._get_chain_id(chain_id), url_dict=url_dict)

        # TODO: etherscan sometimes returns HTTP 502 with no apparent reason, so it's a quick fix
        # that should help, but number of tries should be taken from config in final solution I think
        for _ in range(3):
            resp = self.http.get(url)

            if resp.status_code == 200:
                break

        if resp.status_code != 200:
            raise InvalidEtherscanReturnCodeException(resp.status_code, url_dict)

        return resp.json()

    # helper function decoding contract ABI
    @staticmethod
    def _parse_abi(json_abi) -> Dict:
        # helper function to recursively parse components
        def _parse_components(components):

            comp_canonical = "("
            comp_inputs = []

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

        functions = {}
        events = {}

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
