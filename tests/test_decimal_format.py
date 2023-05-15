from decimal import Decimal

from ethtx.decoders.semantic.helpers.utils import (
    _handle_decimal_representations as handle_decimal_representations,
)


class TestHandleDecimalRepresentations:
    def test_handle_decimal_representations(self):
        # Test for small int
        assert handle_decimal_representations(Decimal(10)) == "10"

        # Test for large int
        assert (
            handle_decimal_representations(Decimal("100000000000000000000000000"))
            == "100000000000000000000000000"
        )

        # Test for small float
        assert handle_decimal_representations(Decimal("0.5")) == "0.5"

        # Test for large float
        assert (
            handle_decimal_representations(Decimal("100000000000000000000.5"))
            == "100000000000000000000.5"
        )

        # Test for float with a lot of decimals
        assert (
            handle_decimal_representations(Decimal("0.12345678901234567890123456789"))
            == "0.12345678901234567890123456789"
        )

        # Test for float with trailing 0s
        assert handle_decimal_representations(Decimal("10.500")) == "10.5"

        # Test for float with trailing 0s
        assert handle_decimal_representations(Decimal("10.000")) == "10"

        # Test for float with trailing 0s and leading 0s
        assert handle_decimal_representations(Decimal("0.0500")) == "0.05"

        # Test cases from the original question
        assert (
            handle_decimal_representations(Decimal("0.0461872460000")) == "0.046187246"
        )
        assert handle_decimal_representations(Decimal("0.00000")) == "0"
        assert handle_decimal_representations(Decimal("650000000")) == "650000000"
        assert (
            handle_decimal_representations(Decimal("650000000.0004214000"))
            == "650000000.0004214"
        )
        assert handle_decimal_representations(Decimal("650000.00000000")) == "650000"

        # Additional test cases
        assert (
            handle_decimal_representations(Decimal("0.0000000000000000000000001"))
            == "0.0000000000000000000000001"
        )
        assert (
            handle_decimal_representations(
                Decimal("0.000000000000000000000000187126874612874612784")
            )
            == "0.000000000000000000000000187126874612874612784"
        )
        assert (
            handle_decimal_representations(
                Decimal("0.000000000000000000000000187126874612874612784000000000")
            )
            == "0.000000000000000000000000187126874612874612784"
        )

        # Test that the function returns a string
        assert isinstance(handle_decimal_representations(Decimal("1.234")), str)
