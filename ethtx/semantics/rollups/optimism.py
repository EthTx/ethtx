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

from datetime import datetime

import requests
from ethereum.transactions import Transaction


def decode_from_4byte(method_sig, decoded_methods):
    if method_sig not in decoded_methods:
        url = (
            "https://www.4byte.directory/api/v1/signatures/?hex_signature=" + method_sig
        )
        r = requests.get(url).json()
        if len(r["results"]):
            text_sig = r["results"][-1]["text_signature"]
        else:
            text_sig = f"{method_sig}()"

        decoded_methods[method_sig] = text_sig
    else:
        text_sig = decoded_methods.get(method_sig)

    return text_sig


def decode_sequencer_batch(data):
    BATCH_CONTEXT_START_POS = 15
    BATCH_CONTEXT_SIZE = 16
    TX_DATA_HEADER_SIZE = 3

    def load_call_data(data, position, shift):

        sub_data = data[2 + 2 * position :]
        value = int(sub_data[: shift * 2], 16)

        return value

    def load_tx_data(data, position, length):
        def ECDSA_recover(transaction):
            tx = Transaction(
                transaction["nonce"],
                transaction["gas_price"],
                transaction["gas_limit"],
                b""
                if transaction["to_address"]
                == "0x0000000000000000000000000000000000000000"
                else transaction["to_address"],
                transaction["value"],
                bytes.fromhex(transaction["data"]),
                int(transaction["v"], 16) + 55,
                int(transaction["r"], 16),
                int(transaction["s"], 16),
            )

            tx_hash = "0x" + tx.hash.hex()
            from_address = "0x" + tx.sender.hex()

            return from_address, tx_hash

        sub_data = data[2 + 2 * position :][: length * 2]

        is_eip155 = int(sub_data[:2])
        r = sub_data[2 : 33 * 2]
        s = sub_data[33 * 2 : 65 * 2]
        v = sub_data[65 * 2 : 66 * 2]
        gas_limit = int(sub_data[66 * 2 : 69 * 2], 16)
        gas_price = int(sub_data[69 * 2 : 72 * 2], 16)
        nonce = int(sub_data[72 * 2 : 75 * 2], 16)
        to_address = "0x" + sub_data[75 * 2 : 95 * 2]
        data = sub_data[95 * 2 :]
        signature = decode_from_4byte("0x" + data[:8], decoded_methods)
        input_data = data[8:]

        transaction = dict(
            eip155=(is_eip155 == 0),
            r=r,
            s=s,
            v=v,
            gas_limit=gas_limit,
            gas_price=gas_price,
            nonce=nonce,
            to_address=to_address,
            value=0,
            data=data,
            signature=signature,
            input=input_data,
        )

        transaction["from_address"], transaction["tx_hash"] = ECDSA_recover(transaction)
        transaction.pop("data")

        return transaction

    decoded_methods = dict()

    data = "0x00000000" + data

    shouldStartAtElement = load_call_data(data, 4, 5)
    totalElementsToAppend = load_call_data(data, 9, 3)
    numContexts = load_call_data(data, 12, 3)
    numTransactions = 0

    batch = dict(
        shouldStartAtElement=shouldStartAtElement,
        totalElementsToAppend=totalElementsToAppend,
        numContexts=numContexts,
        contexts=[],
    )

    nextTransactionPtr = BATCH_CONTEXT_START_POS + BATCH_CONTEXT_SIZE * numContexts

    for i in range(numContexts):

        contextPtr = 15 + i * BATCH_CONTEXT_SIZE
        numSequencedTransactions = load_call_data(data, contextPtr, 3)
        numSubsequentQueueTransactions = load_call_data(data, contextPtr + 3, 3)
        ctxTimestamp = datetime.utcfromtimestamp(
            load_call_data(data, contextPtr + 6, 5)
        )
        ctxBlockNumber = load_call_data(data, contextPtr + 11, 5)

        context = dict(
            numSequencedTransactions=numSequencedTransactions,
            numSubsequentQueueTransactions=numSubsequentQueueTransactions,
            ctxTimestamp=ctxTimestamp,
            ctxBlockNumber=ctxBlockNumber,
            ctxSequencedTransactions=[],
        )

        for _ in range(numSequencedTransactions):
            txDataLength = load_call_data(data, nextTransactionPtr, 3)
            transactionData = load_tx_data(data, nextTransactionPtr + 3, txDataLength)
            context["ctxSequencedTransactions"].append(transactionData)
            numTransactions += 1
            nextTransactionPtr += TX_DATA_HEADER_SIZE + txDataLength

        batch["contexts"].append(context)

    batch["numTransactions"] = numTransactions

    return batch


def decode_ovm_message(data):
    target = gas_limit = data
    signature = input_data = None
    transaction = dict(
        eip155=Transaction,
        r=None,
        s=None,
        v=None,
        gas_limit=gas_limit,
        gas_price=0,
        nonce=0,
        to_address=target,
        value=0,
        data=data,
        signature=signature,
        input=input_data,
    )

    context = dict(
        ctxTimestamp=None, ctxBlockNumber=None, ctxSequencedTransactions=[transaction]
    )

    batch = dict(numContexts=1, contexts=[context])

    return batch
