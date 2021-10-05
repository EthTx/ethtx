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
from abc import ABC, abstractmethod
from typing import Callable, Any

from ens import ENS
from eth_typing import ChecksumAddress
from web3 import Web3


class ENSProviderABC(ABC):
    @abstractmethod
    def __init__(self, provider: Callable):
        ...

    @abstractmethod
    def name(self, address: Any):
        ...

    @abstractmethod
    def address(self, name: Any):
        ...


class Web3ENSProvider(ENSProviderABC):
    ns: ENS

    def __init__(self, provider: Web3):
        self.ns = ENS.fromWeb3(provider)

    def name(self, address: ChecksumAddress) -> str:
        return self.ns.name(address=address)

    def address(self, name: str) -> str:
        return self.ns.address(name=name)
