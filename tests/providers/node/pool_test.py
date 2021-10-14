import pytest

from ethtx.providers.node.base import NodeBase
from ethtx.providers.node.pool import NodeConnectionPool

MAINNET_CHAIN = {"mainnet": {"hook": "a", "poa": True}}
GOERLI_CHAIN = {"goerli": {"hook": "a, b, c", "poa": False}}

GOERLI_NODE = NodeBase("B", False)


class TestNodeConnectionPool:
    @classmethod
    def setup_class(cls):
        cls.pool = NodeConnectionPool(nodes=MAINNET_CHAIN)

    def test_one_connections(self):
        data = NodeBase(node="a", poa=True)
        assert self.pool.connections
        assert len(self.pool.connections) == 1
        assert self.pool.connections["mainnet"][0].__dict__ == data.__dict__
        assert "mainnet" in self.pool.connections

    def test_ok_getattr(self):
        assert self.pool.mainnet

    def test_wrong_getattr(self):
        with pytest.raises(AttributeError):
            _ = self.pool.goerli

    def test_setattr(self):
        self.pool.goerli = GOERLI_NODE
        assert self.pool.goerli

    def test_wrong_setattr(self):
        with pytest.raises(ValueError) as e:
            self.pool.wrong = 1, 1, 1

        assert str(e.value) == "Value is not instance of NodeBase"

    def test_multiple_connections(self):
        assert self.pool.connections
        assert len(self.pool.connections) == 2
        assert "mainnet" in self.pool.connections
        assert "goerli" in self.pool.connections
        assert self.pool.mainnet
        assert self.pool.goerli
