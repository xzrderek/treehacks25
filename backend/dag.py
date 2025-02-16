from dataclasses import dataclass, field
from typing import Dict, List, Optional
import enum

class NodeType(enum.Enum):
    TOOL_CALL = 'TOOL_CALL'
    LLM = 'LLM'
    CONDITION = 'CONDITION'

class NodeStatus(enum.Enum):
    PENDING = 'PENDING'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'

@dataclass
class DAGNode:
    id: str
    type: NodeType
    config: dict
    status: NodeStatus = NodeStatus.PENDING
    result: Optional[dict] = None

@dataclass
class DAG:
    nodes: List[DAGNode] = field(default_factory=list)
    edges: Dict[str, List[str]] = field(default_factory=dict)  # node_id -> [node_id]
    current_node: Optional[str] = None
    
    def add_node(self, node_type: NodeType, config: dict) -> str:
        node = DAGNode(
            id=str(len(self.nodes)),
            type=node_type,
            config=config
        )
        self.nodes.append(node)
        return node.id
    
    def add_edge(self, from_id: str, to_id: str):
        if from_id not in self.edges:
            self.edges[from_id] = []
        self.edges[from_id].append(to_id)

    def get_next_nodes(self) -> List[DAGNode]:
        """Get all nodes that are ready to be executed"""
        if not self.current_node:
            # If no current node, get root nodes (nodes with no incoming edges)
            incoming_edges = {target for targets in self.edges.values() for target in targets}
            return [node for node in self.nodes if node.status == NodeStatus.PENDING 
                   and node.id not in incoming_edges]
        
        # Get nodes that depend on the current node and are ready
        next_ids = self.edges.get(self.current_node, [])
        return [node for node in self.nodes if node.id in next_ids 
               and node.status == NodeStatus.PENDING
               and self._are_dependencies_completed(node.id)]

    def _are_dependencies_completed(self, node_id: str) -> bool:
        """Check if all dependencies of a node are completed"""
        incoming_edges = {target: source for source, targets in self.edges.items() 
                        for target in targets}
        if node_id not in incoming_edges:
            return True
            
        source_id = incoming_edges[node_id]
        source_node = next(node for node in self.nodes if node.id == source_id)
        return source_node.status == NodeStatus.COMPLETED
