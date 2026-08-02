import pytest
from app.ai.graph.builder import GraphBuilder
from langgraph.graph.state import CompiledStateGraph

def test_graph_compilation():
    graph = GraphBuilder.build_graph()
    assert isinstance(graph, CompiledStateGraph)
    
def test_graph_nodes_registered():
    graph = GraphBuilder.build_graph()
    
    # Internal representation of nodes
    node_names = list(graph.builder.nodes.keys())
    assert "load_context_node" in node_names
    assert "report_node" in node_names
    
def test_graph_edges():
    graph = GraphBuilder.build_graph()
    
    edges = [edge for edge in graph.builder.edges]
    # Check simple path from bias to explainability
    edge_targets = [e[1] for e in edges if e[0] == "bias_node"]
    assert "explainability_node" in edge_targets
