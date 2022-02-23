<h1 align='center' style='border-bottom: none'>
  <p>EthTx - Ethereum transactions decoder </p>
</h1>

<p align="center">
<a target="_blank">
    <img src="https://img.shields.io/badge/Made%20with-Python-1f425f.svg" alt="Python">
</a>
<a target="_blank">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Black">
</a>
<a target="_blank">
    <img src="https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github" alt="OpenSource">
</a>
<a target="_blank">
    <img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" alt="Apache">
</a>
<a target="_blank">
    <img src="https://img.shields.io/pypi/v/EthTx?label=pypi%20package" alt="EthTxPyPi">
</a>
</p>

## Introduction

Source Code: [https://github.com/ethtx/ethtx](https://github.com/ethtx/ethtx)

## Installation

```shell
pip install ethtx
```

## Requirements

The package needs a few external resources, defined in `EthTxConfig` object:

1. **Erigon/Geth node** - required to have access to the raw Ethereum data; it must be a full archive node with
   the `debug` option ON
2. **Etherscan API key** - required to get the source code and ABI for smart contracts used in transaction
3. (Optional) **MongoDB database** - required to store smart contracts' ABI and semantics used in the decoding process.
   If you don't want to setup permanent database, you can enter `mongomock://localhost/ethtx`, then in-memory mongo will be
   set up that discards all data with every run.
4. Copy `.env_sample` to `.env` and fill required field according to description
```dotenv
# REQUIRED:

# WEB3 NODES:
# Proper nodes are required to run ethtx. 
# Values are populated from the environment by treating the environment variable's value as a JSON-encoded string.
# EXAMPLE: WEB3_NODES='{"mainnet": {"hook": "https://geth", "poa": false}, "rinkeby": {"hook": "https://eth-rinkeby", "poa": true}}'
# EthTx supports multiple nodes, if one is unavailable, it will use others. You only need to specify them with a comma.
WEB3_NODES=

# ETHERSCAN:
# Etherscan API is used to get contract source code, required for decoding process
# You can get free key here https://etherscan.io/apis
ETHERSCAN_API_KEY=


# OPTIONAL:

# DEFAULT_CHAIN:
# Default chain to use when no chain is specified.
DEFAULT_CHAIN=mainnet

# CACHE_SIZE:
# lru_cache size.
CACHE_SIZE=128

# MONGO_CONNECTION_STRING:
# Those represent data required for connecting to mongoDB. It's used for caching semantics
# used in decoding process. But, it's not neccessary for running, If you don't want to use permanent
# db or setup mongo, leave those values, mongomock package is used to simulate in-memory mongo.
MONGO_CONNECTION_STRING=mongomock://localhost/ethtx

# ETHERSCAN_URLS:
# URLs for etherscan APIs.
# Values are populated from the environment by treating the environment variable's value as a JSON-encoded string.
ETHERSCAN_URLS='{"mainnet": "https://api.etherscan.io/api", "rinkeby": "https://api-rinkeby.etherscan.io/api", "goerli": "https://api-goerli.etherscan.io/api"}'
```

## Getting started

```python
from dotenv import load_dotenv

load_dotenv("<PATH_TO_ENV_FILE>")

from ethtx import EthTx, EthTxConfig
from ethtx.models.decoded_model import DecodedTransaction

ethtx = EthTx.initialize(EthTxConfig)
transaction: DecodedTransaction = ethtx.decoders.decode_transaction(
    '0x50051e0a6f216ab9484c2080001c7e12d5138250acee1f4b7c725b8fb6bb922d')
```

## Features

EthTx most important functions:

1. Raw node data access:

```python
web3provider = ethtx.providers.web3provider

from ethtx.models.w3_model import W3Transaction, W3Block, W3Receipt, W3CallTree

# read raw transaction data directly from the node
w3transaction: W3Transaction = web3provider.get_transaction(
    '0x50051e0a6f216ab9484c2080001c7e12d5138250acee1f4b7c725b8fb6bb922d')
w3block: W3Block = web3provider.get_block(w3transaction.blockNumber)
w3receipt: W3Receipt = web3provider.get_receipt(w3transaction.hash.hex())
w3calls: W3CallTree = web3provider.get_calls(w3transaction.hash.hex())
```

2. ABI decoding:

```python
from ethtx.models.decoded_model import (
    DecodedTransfer,
    DecodedBalance,
    DecodedEvent, DecodedCall,
)
from ethtx.models.objects_model import Transaction, Event, Block, Call

# read the raw transaction from the node
transaction = Transaction.from_raw(
    w3transaction=w3transaction, w3receipt=w3receipt, w3calltree=w3calls
)

# get proxies used in the transaction
proxies = ethtx.decoders.get_proxies(transaction.root_call, "mainnet")

block: Block = Block.from_raw(
    w3block=web3provider.get_block(transaction.metadata.block_number),
    chain_id="mainnet",
)

# decode transaction components
abi_decoded_events: List[Event] = ethtx.decoders.abi_decoder.decode_events(
    transaction.events, block.metadata, transaction.metadata
)
abi_decoded_calls: DecodedCall = ethtx.decoders.abi_decoder.decode_calls(
    transaction.root_call, block.metadata, transaction.metadata, proxies
)
abi_decoded_transfers: List[
    DecodedTransfer
] = ethtx.decoders.abi_decoder.decode_transfers(abi_decoded_calls, abi_decoded_events)
abi_decoded_balances: List[DecodedBalance] = ethtx.decoders.abi_decoder.decode_balances(
    abi_decoded_transfers
)

# decode a single event
raw_event: Event = transaction.events[3]
abi_decoded_event: DecodedEvent = ethtx.decoders.abi_decoder.decode_event(
    raw_event, block.metadata, transaction.metadata
)

# decode a single call
raw_call: Call = transaction.root_call.subcalls[0]
abi_decoded_call: DecodedCall = ethtx.decoders.abi_decoder.decode_call(
    raw_call, block.metadata, transaction.metadata, proxies
)
```

3. Semantic decoding:

```python
from ethtx.models.decoded_model import DecodedTransactionMetadata

# semantically decode transaction components
decoded_metadata: DecodedTransactionMetadata = (
    ethtx.decoders.semantic_decoder.decode_metadata(
        block.metadata, transaction.metadata, "mainnet"
    )
)
decoded_events: List[DecodedEvent] = ethtx.decoders.semantic_decoder.decode_events(
    abi_decoded_events, decoded_metadata, proxies
)

decoded_calls: Call = ethtx.decoders.semantic_decoder.decode_calls(
    abi_decoded_calls, decoded_metadata, proxies
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

# semantically decode a single event
decoded_event: DecodedEvent = ethtx.decoders.semantic_decoder.decode_event(
    abi_decoded_events[0], decoded_metadata, proxies
)
# semantically decode a single call
decoded_call: Call = ethtx.decoders.semantic_decoder.decode_call(
    abi_decoded_calls.subcalls[0], decoded_metadata, proxies
)
```