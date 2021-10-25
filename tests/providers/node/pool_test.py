import pytest

from ethtx.providers.node.connection_base import NodeConnection
from ethtx.providers.node.pool import NodeConnectionPool

MAINNET_CHAIN = {"mainnet": {"hook": "a", "poa": True}}
GOERLI_CHAIN = {"goerli": {"hook": "a, b, c", "poa": False}}

GOERLI_NODE = NodeConnection("goerli", "B", False)


class TestNodeConnectionPool:
    def test_number_of_connections(self):
        pool = NodeConnectionPool(nodes=MAINNET_CHAIN)
        assert len(pool) == 1, "Number of connections should equal 1."

    def test_add_connection(self):
        pool = NodeConnectionPool(nodes=MAINNET_CHAIN)
        pool.add_connection(connection=GOERLI_NODE)

        assert (
            GOERLI_NODE in pool.connections
        ), f"{GOERLI_NODE} should be in pool of connections."

    def test_get_connection(self):
        pool = NodeConnectionPool(nodes=MAINNET_CHAIN)
        pool.add_connection(connection=GOERLI_NODE)
        connection = pool.get_connection("goerli")

        assert (
            connection[0] == GOERLI_NODE
        ), f"{GOERLI_NODE} should be in pool of connections."

    def test_add_wrong_type_connection(self):
        pool = NodeConnectionPool(nodes=MAINNET_CHAIN)
        with pytest.raises(ValueError):
            pool.add_connection((1, 1, 1))
