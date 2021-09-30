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

from abc import ABC
from typing import Dict, Optional, Any, List

import bson
from pymongo.cursor import Cursor
from pymongo.database import Database as MongoDatabase


class ISemanticsDatabase(ABC):
    """Semantics Database. Represents raw interface required to be
    implemented by a database that provides persistent
    data about semantics"""

    def get_address_semantics(self, chain_id: str, address: str) -> Optional[Dict]:
        ...

    def get_contract_semantics(self, code_hash: str) -> Optional[Dict]:
        ...

    def get_signature_semantics(self, signature_hash: str) -> Optional[List[Dict]]:
        ...

    def insert_contract(self, contract: dict, update_if_exist: bool = False) -> Any:
        ...

    def insert_address(self, address: dict, update_if_exist: bool = False) -> Any:
        ...

    def insert_signature(self, signature, update_if_exist: bool = False) -> Any:
        ...


class MongoCollections:
    ADDRESSES = "addresses"
    CONTRACTS = "contracts"
    SIGNATURES = "signatures"


class MongoSemanticsDatabase(ISemanticsDatabase):
    def get_collection_count(self):
        return len(self._db.list_collection_names())

    def __init__(self, db: MongoDatabase):
        self._db = db
        self._addresses = self._db["addresses"]
        self._contracts = self._db["contracts"]
        self._signatures = self._db["signatures"]

    def get_address_semantics(self, chain_id, address) -> Optional[Dict]:
        _id = f"{chain_id}-{address}"
        return self._addresses.find_one({"_id": _id}, {"_id": 0})

    def get_signature_semantics(self, signature_hash: str) -> Cursor:
        return self._signatures.find({"signature_hash": signature_hash})

    def insert_signature(
        self, signature: dict, update_if_exist=False
    ) -> Optional[bson.ObjectId]:
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

    def get_contract_semantics(self, code_hash):
        """Contract hashes are always the same, no mather what chain we use, so there is no need
        to use chain_id"""
        return self._contracts.find_one({"_id": code_hash}, {"_id": 0})

    def insert_contract(
        self, contract, update_if_exist=False
    ) -> Optional[bson.ObjectId]:
        contract_with_id = {"_id": contract["code_hash"], **contract}

        if update_if_exist:
            updated_contract = self._contracts.replace_one(
                {"_id": contract_with_id["_id"]}, contract_with_id, upsert=True
            )

            return (
                None
                if updated_contract.modified_count
                else updated_contract.upserted_id
            )

        inserted_contract = self._contracts.insert_one(contract_with_id)
        return inserted_contract.inserted_id

    def insert_address(self, address, update_if_exist=False) -> Optional[bson.ObjectId]:
        address_with_id = {
            "_id": f"{address['chain_id']}-{address['address']}",
            **address,
        }

        if update_if_exist:
            updated_address = self._addresses.replace_one(
                {"_id": address_with_id["_id"]}, address_with_id, upsert=True
            )
            return (
                None if updated_address.modified_count else updated_address.upserted_id
            )

        inserted_address = self._addresses.insert_one(address_with_id)
        return inserted_address.inserted_id
