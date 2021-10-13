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
from typing import Dict, List

from ethtx.providers.nodes.base import NodeBase


class NodeConnectionPool:
    def __init__(self, nodes: Dict[str, dict]):
        self._set_connections(nodes)

    def __getattribute__(self, chain: str) -> List[NodeBase]:
        return super().__getattribute__(chain.lower())

    def __setattr__(self, chain: str, value: NodeBase) -> None:
        if chain in self.__dict__:
            self.__dict__[chain.lower()].append(value)
        else:
            self.__dict__[chain.lower()] = [value]

    @property
    def connections(self) -> Dict:
        return self.__dict__

    def _set_connections(self, nodes) -> None:
        for chain, node_params in nodes.items():
            nodes: List[str] = list(node_params.keys())[0].split(",")
            poa: bool = list(node_params.values())[0]
            for node in nodes:
                self.__setattr__(chain, NodeBase(hook=node, poa=poa))
