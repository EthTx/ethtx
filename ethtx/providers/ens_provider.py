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

import logging
from abc import ABC, abstractmethod
from typing import Any, TypeVar, Type

from ens import ENS
from web3 import Web3, exceptions

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

        try:
            name = ns.name(address=check_sum_address)
        except exceptions.BadFunctionCallOutput:
            log.warning(
                "ENS name not found for address: %s. There is no code associated with this address.",
                address,
            )
            name = None

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
