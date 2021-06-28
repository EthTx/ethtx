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


class CDPManager(Base):
    code_hash = "0xdc70464baedd675aadf1b109ac8ec36f78adb5db19bc087d2a70208305c786b1"
    contract_semantics = dict(
        transformations={
            "0x6090dec5": {  # open
                "ilk": TransformationSemantics(
                    transformed_type="string", transformation="string_from_bytes(ilk)"
                )
            },
            "0x45e6bdcd": {  # frob
                "dart": TransformationSemantics(transformation="dart / 10**18"),
                "dink": TransformationSemantics(transformation="dink / 10**18"),
            },
            "0xf9f30db6": {  # move
                "rad": TransformationSemantics(transformation="rad / 10**45")
            },
            "0x18af4d60": {  # flux
                "ilk": TransformationSemantics(
                    transformed_type="string", transformation="string_from_bytes(ilk)"
                ),
                "wad": TransformationSemantics(transformation="wad / 10**18"),
            },
            "0x2c2cb9fd": {  # ilks
                "__output0__": TransformationSemantics(
                    transformed_type="string",
                    transformation="string_from_bytes(__output0__)",
                )
            },
        }
    )
