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

import os
from functools import WRAPPER_ASSIGNMENTS, wraps, lru_cache

CACHE_SIZE = int(os.environ.get("CACHE_SIZE", 256))


def cache(func, cache_size: int = CACHE_SIZE):
    @lru_cache(maxsize=cache_size)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def ignore_unhashable(func):
    uncached = func.__wrapped__
    attributes = WRAPPER_ASSIGNMENTS + ("cache_info", "cache_clear")
    wraps(func, assigned=attributes)

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TypeError as error:
            if "unhashable type" in str(error):
                return uncached(*args, **kwargs)
            raise

    wrapper.__uncached__ = uncached
    return wrapper
