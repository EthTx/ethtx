from ethtx.models.semantics_model import (
    TransformationSemantics,
    ParameterSemantics,
    EventSemantics,
    FunctionSemantics,
    SignatureArg,
    Signature,
    ERC20Semantics,
    ContractSemantics,
    AddressSemantics,
)
from tests.models.mock import SemanticModelMock


class TestSemanticsModels:
    def test_transformation_semantics(self):
        ts = TransformationSemantics()

        assert ts.transformed_name is None
        assert ts.transformed_type is None
        assert ts.transformation == ""

    def test_parameter_semantics(self):
        ps = ParameterSemantics(parameter_name="name", parameter_type="type")

        assert ps.parameter_name == "name"
        assert ps.parameter_type == "type"
        assert ps.components == []
        assert not ps.indexed
        assert not ps.dynamic

    def test_event_semantics(self):
        es = EventSemantics(
            signature="0x",
            anonymous=True,
            name="name",
            parameters=[SemanticModelMock.PARAMETER_SEMANTICS],
        )

        assert es.signature == "0x"
        assert es.anonymous
        assert es.name == "name"
        assert es.parameters == [SemanticModelMock.PARAMETER_SEMANTICS]

    def test_function_semantics(self):
        fs = FunctionSemantics(
            signature="0x",
            name="name",
            inputs=[SemanticModelMock.PARAMETER_SEMANTICS],
            outputs=[SemanticModelMock.PARAMETER_SEMANTICS],
        )

        assert fs.signature == "0x"
        assert fs.name == "name"
        assert fs.inputs == [SemanticModelMock.PARAMETER_SEMANTICS]
        assert fs.outputs == [SemanticModelMock.PARAMETER_SEMANTICS]

    def test_signature_args(self):
        sa = SignatureArg(name="name", type="type")

        assert sa.name == "name"
        assert sa.type == "type"

    def test_signature(self):
        sa = SignatureArg(name="name", type="type")
        s = Signature(signature_hash="0x", name="name", args=[sa])

        assert s.signature_hash == "0x"
        assert s.name == "name"
        assert s.args == [sa]
        assert s.count == 1
        assert not s.tuple
        assert not s.guessed

    def test_erc20_semantics(self):
        es = ERC20Semantics(name="name", symbol="symbol", decimals=18)

        assert es.name == "name"
        assert es.symbol == "symbol"
        assert es.decimals == 18

    def test_contract_semantics(self):
        cs = ContractSemantics(code_hash="0x", name="name")

        assert cs.code_hash == "0x"
        assert cs.name == "name"
        assert cs.events == {}
        assert cs.functions == {}
        assert cs.transformations == {}

    def test_address_semantics(self):
        ads = AddressSemantics(
            chain_id="mainnet",
            address="0x",
            name="name",
            is_contract=True,
            contract=SemanticModelMock.CONTRACT_SEMANTICS,
        )
        assert ads.chain_id == "mainnet"
        assert ads.address == "0x"
        assert ads.name == "name"
        assert ads.is_contract
        assert ads.contract == SemanticModelMock.CONTRACT_SEMANTICS
        assert ads.standard is None
        assert ads.erc20 is None
