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

from typing import Dict

from mongoengine import connect
from pymongo import MongoClient

from .decoders.abi.decoder import ABIDecoder
from .decoders.decoder_service import DecoderService
from .decoders.semantic.decoder import SemanticDecoder
from .models.objects_model import Call
from .providers.etherscan_provider import EtherscanProvider
from .providers.semantic_providers.semantics_database import (
    MongoSemanticsDatabase,
    ISemanticsDatabase,
)
from .providers.semantic_providers.semantics_repository import SemanticsRepository
from .providers.web3_provider import Web3Provider
from .utils.validators import assert_tx_hash


class EthTxConfig:
    mongo_connection_string: str
    etherscan_api_key: str
    web3nodes: Dict[str, dict]
    mongo_database: str
    etherscan_urls: Dict[str, str]
    default_chain: str

    def __init__(
        self,
        mongo_connection_string: str,
        mongo_database: str,
        web3nodes: Dict[str, dict],
        etherscan_api_key: str,
        etherscan_urls: Dict[str, str],
        default_chain: str = "mainnet",
    ):
        self.mongo_connection_string = mongo_connection_string
        self.etherscan_api_key = etherscan_api_key
        self.web3nodes = web3nodes
        self.mongo_database = mongo_database
        self.default_chain = default_chain
        self.etherscan_urls = etherscan_urls


class EthTxDecoders:
    semantic_decoder: SemanticDecoder
    abi_decoder: ABIDecoder

    def __init__(
        self,
        semantic_decoder: SemanticDecoder,
        abi_decoder: ABIDecoder,
        decoder_service: DecoderService,
    ):
        self.semantic_decoder = semantic_decoder
        self.abi_decoder = abi_decoder
        self._decoder_service = decoder_service

    def decode_transaction(self, tx_hash: str, chain_id: str = None):
        assert_tx_hash(tx_hash)
        return self._decoder_service.decode_transaction(chain_id, tx_hash)

    def get_proxies(self, call_tree: Call):
        delegations = self._decoder_service.get_delegations(call_tree)
        return self._decoder_service.get_token_proxies(delegations)


class EthTxProviders:
    web3provider: Web3Provider

    def __init__(self, web3provider: Web3Provider):
        self.web3provider = web3provider


class EthTx:
    @staticmethod
    def initialize(config: EthTxConfig):
        default_chain = config.default_chain
        mongo_client: MongoClient = connect(
            config.mongo_database, host=config.mongo_connection_string
        )
        repository = MongoSemanticsDatabase(mongo_client.db)
        web3provider = Web3Provider(
            config.web3nodes, default_chain=config.default_chain
        )
        etherscan = EtherscanProvider(
            config.etherscan_api_key,
            config.etherscan_urls,
            default_chain_id=config.default_chain,
        )

        return EthTx(default_chain, web3provider, repository, etherscan)

    semantics: SemanticsRepository

    def __init__(
        self,
        default_chain: str,
        web3provider: Web3Provider,
        repository: ISemanticsDatabase,
        etherscan: EtherscanProvider,
    ):
        self._default_chain = default_chain
        self._semantics = SemanticsRepository(repository, etherscan, web3provider)
        abi_decoder = ABIDecoder(self.semantics, self._default_chain)
        semantic_decoder = SemanticDecoder(self.semantics, self._default_chain)
        decoder_service = DecoderService(
            abi_decoder, semantic_decoder, web3provider, self._default_chain
        )
        self._decoders = EthTxDecoders(semantic_decoder, abi_decoder, decoder_service)
        self._providers = EthTxProviders(web3provider)

    @property
    def decoders(self) -> EthTxDecoders:
        """EthTx Decoders."""
        return self._decoders

    @property
    def semantics(self) -> SemanticsRepository:
        """EthTx Semantics Repository."""
        return self._semantics

    @property
    def providers(self) -> EthTxProviders:
        """EthTx Providers."""
        return self._providers

    @property
    def default_chain(self) -> str:
        """Default chain."""
        return self._default_chain

    @default_chain.setter
    def default_chain(self, chain: str) -> None:
        """Default chain setter."""
        self._default_chain = chain
