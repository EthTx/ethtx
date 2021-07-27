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

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from hexbytes import HexBytes

from ethtx.models.objects_model import BlockMetadata, TransactionMetadata, Event, Call


@dataclass
class W3Block:
    chain_id: str
    difficulty: int
    extraData: HexBytes
    gasLimit: int
    gasUsed: int
    hash: HexBytes
    logsBloom: HexBytes
    miner: str
    nonce: HexBytes
    number: int
    parentHash: HexBytes
    receiptsRoot: HexBytes
    sha3Uncles: HexBytes
    size: int
    stateRoot: HexBytes
    timestamp: int
    totalDifficulty: int
    transactions: List
    transactionsRoot: HexBytes
    uncles: List

    def to_object(self) -> BlockMetadata:
        block_hash = self.hash.hex()
        timestamp = datetime.utcfromtimestamp(self.timestamp)
        parent_hash = self.parentHash.hex()
        miner = self.miner.lower()
        gas_limit = self.gasLimit
        gas_used = self.gasUsed
        tx_count = len(self.transactions)

        return BlockMetadata(
            block_number=self.number,
            block_hash=block_hash,
            timestamp=timestamp,
            parent_hash=parent_hash,
            miner=miner,
            gas_limit=gas_limit,
            gas_used=gas_used,
            tx_count=tx_count,
        )


@dataclass
class W3Transaction:
    chain_id: str
    blockHash: str
    blockNumber: int
    from_address: str
    gas: int
    gasPrice: int
    hash: HexBytes
    input: str
    nonce: int
    r: HexBytes
    s: HexBytes
    to: str
    transactionIndex: int
    v: int
    value: int

    def to_object(self, w3receipt: W3Receipt) -> TransactionMetadata:
        tx_hash = self.hash.hex()
        block_number = self.blockNumber
        tx_index = self.transactionIndex
        from_address = self.from_address.lower()
        to_address = self.to.lower() if self.to else w3receipt.contractAddress.lower() if w3receipt.contractAddress else None
        tx_value = self.value
        gas_limit = self.gas
        gas_price = self.gasPrice
        gas_used = w3receipt.gasUsed
        success = w3receipt.status == 1

        return TransactionMetadata(
            tx_hash=tx_hash,
            block_number=block_number,
            tx_index=tx_index,
            from_address=from_address,
            to_address=to_address,
            tx_value=tx_value,
            gas_limit=gas_limit,
            gas_price=gas_price,
            gas_used=gas_used,
            success=success,
        )


@dataclass
class W3Receipt:
    tx_hash: str
    chain_id: str
    blockHash: HexBytes
    blockNumber: int
    contractAddress: str
    cumulativeGasUsed: int
    from_address: str
    gasUsed: int
    logsBloom: HexBytes
    root: str
    status: int
    to_address: str
    transactionHash: HexBytes
    transactionIndex: int
    logs: list = field(default_factory=list)


@dataclass
class W3Log:
    tx_hash: str
    chain_id: str
    address: str
    blockHash: HexBytes
    blockNumber: int
    data: str
    logIndex: int
    removed: bool
    topics: List[HexBytes]
    transactionHash: HexBytes
    transactionIndex: int

    def to_object(self) -> Event:
        contract = self.address.lower()
        log_index = self.logIndex
        log_data = self.data
        topics = []

        for i in range(len(self.topics)):
            topics.append(self.topics[i].hex())

        return Event(
            contract=contract, topics=topics, log_data=log_data, log_index=log_index
        )


@dataclass
class W3CallTree:
    tx_hash: str
    chain_id: str
    type: str
    from_address: str
    to_address: str
    input: str
    output: str
    value: str = None
    time: str = None
    gas: str = None
    gasUsed: str = None
    error: str = None
    calls: list = field(default_factory=list)

    def to_object(self) -> Call:
        from_address = self.from_address
        to_address = self.to_address
        call_value = int(self.value, 16) if self.value else 0
        call_type = self.type.lower()
        call_data = self.input
        return_value = self.output
        gas_used = int(self.gasUsed, 16) if self.gasUsed else None
        call_gas = int(self.gas, 16) if self.gas else None
        status = self.error is None
        error = self.error

        call = Call(
            call_type=call_type,
            from_address=from_address,
            to_address=to_address,
            call_value=call_value,
            call_data=call_data,
            return_value=return_value,
            gas_used=gas_used,
            call_gas=call_gas,
            status=status,
            error=error,
        )

        for child_call in self.calls:
            call.subcalls.append(child_call.to_object())

        return call
