import os
from pathlib import Path

# update nodes.py
nodes_file = Path("backend/app/ai/graph/nodes.py")
content = nodes_file.read_text(encoding="utf-8")
content = content.replace('state.metadata.pipeline_status = "NEEDS_RETRY"', '')
content = content.replace('def retry_node(self, state: ReviewState) -> ReviewState:', '''def retry_node(self, state: ReviewState) -> ReviewState:
        logger.warning(f"Entering Retry Node. Current count: {state.execution.retry_count}")
        state.execution.retry_count += 1
        if state.execution.current_step in state.execution.failed_steps:
            state.execution.failed_steps.remove(state.execution.current_step)
        if state.execution.retry_count > 3:
            logger.error("Max graph retries exceeded.")
            state.metadata.pipeline_status = PipelineStatus.FAILED
        return state
    # def dummy''')
content = content.replace('logger.warning(f"Entering Retry Node. Current count: {state.execution.retry_count}")\n        state.execution.retry_count += 1\n        if state.execution.retry_count > 3:\n            logger.error("Max graph retries exceeded.")\n            state.metadata.pipeline_status = PipelineStatus.FAILED\n        else:\n            state.metadata.pipeline_status = PipelineStatus.RUNNING\n        return state', '')
nodes_file.write_text(content, encoding="utf-8")

# update edges.py
edges_file = Path("backend/app/ai/graph/edges.py")
e_content = edges_file.read_text(encoding="utf-8")
e_content = e_content.replace('if state.metadata.pipeline_status == "NEEDS_RETRY":', 'if state.execution.current_step in state.execution.failed_steps:')
edges_file.write_text(e_content, encoding="utf-8")

# update builder.py
builder_file = Path("backend/app/ai/graph/builder.py")
b_content = builder_file.read_text(encoding="utf-8")
old_retry = 'self.workflow.add_conditional_edges("retry_node", edges.retry_router)'
new_retry = '''self.workflow.add_conditional_edges("retry_node", edges.retry_router, {
            "intake": "intake",
            "embedding": "embedding",
            "evidence_retrieval": "evidence_retrieval",
            "bias_detection": "bias_detection",
            "performance_analysis": "performance_analysis",
            "analysis": "performance_analysis", # fallback
            "explainability": "explainability",
            "report_generation": "report_generation",
            "report": "report_generation", # fallback
            "human_approval": "human_approval",
            "END": END
        })'''
b_content = b_content.replace(old_retry, new_retry)
builder_file.write_text(b_content, encoding="utf-8")

print("Files updated for Retry fixes.")
