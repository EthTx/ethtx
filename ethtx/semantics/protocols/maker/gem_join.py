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


class GemJoin(Base):
    code_hash = "0x8661c673677de206fda20eb1883063ea4a827c2ac1c7f232dd30e276d20874fa"
    contract_semantics = dict(
        transformations={
            "0xc5ce281e": {  # ilk
                "__output0__": TransformationSemantics(
                    transformed_type="string",
                    transformation="string_from_bytes(__output0__)",
                )
            },
            "0x3b4da69f": {  # join
                "wad": TransformationSemantics(transformation="wad / 10**18")
            },
            "0xef693bed": {  # exit
                "wad": TransformationSemantics(transformation="wad / 10**18")
            },
        }
    )
