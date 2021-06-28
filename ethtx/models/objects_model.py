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
from typing import List, Optional


@dataclass
class BlockMetadata:
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


@dataclass
class TransactionMetadata:
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
    gas_refund: int = None
    return_value: str = None
    exception_error: str = None
    exception_error_type: str = None
    revert_reason: str = None

    @staticmethod
    def from_raw(w3transaction, w3receipt) -> TransactionMetadata:
        return w3transaction.to_object(w3receipt)


@dataclass
class Event:
    contract: str
    topics: List[str]
    log_data: Optional[str]
    log_index: int

    # for future use
    call_id: str = None

    @staticmethod
    def from_raw(w3log) -> Event:
        return w3log.to_object()


@dataclass
class Call:
    call_type: str
    call_gas: int
    from_address: str
    to_address: str
    call_value: int
    call_data: str
    return_value: str
    gas_used: int
    status: bool
    error: str
    subcalls: Optional[List[Call]] = field(default_factory=list)

    # for future use
    call_id: str = None
    created_address: str = None
    gas_refund: int = None
    exception_error: str = None
    exception_error_type: str = None
    revert_reason: str = None
    success: bool = None

    @staticmethod
    def from_raw(w3calltree) -> Call:
        return w3calltree.to_object()


@dataclass
class Block:
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


@dataclass
class Transaction:
    metadata: TransactionMetadata
    root_call: Call
    events: List[Event]

    @staticmethod
    def from_raw(w3transaction, w3receipt, w3calltree) -> Transaction:
        data = w3transaction.to_object(w3receipt)
        events = [w3log.to_object() for w3log in w3receipt.logs]
        root_call = w3calltree.to_object()
        return Transaction(metadata=data, root_call=root_call, events=events)
