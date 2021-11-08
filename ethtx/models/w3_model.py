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

from datetime import datetime
from typing import Optional, List

from ethtx.models._types import THexBytes
from ethtx.models.base_model import BaseModel
from ethtx.models.objects_model import BlockMetadata, TransactionMetadata, Event, Call


class W3Block(BaseModel):
    chain_id: str
    difficulty: int
    extraData: THexBytes
    gasLimit: int
    gasUsed: int
    hash: THexBytes
    logsBloom: THexBytes
    miner: str
    nonce: THexBytes
    number: int
    parentHash: THexBytes
    receiptsRoot: THexBytes
    sha3Uncles: THexBytes
    size: int
    stateRoot: THexBytes
    timestamp: int
    totalDifficulty: int
    transactions: list
    transactionsRoot: THexBytes
    uncles: list

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


class W3Transaction(BaseModel):
    chain_id: str
    blockHash: THexBytes
    blockNumber: int
    from_address: str
    gas: int
    gasPrice: int
    hash: THexBytes
    input: str
    nonce: int
    r: THexBytes
    s: THexBytes
    to: Optional[str]
    transactionIndex: int
    v: int
    value: int

    def to_object(self, w3receipt: W3Receipt) -> TransactionMetadata:
        tx_hash = self.hash.hex()
        block_number = self.blockNumber
        tx_index = self.transactionIndex
        from_address = self.from_address.lower()
        to_address = (
            self.to.lower()
            if self.to
            else w3receipt.contractAddress.lower()
            if w3receipt.contractAddress
            else None
        )
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


class W3Receipt(BaseModel):
    tx_hash: str
    chain_id: str
    blockHash: THexBytes
    blockNumber: int
    contractAddress: Optional[str]
    cumulativeGasUsed: int
    from_address: str
    gasUsed: int
    logsBloom: THexBytes
    root: Optional[str]
    status: int
    to_address: Optional[str]
    transactionHash: THexBytes
    transactionIndex: int
    logs: list = []


class W3Log(BaseModel):
    tx_hash: str
    chain_id: str
    address: str
    blockHash: THexBytes
    blockNumber: int
    data: str
    logIndex: int
    removed: bool
    topics: List[THexBytes]
    transactionHash: THexBytes
    transactionIndex: int

    def to_object(self) -> Event:
        contract = self.address.lower()
        log_index = self.logIndex
        log_data = self.data
        topics = []

        for i, _ in enumerate(self.topics):
            topics.append(self.topics[i].hex())

        return Event(
            contract=contract, topics=topics, log_data=log_data, log_index=log_index
        )


class W3CallTree(BaseModel):
    tx_hash: str
    chain_id: str
    type: str
    from_address: str
    to_address: Optional[str]
    input: str
    output: str
    value: Optional[str]
    time: Optional[str]
    gas: Optional[str]
    gasUsed: Optional[str]
    error: Optional[str]
    calls: list = []

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
