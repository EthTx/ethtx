from typing import List

from ethtx import EthTx, EthTxConfig
from ethtx.models.decoded_model import (
    DecodedTransfer,
    DecodedBalance,
    DecodedTransactionMetadata,
    DecodedEvent,
)
from ethtx.models.objects_model import Transaction, Event, Block
from ethtx.models.w3_model import W3Transaction, W3Block, W3Receipt

ETHERSCAN_API_KEY: str = "YOUR_ETHERSCAN_API_KEY"
TX_HASH: str = ""
NODE_URL: str = ""
CHAIN_ID: str = "mainnet"
POA: bool = False

ethtx_config = EthTxConfig(
    mongo_connection_string="mongomock://localhost/ethtx",  ##MongoDB connection string,
    etherscan_api_key=ETHERSCAN_API_KEY,
    web3nodes={
        "mainnet": {
            "hook": NODE_URL,  # multiple nodes supported, separate them with comma
            "poa": POA,  # represented by bool value
        }
    },
    default_chain="mainnet",
    etherscan_urls={
        "mainnet": "https://api.etherscan.io/api",
    },
)

ethtx = EthTx.initialize(ethtx_config)

### web3
web3provider = ethtx.providers.web3provider
w3transaction: W3Transaction = web3provider.get_transaction(TX_HASH)
w3block: W3Block = web3provider.get_block(w3transaction.blockNumber)
w3receipt: W3Receipt = web3provider.get_receipt(w3transaction.hash.hex())

transaction = Transaction.from_raw(
    w3transaction=w3transaction, w3receipt=w3receipt, w3calltree=None
)
block = Block.from_raw(
    "mainnet",
    w3block,
)

### ABI
abi_decoded_events: List[Event] = ethtx.decoders.abi_decoder.decode_events(
    transaction.events, block.metadata, transaction.metadata
)
abi_decoded_calls = None
abi_decoded_transfers: List[
    DecodedTransfer
] = ethtx.decoders.abi_decoder.decode_transfers(abi_decoded_calls, abi_decoded_events)
abi_decoded_balances: List[DecodedBalance] = ethtx.decoders.abi_decoder.decode_balances(
    abi_decoded_transfers
)

# semantically decode transaction components
proxies = ethtx.decoders.get_proxies(transaction.root_call, CHAIN_ID)
decoded_metadata: DecodedTransactionMetadata = (
    ethtx.decoders.semantic_decoder.decode_metadata(
        block.metadata, transaction.metadata, CHAIN_ID
    )
)
decoded_events: List[DecodedEvent] = ethtx.decoders.semantic_decoder.decode_events(
    abi_decoded_events, decoded_metadata, proxies
)
decoded_transfers: List[
    DecodedTransfer
] = ethtx.decoders.semantic_decoder.decode_transfers(
    abi_decoded_transfers, decoded_metadata
)
decoded_balances: List[
    DecodedBalance
] = ethtx.decoders.semantic_decoder.decode_balances(
    abi_decoded_balances, decoded_metadata
)

if __name__ == "__main__":
    # All objects have been decoded, use .dict() to get a dict representation
    print(decoded_metadata)
    print(decoded_events)
    print(decoded_transfers)
    print(decoded_balances)
