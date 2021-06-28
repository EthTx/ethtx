import pytest

from ethtx.utils.validators import assert_tx_hash


class TestValidator:
    def test_tx_valid_hash(self):
        tx_hash = "0xe9a781eea6b6dbb9354555fff3cfb4727d27eea78346f2ca341e3268037eb559"
        assert_tx_hash(tx_hash)

    def test_tx_valid_hash_without_0x(self):
        tx_hash = "e9a781eea6b6dbb9354555fff3cfb4727d27eea78346f2ca341e3268037eb559"
        assert_tx_hash(tx_hash)

    def test_tx_invalid_hashes(self):
        invalid_hashes = ["", "test", "Haxl337", None, 1]
        for invalid_hash in invalid_hashes:
            with pytest.raises(Exception):
                assert_tx_hash(invalid_hash)
