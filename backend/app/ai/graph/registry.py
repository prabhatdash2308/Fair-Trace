from typing import Dict, Type
from app.ai.graph.models import NodeDefinition
from app.ai.graph.nodes.base import BaseNode

class NodeRegistry:
    """Enterprise registry for dynamically discovering graph nodes."""
    
    _nodes: Dict[str, NodeDefinition] = {}

    @classmethod
    def register(
        cls, 
        name: str, 
        description: str = "", 
        version: str = "1.0", 
        dependencies: list = None,
        interruptable: bool = False,
        retryable: bool = True
    ):
        def wrapper(node_class: Type[BaseNode]):
            definition = NodeDefinition(
                name=name,
                description=description,
                version=version,
                node_class=node_class,
                dependencies=dependencies or [],
                interruptable=interruptable,
                retryable=retryable
            )
            cls._nodes[name] = definition
            return node_class
        return wrapper

    @classmethod
    def get_node(cls, name: str) -> Type[BaseNode]:
        if name not in cls._nodes:
            raise ValueError(f"Node '{name}' not found in registry.")
        return cls._nodes[name].node_class

    @classmethod
    def list_nodes(cls) -> Dict[str, NodeDefinition]:
        return cls._nodes.copy()
