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

from .connection_base import NodeConnection


class NodeConnectionPool:
    def __init__(self, nodes: Dict[str, dict]):
        self._connections: List[NodeConnection] = []

        self._set_connections(nodes)

    def __len__(self) -> int:
        return len(self._connections)

    @property
    def connections(self) -> List[NodeConnection]:
        return self._connections

    def add_connection(self, connection: NodeConnection) -> None:
        if not isinstance(connection, NodeConnection):
            raise ValueError("Value is not instance of NodeBase")

        self._connections.append(connection)

    def get_connection(self, chain: str) -> List[NodeConnection]:
        return [
            connection for connection in self._connections if connection.chain == chain
        ]

    def _set_connections(self, nodes) -> None:
        for chain, node_params in nodes.items():
            nodes: List[str] = list(node_params.values())[0].split(",")
            poa: bool = list(node_params.values())[1]
            for url in nodes:
                self.add_connection(
                    NodeConnection(chain=chain, url=url.strip(), poa=poa)
                )
