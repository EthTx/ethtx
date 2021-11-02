from ethtx.models.objects_model import (
    BlockMetadata,
    TransactionMetadata,
    Event,
    Call,
    Transaction,
    Block,
)
from tests.models.mock import FAKE_TIME, ObjectModelMock


class TestObjectsModels:
    def test_block_metadata(self):
        bm = BlockMetadata(
            block_number=15,
            block_hash="0x1",
            timestamp=FAKE_TIME,
            parent_hash="0x",
            miner="miner",
            gas_limit=12,
            gas_used=1,
            tx_count=5,
        )

        assert bm.block_number == 15
        assert bm.block_hash == "0x1"
        assert bm.timestamp == FAKE_TIME
        assert bm.parent_hash == "0x"
        assert bm.miner == "miner"
        assert bm.gas_limit == 12
        assert bm.gas_used == 1
        assert bm.tx_count == 5
        assert bm.canonical

    def test_transaction_metadata(self):
        tm = TransactionMetadata(
            tx_hash="0x",
            block_number=1,
            gas_price=2,
            from_address="0xa",
            to_address="0xb",
            tx_index=3,
            tx_value=4,
            gas_limit=5,
            gas_used=1,
            success=False,
        )

        assert tm.tx_hash == "0x"
        assert tm.block_number == 1
        assert tm.gas_price == 2
        assert tm.from_address == "0xa"
        assert tm.to_address == "0xb"
        assert tm.tx_index == 3
        assert tm.tx_value == 4
        assert tm.gas_limit == 5
        assert tm.gas_used == 1
        assert not tm.success
        assert tm.gas_refund is None
        assert tm.return_value is None
        assert tm.exception_error is None
        assert tm.exception_error_type is None
        assert tm.revert_reason is None

    def test_event(self):
        e = Event(contract="0x", topics=["", ""], log_index=1)

        assert e.contract == "0x"
        assert e.topics == ["", ""]
        assert e.log_data is None
        assert e.log_index == 1
        assert e.call_id is None

    def test_call(self):
        c = Call(
            call_type="call",
            from_address="0xa",
            to_address="0xb",
            call_value=10,
            call_data="0x00000000000000000",
            return_value="0xeeee",
            status=True,
        )

        assert c.call_type == "call"
        assert c.from_address == "0xa"
        assert c.to_address == "0xb"
        assert c.call_value == 10
        assert c.call_gas is None
        assert c.call_data == "0x00000000000000000"
        assert c.return_value == "0xeeee"
        assert c.status
        assert c.gas_used is None
        assert c.error is None
        assert c.subcalls == []
        assert c.call_id is None
        assert c.created_address is None
        assert c.gas_refund is None
        assert c.exception_error is None
        assert c.exception_error_type is None
        assert c.revert_reason is None
        assert c.success is None

    def test_transaction(self):
        t = Transaction(
            metadata=ObjectModelMock.TRANSACTION_METADATA,
            root_call=ObjectModelMock.CALL,
            events=[
                ObjectModelMock.EVENT,
                ObjectModelMock.EVENT,
                ObjectModelMock.EVENT,
            ],
        )

        assert t.metadata == ObjectModelMock.TRANSACTION_METADATA
        assert t.root_call == ObjectModelMock.CALL
        assert t.events == [
            ObjectModelMock.EVENT,
            ObjectModelMock.EVENT,
            ObjectModelMock.EVENT,
        ]

    def test_block(self):
        t = Transaction(
            metadata=ObjectModelMock.TRANSACTION_METADATA,
            root_call=ObjectModelMock.CALL,
            events=[
                ObjectModelMock.EVENT,
                ObjectModelMock.EVENT,
                ObjectModelMock.EVENT,
            ],
        )

        b = Block(
            chain_id="mainnet",
            metadata=ObjectModelMock.BLOCK_METADATA,
            transactions=[t, t],
        )

        assert b.chain_id == "mainnet"
        assert b.metadata == ObjectModelMock.BLOCK_METADATA
        assert b.transactions == [t, t]
