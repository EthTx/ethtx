import pytest

from ethtx.providers.node.base import NodeBase

NODE = "test"
POA = False


def test_node_base_model():
    node_base_data = NodeBase(NODE, POA)

    assert node_base_data.node == NODE
    assert node_base_data.poa == POA

    assert repr(node_base_data) == f"<Node: {NODE}, poa: {POA}>"
    assert str(node_base_data) == f"<Node: {NODE}, poa: {POA}>"
