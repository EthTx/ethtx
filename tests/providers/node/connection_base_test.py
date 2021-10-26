from ethtx.providers.node.connection_base import NodeConnection

CHAIN = "mainnet"
NODE = "test"
POA = False


class TestConnectionBase:
    @classmethod
    def setup_class(cls):
        cls.connection = NodeConnection(CHAIN, NODE, POA)

    def test_connection_parameters(self):
        assert self.connection.chain == CHAIN
        assert self.connection.url == NODE
        assert self.connection.poa == POA

    def test_connection_representation(self):
        representation = f"<Chain: {CHAIN}, Node: {NODE}, Poa: {POA}>"
        assert repr(self.connection) == representation
        assert str(self.connection) == representation

    def test_connection_dict(self):
        assert dict(self.connection) == {"chain": CHAIN, "url": NODE, "poa": POA}
