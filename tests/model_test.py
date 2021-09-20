from ethtx.providers import Web3Provider
from .mocks.web3provider import MockWeb3Provider


class TestModel:
    def test_create_transaction(self):
        tx_hash = "0xd7701a0fc05593aee3a16f20cab605db7183f752ae942cc75fd0975feaf1072e"
        mock_web3_provider: Web3Provider = MockWeb3Provider()
        w3receipt = mock_web3_provider.get_receipt(tx_hash, "mainnet")
        tx = mock_web3_provider.get_transaction(tx_hash).to_object(w3receipt)
        assert tx is not None
        assert tx.tx_hash is not None
        assert tx.from_address is not None
        assert tx.to_address is not None
        assert tx.tx_index is not None

    def test_create_block(self):
        mock_web3_provider = MockWeb3Provider()
        block = mock_web3_provider.get_block(1, chain_id="mainnet").to_object()
        assert block is not None
        assert block.block_number is not None
        assert block.block_hash is not None
        assert block.timestamp is not None
        assert block.miner is not None
        assert block.tx_count is not None

    def test_create_event_from_tx_hash(self):
        mock_web3_provider = MockWeb3Provider()
        tx = "0xd7701a0fc05593aee3a16f20cab605db7183f752ae942cc75fd0975feaf1072e"
        receipt = mock_web3_provider.get_receipt(tx, "mainnet")
        r = receipt.logs[0]
        e = r.to_object()

        assert e is not None
        assert e.contract is not None
        assert e.log_data is not None
        assert len(e.topics) == 1
        assert e.log_index is not None
