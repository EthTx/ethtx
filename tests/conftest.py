import pytest
from mongoengine import connect
from pymongo import MongoClient

from ethtx.providers.semantic_providers import MongoSemanticsDatabase


@pytest.fixture
def mongo_db():
    db_name = "mongo_semantics_test"
    client: MongoClient = connect(db=db_name, host="mongomock://localhost")
    yield client.db
    client.drop_database(db_name)
    client.close()


@pytest.fixture
def mongo_semantics_database(mongo_db):
    yield MongoSemanticsDatabase(mongo_db)
