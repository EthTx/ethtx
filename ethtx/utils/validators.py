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

import re

from ethtx.exceptions import InvalidTransactionHash


def assert_tx_hash(tx_hash) -> None:
    tx_hash_regex = "^(0x)?([A-Fa-f0-9]{64})$"
    if not re.match(tx_hash_regex, tx_hash):
        raise InvalidTransactionHash(tx_hash)
