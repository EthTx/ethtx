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

from abc import ABC, abstractmethod
from typing import TypeVar, Dict


class Base(ABC):
    """
    Semantics Base class.
    All semantics should have `code_hash: str` and `contract_semantics: dict` class attribute.
    Inherit this class if you want to implement new semantic.
    """

    @property
    @abstractmethod
    def contract_semantics(self) -> str:
        ...

    @property
    @abstractmethod
    def code_hash(self) -> dict:
        ...


BaseType = TypeVar(
    "BaseType", bound=Dict[Base.code_hash.fget, Base.contract_semantics.fget]
)
