from ethtx.models.decoded_model import (
    AddressInfo,
    DecodedTransactionMetadata,
    Argument,
    DecodedEvent,
    DecodedCall,
    DecodedTransfer,
    DecodedBalance,
    Proxy,
    DecodedTransaction,
)
from tests.models.mock import DecodedModelMock, FAKE_TIME, ObjectModelMock


class TestDecodedModels:
    def test_address_info(self):
        ai = AddressInfo(address="address", name="name")

        assert ai.address == "address"
        assert ai.name == "name"
        assert ai.badge is None

    def test_decoded_transaction_metadata(self):
        dtm = DecodedTransactionMetadata(
            chain_id="mainnet",
            tx_hash="0x12345",
            block_number=1,
            block_hash="0x12345",
            timestamp=FAKE_TIME,
            gas_price=1,
            sender=DecodedModelMock.ADDRESS_INFO,
            receiver=DecodedModelMock.ADDRESS_INFO,
            tx_index=1,
            tx_value=2,
            gas_limit=3,
            gas_used=4,
            success=True,
        )

        assert dtm.chain_id == "mainnet"
        assert dtm.tx_hash == "0x12345"
        assert dtm.block_number == 1
        assert dtm.block_hash == "0x12345"
        assert dtm.timestamp == FAKE_TIME
        assert dtm.gas_price == 1
        assert dtm.sender == DecodedModelMock.ADDRESS_INFO
        assert dtm.receiver == DecodedModelMock.ADDRESS_INFO
        assert dtm.tx_index == 1
        assert dtm.tx_value == 2
        assert dtm.gas_limit == 3
        assert dtm.gas_used == 4
        assert dtm.success

    def test_argument(self):
        a = Argument(name="name", type="type", value=1)

        assert a.name == "name"
        assert a.type == "type"
        assert a.value == 1

    def test_decoded_event(self):
        de = DecodedEvent(
            chain_id="mainnet",
            tx_hash="0x12345",
            timestamp=FAKE_TIME,
            contract=DecodedModelMock.ADDRESS_INFO,
            index=1,
            event_signature="0x0bc2390103cdcea68787f9f22f8be92ccf20f5eae0bb850fbb70af78e366e4dd",
            event_name="WalletAddressesSet",
            parameters=[DecodedModelMock.ARGUMENT, DecodedModelMock.ARGUMENT],
        )

        assert de.chain_id == "mainnet"
        assert de.tx_hash == "0x12345"
        assert de.timestamp == FAKE_TIME
        assert de.contract == DecodedModelMock.ADDRESS_INFO
        assert de.index == 1
        assert de.call_id is None
        assert (
            de.event_signature
            == "0x0bc2390103cdcea68787f9f22f8be92ccf20f5eae0bb850fbb70af78e366e4dd"
        )
        assert de.event_name == "WalletAddressesSet"
        assert de.parameters == [DecodedModelMock.ARGUMENT, DecodedModelMock.ARGUMENT]
        assert not de.event_guessed

    def test_decoded_call(self):
        dc = DecodedCall(
            chain_id="mainnet",
            tx_hash="0x12345",
            timestamp=FAKE_TIME,
            call_type="call",
            from_address=DecodedModelMock.ADDRESS_INFO,
            to_address=DecodedModelMock.ADDRESS_INFO,
            value=15,
            function_signature="0x521f8bed",
            function_name="getAllOperator",
            arguments=[DecodedModelMock.ARGUMENT],
            outputs=[],
            gas_used=15,
            status=True,
            indent=1,
        )

        assert dc.chain_id == "mainnet"
        assert dc.tx_hash == "0x12345"
        assert dc.timestamp == FAKE_TIME
        assert dc.call_id is None
        assert dc.call_type == "call"
        assert dc.from_address == DecodedModelMock.ADDRESS_INFO
        assert dc.to_address == DecodedModelMock.ADDRESS_INFO
        assert dc.value == 15
        assert dc.function_signature == "0x521f8bed"
        assert dc.function_name == "getAllOperator"
        assert dc.arguments == [DecodedModelMock.ARGUMENT]
        assert dc.outputs == []
        assert dc.gas_used == 15
        assert dc.error is None
        assert dc.status
        assert dc.indent == 1
        assert dc.subcalls == []
        assert not dc.function_guessed

    def test_decoded_transfer(self):
        dt = DecodedTransfer(
            from_address=DecodedModelMock.ADDRESS_INFO,
            to_address=DecodedModelMock.ADDRESS_INFO,
            token_symbol="ts",
            value=0.15,
        )

        assert dt.from_address == DecodedModelMock.ADDRESS_INFO
        assert dt.to_address == DecodedModelMock.ADDRESS_INFO
        assert dt.token_address is None
        assert dt.token_symbol == "ts"
        assert dt.token_standard is None
        assert dt.value == 0.15

    def test_decoded_balance(self):
        db = DecodedBalance(holder=DecodedModelMock.ADDRESS_INFO, tokens=[{}])

        assert db.holder == DecodedModelMock.ADDRESS_INFO
        assert db.tokens == [{}]

    def test_decoded_transaction(self):
        de = DecodedEvent(
            chain_id="mainnet",
            tx_hash="0x12345",
            timestamp=FAKE_TIME,
            contract=DecodedModelMock.ADDRESS_INFO,
            index=1,
            event_signature="0x0bc2390103cdcea68787f9f22f8be92ccf20f5eae0bb850fbb70af78e366e4dd",
            event_name="WalletAddressesSet",
            parameters=[DecodedModelMock.ARGUMENT, DecodedModelMock.ARGUMENT],
        )
        dc = DecodedCall(
            chain_id="mainnet",
            tx_hash="0x12345",
            timestamp=FAKE_TIME,
            call_type="call",
            from_address=DecodedModelMock.ADDRESS_INFO,
            to_address=DecodedModelMock.ADDRESS_INFO,
            value=15,
            function_signature="0x521f8bed",
            function_name="getAllOperator",
            arguments=[DecodedModelMock.ARGUMENT],
            outputs=[],
            gas_used=15,
            status=True,
            indent=1,
        )
        dt = DecodedTransfer(
            from_address=DecodedModelMock.ADDRESS_INFO,
            to_address=DecodedModelMock.ADDRESS_INFO,
            token_symbol="ts",
            value=0.15,
        )

        db = DecodedBalance(holder=DecodedModelMock.ADDRESS_INFO, tokens=[{}])

        t = DecodedTransaction(
            block_metadata=ObjectModelMock.BLOCK_METADATA,
            metadata=ObjectModelMock.TRANSACTION_METADATA,
            events=[de],
            calls=dc,
            transfers=[dt],
            balances=[db],
        )

        assert t.block_metadata == ObjectModelMock.BLOCK_METADATA
        assert t.metadata == ObjectModelMock.TRANSACTION_METADATA
        assert t.events == [de]
        assert t.calls == dc
        assert t.transfers == [dt]
        assert t.balances == [db]
        assert not t.status

    def test_proxy(self):
        p = Proxy(address="address", name="name", type="type")

        assert p.address == "address"
        assert p.name == "name"
        assert p.type == "type"
        assert p.semantics is None
        assert p.token is None
