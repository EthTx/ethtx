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

from web3 import Web3

from ethtx.utils.cache_tools import cache


@cache
def is_eip1969_proxy(chain, delegator, delegate):
    implementation_slot = hex(
        int(Web3.keccak(text="eip1967.proxy.implementation").hex(), 16) - 1
    )
    try:
        implementation = (
            "0x"
            + chain.eth.get_storage_at(
                Web3.toChecksumAddress(delegator), implementation_slot
            ).hex()[-40:]
        )
        return implementation == delegate
    except:
        return False


@cache
def is_eip1969_beacon_proxy(chain, delegator, delegate):
    ibeacon_abi = """[
                        {
                            "inputs": [],
                            "name": "implementation",
                            "outputs": [
                                {
                                    "internalType": "address",
                                    "name": "",
                                    "type": "address"
                                }
                            ],
                            "stateMutability": "view",
                            "type": "function"
                        }
                    ]"""

    beacon_slot = hex(int(Web3.keccak(text="eip1967.proxy.beacon").hex(), 16) - 1)
    try:
        beacon = (
            "0x"
            + chain.eth.get_storage_at(
                Web3.toChecksumAddress(delegator), beacon_slot
            ).hex()[-40:]
        )
        beacon = chain.eth.contract(
            address=Web3.toChecksumAddress(beacon), abi=ibeacon_abi
        )
        implementation = beacon.functions.implementation().call()
        return implementation == Web3.toChecksumAddress(delegate)
    except:
        return False
