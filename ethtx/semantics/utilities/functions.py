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

from functools import partial


def token_decimals(transaction, repository, address):
    try:
        _, _, decimals = repository.get_token_data(transaction.chain_id, address)
    except:
        decimals = 18

    return decimals


def decode_nft(contract, token_id):
    if len(str(token_id)) > 8:
        token_symbol = f"NFT {str(token_id)[:6]}...{str(token_id)[-2:]}"
    else:
        token_symbol = f"NFT {token_id}"

    token_address = f"{contract}?a={token_id}#inventory"

    return dict(address=token_address, name=token_symbol)


def string_from_bytes(raw_value):
    try:
        raw_value = raw_value[2:] if raw_value[:2] == "0x" else raw_value
        decoded_string = bytes.fromhex(raw_value).decode("utf-8").replace("\x00", "")
    except:
        decoded_string = "???"

    return decoded_string


def add_utils_to_context(context):

    # register additional functions available for transformations
    context["token_decimals"] = partial(
        token_decimals, context["__transaction__"], context["__repository__"]
    )
    context["decode_nft"] = partial(decode_nft, context["__contract__"])
    context["string_from_bytes"] = string_from_bytes

    return
