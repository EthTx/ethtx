import pytest

from ethtx.providers.node.base import NodeBase

NODE = "test"
POA = False


@pytest.fixture()
def node_base_data():
    return NodeBase(NODE, POA)


def test_node_base_model(node_base_data):
    assert node_base_data.node == NODE
    assert node_base_data.poa == POA

    assert repr(node_base_data) == f"<Node: {NODE}, poa: {POA}>"
    assert str(node_base_data) == f"<Node: {NODE}, poa: {POA}>"
