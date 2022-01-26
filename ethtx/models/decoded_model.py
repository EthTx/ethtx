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
from typing import List, Any, Optional

from ethtx.models.base_model import BaseModel
from ethtx.models.objects_model import BlockMetadata, TransactionMetadata
from ethtx.models.semantics_model import AddressSemantics, ERC20Semantics


class AddressInfo(BaseModel):
    address: Optional[str]
    name: str
    badge: Optional[str]


class DecodedTransactionMetadata(BaseModel):
    chain_id: Optional[str]
    tx_hash: str
    block_number: Optional[int]
    block_hash: Optional[str]
    timestamp: Optional[datetime]
    gas_price: Optional[int]
    sender: Optional[AddressInfo]
    receiver: Optional[AddressInfo]
    tx_index: int
    tx_value: int
    gas_limit: int
    gas_used: int
    success: bool


class Argument(BaseModel):
    name: str
    type: str
    value: Any


class DecodedEvent(BaseModel):
    chain_id: str
    tx_hash: str
    timestamp: datetime
    contract: AddressInfo
    index: Optional[int]
    call_id: Optional[str]
    event_signature: Optional[str]
    event_name: str
    parameters: List[Argument]
    event_guessed: bool = False


class DecodedCall(BaseModel):
    chain_id: str
    timestamp: datetime
    tx_hash: str
    call_id: Optional[str]
    call_type: str
    from_address: AddressInfo
    to_address: Optional[AddressInfo]
    value: float
    function_signature: str
    function_name: str
    arguments: List[Argument]
    outputs: List[Argument]
    gas_used: Optional[int]
    error: Optional[str]
    status: bool
    indent: int
    subcalls: List[DecodedCall] = []
    function_guessed: bool = False


class DecodedTransfer(BaseModel):
    from_address: AddressInfo
    to_address: AddressInfo
    token_address: Optional[str]
    token_symbol: str
    token_standard: Optional[str]
    value: float


class DecodedBalance(BaseModel):
    holder: AddressInfo
    tokens: List[dict]


class DecodedTransaction(BaseModel):
    block_metadata: BlockMetadata
    metadata: TransactionMetadata
    events: List[DecodedEvent]
    calls: Optional[DecodedCall]
    transfers: List[DecodedTransfer]
    balances: List[DecodedBalance]
    status: bool = False


class Proxy(BaseModel):
    address: str
    name: str
    type: str
    semantics: Optional[List[AddressSemantics]]
    token: Optional[ERC20Semantics]
