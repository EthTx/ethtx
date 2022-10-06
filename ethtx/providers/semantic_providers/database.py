# Copyright 2021 DAI FOUNDATION (the original version https://github.com/daifoundation/ethtx_ce)
# Copyright 2021-2022 Token Flow Insights SA (modifications to the original software as recorded
# in the changelog https://github.com/EthTx/ethtx/blob/master/CHANGELOG.md)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.
#
# The product contains trademarks and other branding elements of Token Flow Insights SA which are
# not licensed under the Apache 2.0 license. When using or reproducing the code, please remove
# the trademark and/or other branding elements.

import logging
from typing import Dict, Optional

from bson import ObjectId
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from pymongo.database import Database as MongoDatabase

from .base import ISemanticsDatabase
from .const import MongoCollections
from ...utils.cache_tools import cache

log = logging.getLogger(__name__)


class MongoSemanticsDatabase(ISemanticsDatabase):
    _db: MongoDatabase

    _addresses: Collection
    _contracts: Collection
    _signatures: Collection

    def __init__(self, db: MongoDatabase):
        self._db = db

        self._addresses = None
        self._contracts = None
        self._signatures = None

        self._init_collections()

    def get_collection_count(self) -> int:
        return len(self._db.list_collection_names())

    @cache
    def get_address_semantics(self, chain_id: str, address: str) -> Dict:
        return self._addresses.find_one({"chain_id": chain_id, "address": address})

    def get_signature_semantics(self, signature_hash: str) -> Cursor:
        return self._signatures.find({"signature_hash": signature_hash})

    def insert_signature(
        self, signature: dict, update_if_exist: Optional[bool] = False
    ) -> Optional[ObjectId]:
        if update_if_exist:
            updated_signature = self._signatures.replace_one(
                {"_id": signature["_id"]}, signature, upsert=True
            )
            return (
                None
                if updated_signature.modified_count
                else updated_signature.upserted_id
            )

        inserted_signature = self._signatures.insert_one(signature)
        return inserted_signature.inserted_id

    @cache
    def get_contract_semantics(self, code_hash: str) -> Dict:
        """Contract hashes are always the same, no mather what chain we use, so there is no need
        to use chain_id"""
        return self._contracts.find_one({"code_hash": code_hash})

    def insert_contract(
        self, contract: Dict, update_if_exist: Optional[bool] = False
    ) -> Optional[ObjectId]:

        if update_if_exist:
            updated_contract = self._contracts.replace_one(
                {"code_hash": contract["code_hash"]}, contract, upsert=True
            )

            return (
                None
                if updated_contract.modified_count
                else updated_contract.upserted_id
            )

        inserted_contract = self._contracts.insert_one(contract)
        return inserted_contract.inserted_id

    def insert_address(
        self, address: Dict, update_if_exist: Optional[bool] = False
    ) -> Optional[ObjectId]:

        if update_if_exist:
            updated_address = self._addresses.replace_one(
                {"chain_id": address["chain_id"], "address": address["address"]},
                address,
                upsert=True,
            )
            return (
                None if updated_address.modified_count else updated_address.upserted_id
            )

        inserted_address = self._addresses.insert_one(address)
        return inserted_address.inserted_id

    def _init_collections(self) -> None:
        for mongo_collection in MongoCollections:
            self.__setattr__(f"_{mongo_collection}", self._db[mongo_collection])

    def delete_semantics_by_address(self, chain_id: str, address: str) -> None:

        address_semantics = self.get_address_semantics(chain_id, address)

        if not address_semantics:
            return

        codehash = address_semantics["contract"]
        # contract_semantics = self.get_contract_semantics(codehash)

        self._addresses.delete_one({"chain_id": chain_id, "address": address})
        self._contracts.delete_one({"code_hash": codehash})

        self.get_contract_semantics.cache_clear()
        self.get_address_semantics.cache_clear()
