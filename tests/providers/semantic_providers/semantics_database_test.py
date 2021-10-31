from mongomock import Database

from ethtx.providers.semantic_providers.const import MongoCollections


class TestMongoSemanticsDatabase:
    def test_no_address_semantics(self, mongo_semantics_database):
        sema = mongo_semantics_database.get_address_semantics("mainnet", "not_existing")
        assert not sema

    def test_save_and_get_contract_semantic(
        self, mongo_semantics_database, mongo_db: Database
    ):
        code_hash = "test_code_hash"
        contract_data = {"code_hash": code_hash, "chain_id": "mainnet"}

        try:
            assert (
                0
                == mongo_db.get_collection(
                    MongoCollections.CONTRACTS
                ).estimated_document_count()
            )
            mongo_semantics_database.insert_contract(contract_data)
            assert (
                1
                == mongo_db.get_collection(
                    MongoCollections.CONTRACTS
                ).estimated_document_count()
            )
            contract_from_db = mongo_semantics_database.get_contract_semantics(
                code_hash
            )
            assert contract_from_db == contract_data
            assert mongo_db.list_collection_names() == [MongoCollections.CONTRACTS]
        finally:
            mongo_db.drop_collection(MongoCollections.CONTRACTS)

    def test_save_and_get_address_semantic(self, mongo_db, mongo_semantics_database):
        address = "test_address"
        address_data = {
            "address": address,
            "chain_id": "mainnet",
            "erc20": {
                "name": "test_name",
                "symbol": "test_symbol",
                "decimals": "test_decimal",
            },
            "contract": "test_contract",
            "name": "test_contract_name",
            "is_contract": False,
            "standard": False,
        }

        try:
            assert (
                0
                == mongo_db.get_collection(
                    MongoCollections.ADDRESSES
                ).estimated_document_count()
            )
            mongo_semantics_database.insert_address(address_data)
            assert (
                1
                == mongo_db.get_collection(
                    MongoCollections.ADDRESSES
                ).estimated_document_count()
            )
            address_from_db = mongo_semantics_database.get_address_semantics(
                "mainnet", address
            )
            assert address_from_db == address_data
            assert mongo_db.list_collection_names() == [MongoCollections.ADDRESSES]
        finally:
            mongo_db.drop_collection(MongoCollections.ADDRESSES)
