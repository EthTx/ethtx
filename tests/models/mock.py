from ethtx.models.decoded_model import AddressInfo, Argument


class DecodedModelMock:
    ADDRESS_INFO: AddressInfo = AddressInfo(address="address", name="name")
    ARGUMENT: Argument = Argument(name="name", type="type", value=1)
