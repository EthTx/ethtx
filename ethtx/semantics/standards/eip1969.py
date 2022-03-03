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
