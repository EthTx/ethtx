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


__all__ = ["Web3ConnectionException", "ProcessingException", "InvalidTransactionHash"]


class Web3ConnectionException(Exception):
    """Web3 Connection Exception."""

    def __init__(self):
        super().__init__("Couldn't connect to web3provider")


class ProcessingException(Exception):
    """Processing Exception."""

    def __init__(self, msg):
        super().__init__("Exception processing: " + msg)


class InvalidTransactionHash(Exception):
    """Invalid Transaction Hash."""

    def __init__(self, tx_hash):
        super().__init__("Invalid transaction hash provided: " + tx_hash)
