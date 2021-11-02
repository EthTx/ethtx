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
from .models.decoded_model import Proxy, DecodedTransaction
from .models.objects_model import Call
from .providers import EtherscanProvider, Web3Provider, ENSProvider
from .providers.semantic_providers import (
    ISemanticsDatabase,
    SemanticsRepository,
    MongoSemanticsDatabase,
)
from .utils.validators import assert_tx_hash


class EthTxConfig:
    mongo_connection_string: str
    etherscan_api_key: str
    web3nodes: Dict[str, dict]
    etherscan_urls: Dict[str, str]
    default_chain: str

    def __init__(
        self,
        mongo_connection_string: str,
        web3nodes: Dict[str, dict],
        etherscan_api_key: str,
        etherscan_urls: Dict[str, str],
        default_chain: str = "mainnet",
    ):
        self.mongo_connection_string = mongo_connection_string
        self.etherscan_api_key = etherscan_api_key
        self.web3nodes = web3nodes
        self.default_chain = default_chain
        self.etherscan_urls = etherscan_urls


class EthTxDecoders:
    semantic_decoder: SemanticDecoder
    abi_decoder: ABIDecoder

    def __init__(self, decoder_service: DecoderService):
        self._decoder_service = decoder_service
        self.abi_decoder: ABIDecoder = decoder_service.abi_decoder
        self.semantic_decoder: SemanticDecoder = decoder_service.semantic_decoder

    def decode_transaction(
        self, tx_hash: str, chain_id: str = None
    ) -> DecodedTransaction:
        assert_tx_hash(tx_hash)
        return self._decoder_service.decode_transaction(chain_id, tx_hash)

    def get_proxies(self, call_tree: Call, chain_id: str) -> Dict[str, Proxy]:
        delegations = self._decoder_service.get_delegations(call_tree)
        return self._decoder_service.get_proxies(delegations, chain_id)


class EthTxProviders:
    web3provider: Web3Provider
    etherscan_provider: EtherscanProvider
    ens_provider: ENSProvider

    def __init__(
        self,
        web3provider: Web3Provider,
        etherscan_provider: EtherscanProvider,
        ens_provider: ENSProvider,
    ):
        self.web3provider = web3provider
        self.etherscan_provider = etherscan_provider
        self.ens_provider = ens_provider


class EthTx:
    def __init__(
        self,
        default_chain: str,
        database: ISemanticsDatabase,
        web3provider: Web3Provider,
        etherscan_provider: EtherscanProvider,
        ens_provider: ENSProvider,
    ):
        self._default_chain = default_chain
        self._semantics_repository = SemanticsRepository(
            database_connection=database,
            etherscan_provider=etherscan_provider,
            web3provider=web3provider,
            ens_provider=ens_provider,
        )

        abi_decoder = ABIDecoder(self.semantics, self._default_chain)
        semantic_decoder = SemanticDecoder(self.semantics, self._default_chain)
        decoder_service = DecoderService(
            abi_decoder, semantic_decoder, web3provider, self._default_chain
        )
        self._decoders = EthTxDecoders(decoder_service=decoder_service)
        self._providers = EthTxProviders(
            web3provider=web3provider,
            etherscan_provider=etherscan_provider,
            ens_provider=ens_provider,
        )

    @staticmethod
    def initialize(config: EthTxConfig):
        mongo_client: MongoClient = connect(host=config.mongo_connection_string)
        repository = MongoSemanticsDatabase(db=mongo_client.get_database())

        web3provider = Web3Provider(
            nodes=config.web3nodes, default_chain=config.default_chain
        )
        etherscan_provider = EtherscanProvider(
            api_key=config.etherscan_api_key,
            nodes=config.etherscan_urls,
            default_chain_id=config.default_chain,
        )

        ens_provider = ENSProvider

        return EthTx(
            config.default_chain,
            repository,
            web3provider,
            etherscan_provider,
            ens_provider,
        )

    @property
    def decoders(self) -> EthTxDecoders:
        """EthTx Decoders."""
        return self._decoders

    @property
    def semantics(self) -> SemanticsRepository:
        """EthTx Semantics Repository."""
        return self._semantics_repository

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
