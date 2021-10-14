from ethtx.providers.node import get_connection
from ethtx.providers.node.base import NodeBase

CHAIN = "mainnet"
MAINNET_CHAIN = {"mainnet": {"hook": "a", "poa": True}}


def test_get_connection():
    data = list(get_connection(MAINNET_CHAIN, CHAIN))

    assert len(data) == 1
    assert isinstance(data[0], NodeBase)

    assert data[0].node == "a"
    assert data[0].poa == True
