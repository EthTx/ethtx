# Copyright 2021 DAI FOUNDATION (the original version https://github.com/daifoundation/ethtx_ce)
# Copyright 2021-2022 Token Flow Insights SA (modifications to the original software as recorded
# in the changelog https://github.com/EthTx/ethtx/blob/master/CHANGELOG.md)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.
#
# The product contains trademarks and other branding elements of Token Flow Insights SA which are
# not licensed under the Apache 2.0 license. When using or reproducing the code, please remove
# the trademark and/or other branding elements.

import logging
import sys
import time

log = logging.getLogger(__name__)


class ExecutionTimer:
    start_time: float
    part_name: str

    def __init__(self, part_name: str):
        self.part_name = part_name

    def __enter__(self):
        self.start_time = time.time()

    def __exit__(self, *kwargs):
        end_time = time.time()
        exec_time = (end_time - self.start_time) * 1000
        log.info("Executed %s in %s ms", self.part_name, exec_time)


class RecursionLimit:
    def __init__(self, limit: int):
        self.limit = limit
        self.cur_limit = sys.getrecursionlimit()

    def __enter__(self) -> None:
        sys.setrecursionlimit(self.limit)

    def __exit__(self, *_) -> None:
        sys.setrecursionlimit(self.cur_limit)
