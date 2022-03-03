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
import logging
from abc import ABC, abstractmethod
from typing import Any, TypeVar, Type

from ens import ENS
from web3 import Web3

log = logging.getLogger(__name__)

T = TypeVar("T")


class ENSProviderBase(ABC):
    @abstractmethod
    def name(self, provider: Type[T], address: Any):
        ...

    @abstractmethod
    def address(self, provider: Type[T], name: Any):
        ...


class Web3ENSProvider(ENSProviderBase):
    ns: ENS

    def name(self, provider: Web3, address: str) -> str:
        ns = self._set_provider(provider)
        check_sum_address = Web3.toChecksumAddress(address)
        name = ns.name(address=check_sum_address)

        if name:
            log.info("ENS resolved an address: %s to name: %s", address, name)

        return name if name else address

    def address(self, provider: Web3, name: str) -> str:
        ns = self._set_provider(provider)
        address = ns.address(name=name)

        if address:
            log.info("ENS resolved name: %s to address: %s", name, address)

        return address if address else name

    def _set_provider(self, provider: Web3) -> ENS:
        return ENS.fromWeb3(provider)


ENSProvider = Web3ENSProvider()
