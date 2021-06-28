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

from ethtx.models.semantics_model import TransformationSemantics
from ethtx.semantics.base import Base


class Dai(Base):
    code_hash = "0x4e36f96ee1667a663dfaac57c4d185a0e369a3a217e0079d49620f34f85d1ac7"
    contract_semantics = dict(
        transformations={
            "0x40c10f19": {  # mint
                "wad": TransformationSemantics(transformation="wad / 10**18")
            },
            "0x9dc29fac": {  # burn
                "wad": TransformationSemantics(transformation="wad / 10**18")
            },
        }
    )
