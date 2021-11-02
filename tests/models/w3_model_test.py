from ethtx.models.w3_model import W3Block, W3Transaction, W3Receipt, W3Log, W3CallTree


class TestW3Models:
    def test_w3_block(self, mocker):
        hex_bytes = mocker.patch(
            "hexbytes.main.HexBytes",
            return_value="0x",
            new_callable=mocker.PropertyMock,
        )
        wb = W3Block(
            chain_id="mainnet",
            difficulty=1,
            extraData=hex_bytes,
            gasLimit=100,
            gasUsed=20,
            hash=hex_bytes,
            logsBloom=hex_bytes,
            miner="miner",
            nonce=hex_bytes,
            number=10,
            parentHash=hex_bytes,
            receiptsRoot=hex_bytes,
            sha3Uncles=hex_bytes,
            size=10,
            stateRoot=hex_bytes,
            timestamp=123123123123,
            totalDifficulty=1,
            transactions=[],
            transactionsRoot=hex_bytes,
            uncles=[],
        )

        assert wb.chain_id == "mainnet"
        assert wb.difficulty == 1
        assert wb.extraData == hex_bytes
        assert wb.gasLimit == 100
        assert wb.gasUsed == 20
        assert wb.hash == hex_bytes
        assert wb.logsBloom == hex_bytes
        assert wb.miner == "miner"
        assert wb.nonce == hex_bytes
        assert wb.number == 10
        assert wb.parentHash == hex_bytes
        assert wb.receiptsRoot == hex_bytes
        assert wb.sha3Uncles == hex_bytes
        assert wb.size == 10
        assert wb.stateRoot == hex_bytes
        assert wb.timestamp == 123123123123
        assert wb.totalDifficulty == 1
        assert wb.transactions == []
        assert wb.transactionsRoot == hex_bytes
        assert wb.uncles == []

    def test_w3_transaction(self, mocker):
        hex_bytes = mocker.patch(
            "hexbytes.main.HexBytes",
            return_value="0x",
            new_callable=mocker.PropertyMock,
        )

        wt = W3Transaction(
            chain_id="mainnet",
            blockHash=hex_bytes,
            blockNumber=5,
            from_address="0x",
            gas=5,
            gasPrice=5,
            hash=hex_bytes,
            input="0x",
            nonce=5,
            r=hex_bytes,
            s=hex_bytes,
            to="0x",
            transactionIndex=5,
            v=5,
            value=5,
        )

        assert wt.chain_id == "mainnet"
        assert wt.blockHash == hex_bytes
        assert wt.blockNumber == 5
        assert wt.from_address == "0x"
        assert wt.gas == 5
        assert wt.gasPrice == 5
        assert wt.hash == hex_bytes
        assert wt.input == "0x"
        assert wt.nonce == 5
        assert wt.r == hex_bytes
        assert wt.s == hex_bytes
        assert wt.to == "0x"
        assert wt.transactionIndex == 5
        assert wt.v == 5
        assert wt.value == 5

    def test_w3_receipt(self, mocker):
        hex_bytes = mocker.patch(
            "hexbytes.main.HexBytes",
            return_value="0x",
            new_callable=mocker.PropertyMock,
        )

        wr = W3Receipt(
            tx_hash="0x",
            chain_id="0x",
            blockHash=hex_bytes,
            blockNumber=10,
            contractAddress="0x",
            cumulativeGasUsed=10,
            from_address="0x",
            gasUsed=10,
            logsBloom=hex_bytes,
            status=10,
            to_address="0x",
            transactionHash=hex_bytes,
            transactionIndex=10,
            logs=[],
        )

        assert wr.tx_hash == "0x"
        assert wr.chain_id == "0x"
        assert wr.blockHash == hex_bytes
        assert wr.blockNumber == 10
        assert wr.contractAddress == "0x"
        assert wr.cumulativeGasUsed == 10
        assert wr.from_address == "0x"
        assert wr.gasUsed == 10
        assert wr.logsBloom == hex_bytes
        assert wr.status == 10
        assert wr.to_address == "0x"
        assert wr.transactionHash == hex_bytes
        assert wr.transactionIndex == 10
        assert wr.logs == []
        assert wr.root is None

    def test_w3_log(self, mocker):
        hex_bytes = mocker.patch(
            "hexbytes.main.HexBytes",
            return_value="0x",
            new_callable=mocker.PropertyMock,
        )
        wl = W3Log(
            tx_hash="0x",
            chain_id="0x",
            address="0x",
            blockHash=hex_bytes,
            blockNumber=55,
            data="0x",
            logIndex=55,
            removed=False,
            topics=[hex_bytes],
            transactionHash=hex_bytes,
            transactionIndex=55,
        )

        assert wl.tx_hash == "0x"
        assert wl.chain_id == "0x"
        assert wl.address == "0x"
        assert wl.blockHash == hex_bytes
        assert wl.blockNumber == 55
        assert wl.data == "0x"
        assert wl.logIndex == 55
        assert not wl.removed
        assert wl.topics == [hex_bytes]
        assert wl.transactionHash == hex_bytes
        assert wl.transactionIndex == 55

    def test_w3_call_tree(self):
        wct = W3CallTree(
            tx_hash="0xdas",
            chain_id="0xdas",
            type="0xdas",
            from_address="0xdas",
            to_address="0xdas",
            input="0xdas",
            output="0xdas",
            calls=[],
        )

        assert wct.tx_hash == "0xdas"
        assert wct.chain_id == "0xdas"
        assert wct.type == "0xdas"
        assert wct.from_address == "0xdas"
        assert wct.to_address == "0xdas"
        assert wct.input == "0xdas"
        assert wct.output == "0xdas"
        assert wct.calls == []
        assert wct.value is None
        assert wct.time is None
        assert wct.gas is None
        assert wct.gasUsed is None
        assert wct.error is None
