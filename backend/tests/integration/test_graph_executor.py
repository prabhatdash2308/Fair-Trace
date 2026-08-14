import pytest
import uuid
from app.ai.graph.executor import GraphExecutor
from app.ai.graph.state import ReviewState

from app.ai.graph.models import NodeResult
from unittest.mock import patch

@pytest.fixture(autouse=True)
def mock_all_nodes():
    with patch("app.ai.graph.nodes.performance.PerformanceNode.run") as mock_perf, \
         patch("app.ai.graph.nodes.bias.BiasNode.run") as mock_bias, \
         patch("app.ai.graph.nodes.explainability.ExplainabilityNode.run") as mock_expl, \
         patch("app.ai.graph.nodes.report.ReportNode.run") as mock_rep:
        mock_perf.return_value = NodeResult(status="success", data={"performance_analysis": {"status": "mocked"}}, state={})
        mock_bias.return_value = NodeResult(status="success", data={"bias_analysis": {"status": "mocked"}}, state={})
        mock_expl.return_value = NodeResult(status="success", data={"explainability_analysis": {"status": "mocked"}}, state={})
        mock_rep.return_value = NodeResult(status="success", data={"final_report": {"status": "mocked"}}, state={})
        yield

@pytest.mark.skip(reason="Obsolete: replaced by RealPipeline")
@pytest.mark.asyncio
async def test_full_graph_execution_with_interrupt():
    execution_id = str(uuid.uuid4())
    state: ReviewState = {
        "execution_id": execution_id,
        "document_id": "doc-1",
        "user_id": "usr-1",
        "context_bundle": {"data": "test"}
    }
    
    # 1. Run until interrupt
    result = await GraphExecutor.run(execution_id, state)
    
    # It should pause at 'approval_node' and not reach 'report_node'
    status = await GraphExecutor.get_status(execution_id)
    assert status["status"] == "paused"
    assert "approval_node" in status["next_nodes"]
    
    # 2. Resume graph with approval (resolved state)
    update = {"approval": {"status": "APPROVED", "resolved": True}}
    await GraphExecutor.resume(execution_id, update)
    status2 = await GraphExecutor.get_status(execution_id)
    assert not status2.get("next_nodes") # Graph finished
    
@pytest.mark.skip(reason="Obsolete: replaced by RealPipeline")
@pytest.mark.asyncio
async def test_resume_to_report():
    execution_id = str(uuid.uuid4())
    state: ReviewState = {
        "execution_id": execution_id,
        "document_id": "doc-1",
        "user_id": "usr-1",
        "context_bundle": {"text": "dummy"}
    }
    
    await GraphExecutor.run(execution_id, state)
    
    # Resume with approval
    update = {"approval": {"status": "APPROVED", "resolved": True}}
    result = await GraphExecutor.resume(execution_id, update)
    
    # Because it finished, check that final_report exists in state
    assert "final_report" in result
