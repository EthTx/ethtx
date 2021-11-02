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


__all__ = [
    "NodeConnectionException",
    "ProcessingException",
    "InvalidTransactionHash",
    "InvalidEtherscanReturnCodeException",
    "FourByteConnectionException",
    "FourByteContentException",
    "FourByteException",
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


class FourByteException(Exception):
    """4byte base exception class."""


class FourByteConnectionException(FourByteException):
    """4byte directory connection error."""

    def __init__(self, msg: str):
        super().__init__(f"Couldn't connect to 4byte.directory: {msg}")


class FourByteContentException(FourByteException):
    """4byte content exception. Missing output."""

    def __init__(self, status_code: int, content: bytes):
        super().__init__(
            f"Wrong response from 4byte.directory. Status code:{status_code}, content: {content}"
        )
