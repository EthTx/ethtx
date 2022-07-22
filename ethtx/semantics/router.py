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

import glob
import importlib
import os

from ..semantics.base import BaseType, Base


class Router:
    """
    Semantics router.
    Returns all objects withs semantics to include.
    """

    root_dir = os.path.dirname(__file__)
    root_module_name = ".".join(__name__.split(".")[:-1])

    def __new__(cls) -> BaseType:
        return cls._get_semantics()

    @classmethod
    def _get_semantics(cls) -> BaseType:
        """
        Get all available semantics.
        Match pattern:
            - .py file
            - object is a class type
            - object is a Base subclass
        """
        rv = {}
        files = (
            semantic
            for semantic in glob.iglob(cls.root_dir + "**/**", recursive=True)
            if os.path.isfile(semantic)
            and "__" not in semantic
            and semantic.endswith(".py")
        )

        for filename in files:
            filename = filename.replace("/", ".").replace(".py", "")
            imported_module = importlib.import_module(
                f"{cls.root_module_name}{filename.split(cls.root_module_name)[-1]}"
            )
            for item in dir(imported_module):
                obj = getattr(imported_module, item)
                if isinstance(obj, type) and issubclass(obj, Base) and obj != Base:
                    rv[obj.code_hash] = obj.contract_semantics

        return rv
