import datetime

import pytest

from ethtx.models.decoded_model import AddressInfo, Argument
from ethtx.models.objects_model import BlockMetadata, TransactionMetadata

FAKE_TIME = datetime.datetime(2020, 12, 25, 17, 5, 55)


@pytest.fixture
def patch_datetime_now(monkeypatch):
    class MyDatetime:
        @classmethod
        def now(cls):
            return FAKE_TIME

    monkeypatch.setattr(datetime, "datetime", MyDatetime)


class DecodedModelMock:
    ADDRESS_INFO: AddressInfo = AddressInfo(address="address", name="name")
    ARGUMENT: Argument = Argument(name="name", type="type", value=1)


class ObjectModelMock:
    BLOCK_METADATA: BlockMetadata = BlockMetadata(
        block_number=15,
        block_hash="0x1",
        timestamp=FAKE_TIME,
        parent_hash="0x",
        miner="miner",
        gas_limit=12,
        gas_used=1,
        tx_count=5,
    )

    TRANSACTION_METADATA: TransactionMetadata = TransactionMetadata(
        tx_hash="0x",
        block_number=1,
        gas_price=2,
        from_address="0xa",
        to_address="0xb",
        tx_index=3,
        tx_value=4,
        gas_limit=5,
        gas_used=1,
        success=False
    )
