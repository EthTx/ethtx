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
from typing import List, Optional

from pydantic import Field

from ethtx.models.base_model import BaseModel


class BlockMetadata(BaseModel):
    block_number: int
    block_hash: str
    timestamp: datetime
    parent_hash: str
    miner: str
    gas_limit: int
    gas_used: int
    tx_count: int

    # for future use
    canonical: bool = True

    @staticmethod
    def from_raw(w3block) -> BlockMetadata:
        return w3block.to_object()


class TransactionMetadata(BaseModel):
    tx_hash: str
    block_number: int
    gas_price: int
    from_address: str
    to_address: str
    tx_index: int
    tx_value: int
    gas_limit: int
    gas_used: int
    success: bool

    # for future use
    gas_refund: Optional[int]
    return_value: Optional[str]
    exception_error: Optional[str]
    exception_error_type: Optional[str]
    revert_reason: Optional[str]

    @staticmethod
    def from_raw(w3transaction, w3receipt) -> TransactionMetadata:
        return w3transaction.to_object(w3receipt)


class Event(BaseModel):
    contract: Optional[str]
    topics: List[str]
    log_data: Optional[str]
    log_index: Optional[int]

    call_id: Optional[str]

    @staticmethod
    def from_raw(w3log) -> Event:
        return w3log.to_object()


class Call(BaseModel):
    call_type: str
    call_gas: Optional[int]
    from_address: str
    to_address: Optional[str]
    call_value: int
    call_data: str
    return_value: str
    gas_used: Optional[int]
    status: bool
    error: Optional[str]
    subcalls: List[Call] = Field(default_factory=list)

    # for future use
    call_id: Optional[str]
    created_address: Optional[str]
    gas_refund: Optional[int]
    exception_error: Optional[str]
    exception_error_type: Optional[str]
    revert_reason: Optional[str]
    success: Optional[bool]

    @staticmethod
    def from_raw(w3calltree) -> Call:
        return w3calltree.to_object()


Call.update_forward_refs()


class Transaction(BaseModel):
    metadata: TransactionMetadata
    root_call: Call
    events: List[Event]

    @staticmethod
    def from_raw(w3transaction, w3receipt, w3calltree) -> Transaction:
        data = w3transaction.to_object(w3receipt)
        events = [w3log.to_object() for w3log in w3receipt.logs]
        root_call = w3calltree.to_object()
        return Transaction(metadata=data, root_call=root_call, events=events)


class Block(BaseModel):
    chain_id: str
    metadata: BlockMetadata
    transactions: List[Transaction]

    @staticmethod
    def from_raw(chain_id, w3block, w3transactions=None) -> Block:
        data = w3block.to_object()
        if w3transactions:
            transactions = [
                Transaction.from_raw(w3transaction, w3receipt, w3calltree)
                for (w3transaction, w3receipt, w3calltree) in w3transactions
            ]
        else:
            transactions = []

        return Block(chain_id=chain_id, metadata=data, transactions=transactions)
