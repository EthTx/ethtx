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


class Jug(Base):
    code_hash = "0x79e3139c72f7ad381e81a7ff8ae63b5998f0778c1c025c6095a6f878771dc729"
    contract_semantics = dict(
        transformations={
            "0x44e2a5a8": {  # drip
                "ilk": TransformationSemantics(
                    transformed_type="string", transformation="string_from_bytes(ilk)"
                )
            }
        }
    )
