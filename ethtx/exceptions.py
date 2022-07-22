# Copyright 2021 DAI FOUNDATION (the original version https://github.com/daifoundation/ethtx_ce)
# Copyright 2021-2022 Token Flow Insights SA (modifications to the original software as recorded
# in the changelog https://github.com/EthTx/ethtx/blob/master/CHANGELOG.md)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.
#
# The product contains trademarks and other branding elements of Token Flow Insights SA which are
# not licensed under the Apache 2.0 license. When using or reproducing the code, please remove
# the trademark and/or other branding elements.


__all__ = [
    "NodeConnectionException",
    "ProcessingException",
    "InvalidTransactionHash",
    "InvalidEtherscanReturnCodeException",
]

import json
from typing import Dict


class NodeConnectionException(Exception):
    """Node Connection Exception."""

    def __init__(self):
        super().__init__("Couldn't connect to node(s)")


class ProcessingException(Exception):
    """Processing Exception."""

    def __init__(self, msg):
        super().__init__("Exception processing: " + msg)


class InvalidTransactionHash(Exception):
    """Invalid Transaction Hash."""

    def __init__(self, tx_hash):
        super().__init__("Invalid transaction hash provided: " + tx_hash)


class InvalidEtherscanReturnCodeException(Exception):
    def __init__(self, returned_code: int, params: Dict = None):
        params_msg = " with params: " + json.dumps(params) if params else ""
        msg = f"Invalid status code for etherscan request: {returned_code} {params_msg}"
        super().__init__(msg)
