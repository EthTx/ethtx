#  Copyright 2021 DAI Foundation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


def decode_rollup_data(data):
    def get_32word_at(data, pos):
        word_length = 2 * 32
        dataStart = pos * 2
        return data[dataStart : dataStart + word_length]

    numberOfAssets = 4
    txNumPubInputs = 12
    rollupNumPubInputs = 10 + numberOfAssets
    # public inputs length for of each inner proof tx
    txPubInputLength = txNumPubInputs * 32
    rollupPubInputLength = rollupNumPubInputs * 32

    rollup = dict(
        rollupPubInputLength=rollupPubInputLength,
        rollupId=int(get_32word_at(data, 0), 16),
        rollupSize=int(get_32word_at(data, int("0x20", 16)), 16),
        dataStartIndex=int(get_32word_at(data, int("0x40", 16)), 16),
        oldDataRoot=get_32word_at(data, int("0x60", 16)),
        newDataRoot=get_32word_at(data, int("0x80", 16)),
        oldNullRoot=get_32word_at(data, int("0xa0", 16)),
        newNullRoot=get_32word_at(data, int("0xc0", 16)),
        oldRootRoot=get_32word_at(data, int("0xe0", 16)),
        newRootRoot=get_32word_at(data, int("0x100", 16)),
    )

    rollupSize = int(get_32word_at(data, int("0x20", 16)), 16)
    numTxs = 1 if rollupSize == 0 else rollupSize

    proofDataPointer = rollupPubInputLength
    operations = []
    for _ in range(numTxs):

        proofId = int(get_32word_at(data, proofDataPointer), 16)
        publicInput = get_32word_at(data, proofDataPointer + int("0x20", 16))
        publicOutput = get_32word_at(data, proofDataPointer + int("0x40", 16))
        nullifier1 = get_32word_at(data, proofDataPointer + int("0x100", 16))

        if proofId == 0:

            assetId = int(get_32word_at(data, proofDataPointer + int("0x60", 16)), 16)
            inputOwner = (
                "0x" + get_32word_at(data, proofDataPointer + int("0x140", 16))[-40:]
            )
            outputOwner = (
                "0x" + get_32word_at(data, proofDataPointer + int("0x160", 16))[-40:]
            )

            if assetId == 0:
                if int(publicInput, 16):
                    operation = dict(
                        type="Deposits",
                        address=inputOwner,
                        amount=f"{int(publicInput, 16) / 10 ** 18:,} ETH",
                    )
                    operations.append(operation)

                elif int(publicOutput, 16):
                    operation = dict(
                        type="Withdrawals",
                        address=outputOwner,
                        amount=f"{int(publicOutput, 16) / 10 ** 18:,} ETH",
                    )
                    operations.append(operation)

                elif int(nullifier1, 16):
                    operation = dict(type="Private", address="", amount="")
                    operations.append(operation)

        elif proofId == 1:

            address = "0x" + publicInput + publicOutput
            operation = dict(
                type="Accounts", address=address[:60] + "..." + address[-6:], amount=""
            )
            operations.append(operation)

        proofDataPointer = proofDataPointer + txPubInputLength

    return rollup, operations
