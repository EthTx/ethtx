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

import logging
from functools import lru_cache

from ..models.semantics_model import ContractSemantics
from ..semantics.router import Router

log = logging.getLogger(__name__)


@lru_cache(maxsize=128)
def amend_contract_semantics(semantics: ContractSemantics, router_=Router()):
    if semantics.code_hash in router_:
        try:
            semantics_updates = router_[semantics.code_hash]
            if "name" in semantics_updates:
                semantics.name = semantics_updates["name"]
            if "events" in semantics_updates:
                for signature, event_semantics in semantics_updates["events"].items():
                    semantics.events[signature] = event_semantics
            if "functions" in semantics_updates:
                for signature, function_semantics in semantics_updates[
                    "functions"
                ].items():
                    semantics.functions[signature] = function_semantics
            if "transformations" in semantics_updates:
                for signature, transformation in semantics_updates[
                    "transformations"
                ].items():
                    semantics.transformations[signature] = transformation

        except Exception as exc:
            log.warning(
                "Semantics update load for %s failed.",
                semantics.code_hash,
                exc_info=exc,
            )
