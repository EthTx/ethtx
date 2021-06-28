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
from typing import Dict, Optional

from pymongo.database import Database as MongoDatabase


class ISemanticsDatabase(ABC):
    """Semantics Database. Represents raw interface required to be
    implemented by a database that provides persistent
    data about semantics"""

    def get_address_semantics(self, chain_id: str, address: str) -> Optional[Dict]:
        ...

    def get_contract_semantics(self, code_hash: str) -> Optional[Dict]:
        ...

    def get_signature_semantics(self, signature_hash: str) -> Optional[Dict]:
        ...

    def insert_contract(self, contract: dict, update_if_exist: bool = False):
        ...

    def insert_address(self, address_data: dict, update_if_exist: bool = False):
        ...

    def insert_signature(self, signature, update_if_exist: bool = False):
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

    def get_signature_semantics(self, signature_hash):
        return self._signatures.find_one({"_id": signature_hash}, {"_id": 0})

    def get_contract_semantics(self, code_hash):
        """Contract hashes are always the same, no mather what chain we use, so there is no need
        to use chain_id"""
        return self._contracts.find_one({"_id": code_hash}, {"_id": 0})

    def insert_contract(self, contract, update_if_exist=False):
        contract_with_id = {"_id": contract["code_hash"], **contract}

        if update_if_exist:
            self._contracts.replace_one(
                {"_id": contract_with_id["_id"]}, contract_with_id, upsert=True
            )
        else:
            self._contracts.insert_one(contract_with_id)

    def insert_address(self, address, update_if_exist=False):
        address_with_id = {
            "_id": f"{address['chain_id']}-{address['address']}",
            **address,
        }

        if update_if_exist:
            self._addresses.replace_one(
                {"_id": address_with_id["_id"]}, address_with_id, upsert=True
            )
        else:
            self._addresses.insert_one(address_with_id)

    def insert_signature(self, signature, update_if_exist=False):
        signature_with_id = {"_id": signature["hash"], **signature}

        if update_if_exist:
            self._signatures.replace_one(
                {"_id": signature_with_id["_id"]}, signature_with_id, upsert=True
            )
        else:
            self._signatures.insert_one(signature_with_id)
