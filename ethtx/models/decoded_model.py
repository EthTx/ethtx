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
from ethtx.models.objects_model import BlockMetadata
from ethtx.models.semantics_model import AddressSemantics, ERC20Semantics
from ethtx.utils.pickable import JsonObject


class AddressInfo(BaseModel):
    address: str
    name: str
    badge: Optional[str]


class DecodedTransactionMetadata(BaseModel):
    chain_id: str
    tx_hash: str
    block_number: int
    block_hash: str
    timestamp: datetime
    gas_price: int
    sender: AddressInfo
    receiver: AddressInfo
    tx_index: int
    tx_value: int
    eth_price: float
    gas_limit: int
    gas_used: int
    success: bool


class Argument(BaseModel):
    name: str
    type: str
    value: Any


class DecodedEvent(JsonObject):
    chain_id: str
    tx_hash: str
    timestamp: datetime
    contract: AddressInfo
    index: int
    call_id: str
    event_signature: str
    event_name: str
    parameters: List[Argument]

    def __init__(
        self,
        chain_id: str,
        tx_hash: str,
        timestamp: datetime,
        contract_address: str,
        contract_name: str,
        index: int,
        call_id: str,
        event_signature: str,
        event_name: str,
        parameters: List[Argument],
    ):
        self.chain_id = chain_id
        self.tx_hash = tx_hash
        self.timestamp = timestamp
        self.contract = AddressInfo(address=contract_address, name=contract_name)
        self.contract_name = contract_name
        self.index = index
        self.call_id = call_id
        self.event_signature = event_signature
        self.event_name = event_name
        self.parameters = parameters

    def __eq__(self, other):
        if isinstance(other, DecodedEvent):
            return (
                self.chain_id == other.chain_id
                and self.tx_hash == other.tx_hash
                and self.timestamp == other.timestamp
                and self.contract == other.contract
                and self.contract_name == other.contract_name
                and self.index == other.index
                and self.call_id == other.call_id
                and self.event_signature == other.event_signature
                and self.event_name == other.event_name
                and self.parameters == other.parameters
            )
        return False


class DecodedCall(JsonObject):
    chain_id: str
    timestamp: datetime
    tx_hash: str
    call_id: str
    call_type: str
    from_address: AddressInfo
    to_address: AddressInfo
    value: int
    function_signature: str
    function_name: str
    arguments: List[Argument]
    outputs: List[Argument]
    gas_used: int
    error: str
    status: bool
    subcalls: List[DecodedCall]

    def __init__(
        self,
        chain_id: str,
        tx_hash: str,
        timestamp: datetime,
        call_id: str,
        call_type: str,
        from_address: str,
        from_name: str,
        to_address: str,
        to_name: str,
        value: int,
        function_signature: str,
        function_name: str,
        arguments: List[Argument],
        outputs: List[Argument],
        gas_used: int,
        error: str,
        status: bool,
        indent: int,
        subcalls: Optional[List[DecodedCall]] = None,
    ):
        self.chain_id = chain_id
        self.tx_hash = tx_hash
        self.timestamp = timestamp
        self.call_id = call_id
        self.call_type = call_type
        self.from_address = AddressInfo(address=from_address, name=from_name)
        self.to_address = AddressInfo(address=to_address, name=to_name)
        self.to_name = to_name
        self.value = value
        self.function_signature = function_signature
        self.function_name = function_name
        self.arguments = arguments
        self.outputs = outputs
        self.gas_used = gas_used
        self.error = error
        self.status = status
        self.indent = indent
        self.subcalls = subcalls if subcalls else []

    def __eq__(self, other):
        if isinstance(other, DecodedCall):
            return (
                self.chain_id == other.chain_id
                and self.tx_hash == other.tx_hash
                and self.timestamp == other.timestamp
                and self.call_type == other.call_type
                and self.from_address == other.from_address
                and self.to_address == other.to_address
                and self.to_name == other.to_name
                and self.value == other.value
                and self.function_signature == other.function_signature
                and self.function_name == other.function_name
                and self.arguments == other.arguments
                and self.outputs == other.outputs
                and self.gas_used == other.gas_used
                and self.error == other.error
                and self.status == other.status
                and self.subcalls == other.subcalls
            )

        return False


class DecodedTransfer(JsonObject):
    from_address: AddressInfo
    to_address: AddressInfo
    token_address: Optional[str]
    token_symbol: str
    token_standard: Optional[str]
    value: float

    def __init__(
        self,
        from_address: AddressInfo,
        to_address: AddressInfo,
        token_standard: Optional[str],
        token_address: Optional[str],
        token_symbol: str,
        value: float,
    ):
        self.from_address = from_address
        self.to_address = to_address
        self.token_address = token_address
        self.token_symbol = token_symbol
        self.token_standard = token_standard
        self.value = value


class DecodedBalance(JsonObject):
    holder: AddressInfo
    tokens: List[dict]

    def __init__(self, holder: AddressInfo, tokens: List[dict]):
        self.holder = holder
        self.tokens = tokens


class DecodedTransaction(JsonObject):
    block_metadata: BlockMetadata
    metadata: DecodedTransactionMetadata
    events: List[DecodedEvent]
    calls: Optional[DecodedCall]
    transfers: List[DecodedTransfer]
    balances: List[DecodedBalance]
    status: bool

    def __init__(
        self,
        block_metadata: BlockMetadata,
        tx_metadata: DecodedTransactionMetadata,
        events: List[DecodedEvent],
        calls: Optional[DecodedCall],
        transfers: List[DecodedTransfer],
        balances: List[DecodedBalance],
    ):
        self.block_metadata = block_metadata
        self.metadata = tx_metadata
        self.events = events
        self.calls = calls
        self.transfers = transfers
        self.balances = balances
        self.status = False


class Proxy:
    address: str
    name: str
    type: str
    semantics: Optional[List[AddressSemantics]]
    token: Optional[ERC20Semantics]

    def __init__(
        self,
        address: str,
        name: str,
        type: str,
        semantics: Optional[List[AddressSemantics]] = None,
        token: Optional[ERC20Semantics] = None,
    ):
        self.address = address
        self.name = name
        self.type = type
        self.semantics = semantics
        self.token = token
