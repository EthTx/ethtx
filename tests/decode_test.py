from ethtx.decoders.decoders.parameters import decode_static_argument


class TestParameterDecoder:

    def test_decode_static_argument_doesnt_double_0x_prefix(self):
        argument_type = "bytes32"
        raw_value = "0x0"
        decoded_value = decode_static_argument(raw_value=raw_value, argument_type=argument_type)
        assert decoded_value == "0x0"
