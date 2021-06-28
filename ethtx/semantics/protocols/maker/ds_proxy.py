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


class DsProxy(Base):
    code_hash = "0x27c02a1a822222c2ad6a9a01021c98abf05dbe6d19540035756ef97697ed41d0"
    contract_semantics = dict(
        transformations={
            "0x1cff79cd": {  # execute
                "_data": TransformationSemantics(
                    transformed_type="call",
                    transformation="decode_call(_target, _data)",
                )
            }
        }
    )
