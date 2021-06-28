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


class DaiJoin(Base):
    code_hash = "0x76dac2e14412f6ee4c5ca566296c954598168738955fa974cb3302cb73b95f0f"

    contract_semantics = dict(
        transformations={
            "0x3b4da69f": {  # join
                "wad": TransformationSemantics(transformation="wad / 10**18")
            },
            "0xef693bed": {  # exit
                "wad": TransformationSemantics(transformation="wad / 10**18")
            },
        }
    )
