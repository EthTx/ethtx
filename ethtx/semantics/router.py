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
            foo = importlib.import_module(
                f"{cls.root_module_name}{filename.split(cls.root_module_name)[-1]}"
            )
            for item in dir(foo):
                obj = getattr(foo, item)
                if isinstance(obj, type) and issubclass(obj, Base) and obj != Base:
                    rv[obj.code_hash] = obj.contract_semantics

        return rv
