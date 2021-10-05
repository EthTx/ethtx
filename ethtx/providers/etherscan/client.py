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
import logging
from collections import OrderedDict
from typing import Dict, Optional

import requests

from ethtx.exceptions import ProcessingException

log = logging.getLogger(__name__)


class EtherscanClient:
    MODULE = "module="
    ACTION = "&action="
    CONTRACT_ADDRESS = "&contractaddress="
    ADDRESS = "&address="
    OFFSET = "&offset="
    PAGE = "&page="
    SORT = "&sort="
    BLOCK_TYPE = "&blocktype="
    TO = "&to="
    VALUE = "&value="
    DATA = "&data="
    POSITION = "&position="
    HEX = "&hex="
    GAS_PRICE = "&gasPrice="
    GAS = "&gas="
    START_BLOCK = "&startblock="
    END_BLOCK = "&endblock="
    BLOCKNO = "&blockno="
    TXHASH = "&txhash="
    TAG = "&tag="
    BOOLEAN = "&boolean="
    INDEX = "&index="
    API_KEY = "&apikey="

    url_dict: OrderedDict = {}

    def __init__(
        self,
        api_key: str,
        nodes: Dict[str, str],
        default_chain_id: Optional[str] = None,
    ):
        self.api_key = api_key
        self.endpoints = nodes
        self.default_chain = default_chain_id

        self.http = requests.session()
        self.http.headers.update({"User-Agent": "API"})

        self.url_dict = OrderedDict(
            [
                (self.MODULE, ""),
                (self.ADDRESS, ""),
                (self.ACTION, ""),
                (self.OFFSET, ""),
                (self.PAGE, ""),
                (self.SORT, ""),
                (self.BLOCK_TYPE, ""),
                (self.TO, ""),
                (self.VALUE, ""),
                (self.DATA, ""),
                (self.POSITION, ""),
                (self.HEX, ""),
                (self.GAS_PRICE, ""),
                (self.GAS, ""),
                (self.START_BLOCK, ""),
                (self.END_BLOCK, ""),
                (self.BLOCKNO, ""),
                (self.TXHASH, ""),
                (self.TAG, ""),
                (self.BOOLEAN, ""),
                (self.INDEX, ""),
                (self.API_KEY, api_key),
            ]
        )

    def build_url(self, chain_id: str, url_dict: OrderedDict) -> str:
        return (
            self.endpoints[chain_id]
            + "?"
            + "".join([param + val if val else "" for param, val in url_dict.items()])
        )

    def _get_chain_id(self, chain_id) -> str:
        _id = chain_id or self.default_chain

        if _id is None:
            raise ProcessingException(
                "chain_id must be provided as argument or constructor default"
            )
        return _id
