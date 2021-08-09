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

import logging
import os
from functools import lru_cache
from typing import List, Dict, Optional

from web3 import Web3
from web3.datastructures import AttributeDict
from web3.middleware import geth_poa_middleware
from web3.types import BlockData, TxData, TxReceipt, HexStr

from ..exceptions import Web3ConnectionException, ProcessingException
from ..models.objects_model import (
    Block,
    Transaction,
    BlockMetadata,
    TransactionMetadata,
    Call,
)
from ..models.w3_model import W3Block, W3Transaction, W3Receipt, W3CallTree, W3Log
from ..semantics.standards import erc20

log = logging.getLogger(__name__)


def connect_chain(
    http_hook: str = None,
    ipc_hook: str = None,
    ws_hook: str = None,
    poa: bool = False
) -> Web3 or None:
    if http_hook:
        method = "HTTP"
        provider = Web3.HTTPProvider
        hook = http_hook
    elif ipc_hook:
        method = "IPC"
        provider = Web3.IPCProvider
        hook = ipc_hook
    elif ws_hook:
        method = "Websocket"
        provider = Web3.WebsocketProvider
        hook = ws_hook
    else:
        method = "IPC"
        provider = Web3.IPCProvider
        hook = "\\\\.\\pipe\\geth.ipc"

    try:
        w3 = Web3(provider(hook, request_kwargs={"timeout": 600}))

        # middleware injection for POA chains
        if poa:
            w3.middleware_onion.inject(geth_poa_middleware, layer=0)

        if w3.isConnected():
            log.info(
                "Connected to %s: %s with latest block %s.",
                method,
                hook,
                w3.eth.block_number,
            )
            return w3
        else:
            log.info("%s connection to %s failed.", method, hook)
            raise Web3ConnectionException()
    except Exception as exc:
        log.warning("Node connection %s: %s failed.", method, hook, exc_info=exc)
        raise


class NodeDataProvider:

    default_chain: str

    def __init__(self, default_chain=None):
        self.default_chain = default_chain

    def get_block(
        self, block_number: int, chain_id: Optional[str] = None
    ) -> BlockMetadata:
        ...

    def get_transaction(
        self, tx_hash: str, chain_id: Optional[str] = None
    ) -> TransactionMetadata:
        ...

    def get_full_transaction(
        self, tx_hash: str, chain_id: Optional[str] = None
    ) -> Transaction:
        ...

    def get_calls(self, tx_hash: str, chain_id: Optional[str] = None) -> Call:
        ...


class Web3Provider(NodeDataProvider):
    chain: Web3

    def __init__(self, nodes: Dict[str, str], default_chain=None):
        super().__init__(default_chain)
        self.nodes = nodes

    def _get_node_connection(self, chain_id: Optional[str] = None) -> Web3:
        chain_id = chain_id or self.default_chain

        if chain_id is None:
            raise ProcessingException(
                "chain_id must be provided as an argument or constructor default"
            )

        if chain_id not in self.nodes:
            raise ProcessingException(
                "unknown chain_id, it must be defined in the EthTxConfig object"
            )

        return connect_chain(http_hook=self.nodes[chain_id]['hook'], poa=self.nodes[chain_id]['poa'])

    # get the raw block data from the node
    @lru_cache(maxsize=512)
    def get_block(self, block_number: int, chain_id: Optional[str] = None) -> W3Block:
        chain = self._get_node_connection(chain_id)
        raw_block: BlockData = chain.eth.get_block(block_number)
        block = W3Block(
            chain_id=chain_id or self.default_chain,
            difficulty=raw_block.difficulty,
            extraData=raw_block.get('extraData', None),
            gasLimit=raw_block.gasLimit,
            gasUsed=raw_block.gasUsed,
            hash=raw_block.hash,
            logsBloom=raw_block.logsBloom,
            miner=raw_block.miner,
            nonce=raw_block.get("nonce", 0),
            number=raw_block.number,
            parentHash=raw_block.parentHash,
            receiptsRoot=raw_block.receiptsRoot,
            sha3Uncles=raw_block.sha3Uncles,
            size=raw_block.size,
            stateRoot=raw_block.stateRoot,
            timestamp=raw_block.timestamp,
            totalDifficulty=raw_block.totalDifficulty,
            transactions=raw_block.transactions,
            transactionsRoot=raw_block.transactionsRoot,
            uncles=raw_block.uncles,
        )

        return block

    # get the raw transaction data from the node
    @lru_cache(maxsize=512)
    def get_transaction(
        self, tx_hash: str, chain_id: Optional[str] = None
    ) -> W3Transaction:
        chain = self._get_node_connection(chain_id)
        raw_tx: TxData = chain.eth.get_transaction(HexStr(tx_hash))
        transaction = W3Transaction(
            chain_id=chain_id or self.default_chain,
            blockHash=raw_tx.blockHash,
            blockNumber=raw_tx.blockNumber,
            from_address=raw_tx["from"],
            gas=raw_tx.gas,
            gasPrice=raw_tx.gasPrice,
            hash=raw_tx.hash,
            input=raw_tx.input,
            nonce=raw_tx.nonce,
            r=raw_tx.r,
            s=raw_tx.s,
            to=raw_tx.to,
            transactionIndex=raw_tx.transactionIndex,
            v=raw_tx.v,
            value=raw_tx.value,
        )

        return transaction

    @lru_cache(maxsize=512)
    def get_receipt(self, tx_hash: str, chain_id: Optional[str] = None) -> W3Receipt:
        chain = self._get_node_connection(chain_id)
        raw_receipt: TxReceipt = chain.eth.get_transaction_receipt(tx_hash)
        _root = raw_receipt.root if hasattr(raw_receipt, "root") else None

        _logs = [
            W3Log(
                tx_hash=tx_hash,
                chain_id=chain_id or self.default_chain,
                address=_log.address,
                blockHash=_log.blockHash,
                blockNumber=_log.blockNumber,
                data=_log.data,
                logIndex=_log.logIndex,
                removed=_log.removed,
                topics=_log.topics,
                transactionHash=_log.transactionHash,
                transactionIndex=_log.transactionIndex,
            )
            for _log in raw_receipt.logs
        ]

        receipt = W3Receipt(
            tx_hash=tx_hash,
            chain_id=chain_id or self.default_chain,
            blockHash=raw_receipt.blockHash,
            blockNumber=raw_receipt.blockNumber,
            contractAddress=raw_receipt.contractAddress,
            cumulativeGasUsed=raw_receipt.cumulativeGasUsed,
            from_address=raw_receipt["from"],
            gasUsed=raw_receipt.gasUsed,
            logs=_logs,
            logsBloom=raw_receipt.logsBloom,
            root=_root,
            status=raw_receipt.get('status', True),
            to_address=raw_receipt.to,
            transactionHash=raw_receipt.transactionHash,
            transactionIndex=raw_receipt.transactionIndex,
        )

        return receipt

    @staticmethod
    def _get_custom_calls_tracer():
        return open(os.path.join(os.path.dirname(__file__), "static/tracer.js")).read()

    @lru_cache(maxsize=512)
    def get_calls(self, tx_hash: str, chain_id: Optional[str] = None) -> W3CallTree:
        # tracer is a temporary fixed implementation of geth tracer
        chain = self._get_node_connection(chain_id)
        tracer = self._get_custom_calls_tracer()
        response = chain.manager.request_blocking(
            "debug_traceTransaction", [tx_hash, {"tracer": tracer}]
        )

        return self._create_call_from_debug_trace_tx(
            tx_hash, chain_id or self.default_chain, response
        )

    # get the contract bytecode hash from the node
    @lru_cache(maxsize=512)
    def get_code_hash(
        self, contract_address: str, chain_id: Optional[str] = None
    ) -> str:
        chain = self._get_node_connection(chain_id)
        byte_code = chain.eth.get_code(Web3.toChecksumAddress(contract_address))
        code_hash = Web3.keccak(byte_code).hex()
        return code_hash

    # get the erc20 token data from the node
    def get_erc20_token(
        self,
        token_address: str,
        contract_name: str,
        functions,
        chain_id: Optional[str] = None,
    ):

        name_abi = symbol_abi = decimals_abi = ""

        if functions:
            for function in functions.values():
                if (
                    function.name == "name"
                    and len(function.inputs) == 0
                    and len(function.outputs) == 1
                ):
                    name_type = function.outputs[0].parameter_type
                    name_abi = (
                        '{"name":"name", "constant":true, "payable":false, "type":"function", '
                        ' "inputs":[], "outputs":[{"name":"","type":"%s"}]}' % name_type
                    )

                elif (
                    function.name == "symbol"
                    and len(function.inputs) == 0
                    and len(function.outputs) == 1
                ):
                    symbol_type = function.outputs[0].parameter_type
                    symbol_abi = (
                        '{"name":"symbol", "constant":true, "payable":false,"type":"function", '
                        ' "inputs":[], "outputs":[{"name":"","type":"%s"}]}'
                        % symbol_type
                    )

                elif (
                    function.name in ["decimals", "dec"]
                    and len(function.inputs) == 0
                    and len(function.outputs) == 1
                ):
                    decimals_type = function.outputs[0].parameter_type
                    decimals_abi = (
                        '{"name":"decimals", "constant":true, "payable":false,"type":"function", '
                        ' "inputs":[], "outputs":[{"name":"","type":"%s"}]}'
                        % decimals_type
                    )

        abi = f'[{",".join([name_abi, symbol_abi, decimals_abi])}]'

        try:
            chain = self._get_node_connection(chain_id)
            token = chain.eth.contract(
                address=Web3.toChecksumAddress(token_address), abi=abi
            )
            name = token.functions.name().call() if name_abi else contract_name
            if type(name) == bytes:
                name = name.decode("utf-8").replace("\x00", "")

            symbol = token.functions.symbol().call() if symbol_abi else contract_name
            if type(symbol) == bytes:
                symbol = symbol.decode("utf-8").replace("\x00", "")

            decimals = token.functions.decimals().call() if decimals_abi else 18
        except Exception:
            name = symbol = contract_name
            decimals = 18

        return dict(address=token_address, symbol=symbol, name=name, decimals=decimals)

    # guess if the contract is and erc20 token and get the data
    @lru_cache(maxsize=512)
    def guess_erc20_token(self, contract_address, chain_id: Optional[str] = None):
        chain = self._get_node_connection(chain_id)

        byte_code = chain.eth.get_code(Web3.toChecksumAddress(contract_address)).hex()

        if all(
            "63" + signature[2:] in byte_code
            for signature in (
                erc20.erc20_transfer_function.signature,
                erc20.erc20_transferFrom_function.signature,
                erc20.erc20_approve_function.signature,
            )
        ) and all(
            signature[2:] in byte_code
            for signature in (
                erc20.erc20_transfer_event.signature,
                erc20.erc20_approval_event.signature,
            )
        ):

            name_abi = (
                '{"name":"name", "constant":true, "payable":false,'
                ' "type":"function", "inputs":[], "outputs":[{"name":"","type":"string"}]}'
            )
            symbol_abi = (
                '{"name":"symbol", "constant":true, "payable":false,'
                '"type":"function", "inputs":[], "outputs":[{"name":"","type":"string"}]}'
            )
            decimals_abi = (
                '{"name":"decimals", "constant":true, "payable":false,'
                '"type":"function",  "inputs":[], "outputs":[{"name":"","type":"uint8"}]}'
            )

            abi = f'[{",".join([name_abi, symbol_abi, decimals_abi])}]'

            try:
                token = chain.eth.contract(
                    address=Web3.toChecksumAddress(contract_address), abi=abi
                )
                name = token.functions.name().call()
                symbol = token.functions.symbol().call()
                decimals = token.functions.decimals().call()

                return dict(
                    address=contract_address,
                    symbol=symbol,
                    name=name,
                    decimals=decimals,
                )

            except Exception:
                pass

        return None

    # guess if the contract is and erc20 token proxy and get the data
    @lru_cache(maxsize=512)
    def guess_erc20_proxy(self, contract_address, chain_id: Optional[str] = None):
        chain = self._get_node_connection(chain_id)

        name_abi = (
            '{"name":"name", "constant":true, "payable":false,'
            ' "type":"function", "inputs":[], "outputs":[{"name":"","type":"string"}]}'
        )
        symbol_abi = (
            '{"name":"symbol", "constant":true, "payable":false,'
            '"type":"function", "inputs":[], "outputs":[{"name":"","type":"string"}]}'
        )
        decimals_abi = (
            '{"name":"decimals", "constant":true, "payable":false,'
            '"type":"function",  "inputs":[], "outputs":[{"name":"","type":"uint8"}]}'
        )

        abi = f'[{",".join([name_abi, symbol_abi, decimals_abi])}]'

        try:
            token = chain.eth.contract(
                address=Web3.toChecksumAddress(contract_address), abi=abi
            )
            name = token.functions.name().call()
            symbol = token.functions.symbol().call()
            decimals = token.functions.decimals().call()

            return dict(symbol=symbol, name=name, decimals=decimals)

        except Exception:
            pass

        return None

    @staticmethod
    def _create_call_from_debug_trace_tx(
        tx_hash: str, chain_id: str, input_rpc: AttributeDict
    ) -> W3CallTree:
        def prep_raw_dict(dct: [AttributeDict, Dict]):
            if not isinstance(dct, dict):
                dct = dct.__dict__
            dct["from_address"] = dct.pop("from", None)
            dct["to_address"] = dct.pop("to", None)
            dct["input"] = dct.pop("input", "0x")
            dct["output"] = dct.pop("output", "0x")
            calls = dct.pop("calls", [])
            return dct, calls

        obj = input_rpc.__dict__
        tmp_call_tree = []

        w3input, main_parent_calls = prep_raw_dict(obj)
        main_parent = W3CallTree(tx_hash, chain_id, **w3input)
        for main_parent_call in main_parent_calls:
            w3input, main_parent_calls = prep_raw_dict(main_parent_call)
            main_parent_child = W3CallTree(tx_hash, chain_id, **w3input)
            main_parent.calls.append(main_parent_child)
            if len(main_parent_calls) > 0:
                tmp_call_tree.append(
                    {"parent": main_parent_child, "children": main_parent_calls}
                )

        while len(tmp_call_tree) != 0:
            new_call_tree = []

            for pair in tmp_call_tree:

                parent_call: W3CallTree = pair["parent"]
                child_calls: List = pair["children"]

                if child_calls is not None:
                    for child_call in child_calls:
                        w3input, child_child_call = prep_raw_dict(child_call)
                        child = W3CallTree(tx_hash, chain_id, **w3input)
                        parent_call.calls.append(child)

                        if len(child_call) > 0:
                            new_call_tree.append(
                                {"parent": child, "children": child_child_call}
                            )

            tmp_call_tree = new_call_tree

        return main_parent

    @lru_cache(maxsize=512)
    def get_full_block(self, block_number: int, chain_id: Optional[str] = None):

        w3block = self.get_block(block_number, chain_id)
        w3transactions = [
            (
                self.get_transaction(tx_hash.hex(), chain_id),
                self.get_receipt(tx_hash.hex(), chain_id),
                self.get_calls(tx_hash.hex(), chain_id),
            )
            for tx_hash in w3block.transactions
        ]

        return Block.from_raw(
            chain_id=chain_id or self.default_chain,
            w3block=w3block,
            w3transactions=w3transactions,
        )

    @lru_cache(maxsize=512)
    def get_full_transaction(self, tx_hash: str, chain_id: Optional[str] = None):

        w3transaction = self.get_transaction(tx_hash, chain_id)
        w3receipt = self.get_receipt(tx_hash, chain_id)
        w3calltree = self.get_calls(tx_hash, chain_id)

        return Transaction.from_raw(
            w3transaction=w3transaction, w3receipt=w3receipt, w3calltree=w3calltree
        )
