"""
Bootstrap factory for LangGraph and Agents.
"""
from app.ai.bootstrap.service_factory import (
    llm_service,
    embedding_service,
    vector_store_service,
    prompt_registry
)

from app.ai.agents.intake_agent import IntakeAgent
from app.ai.agents.embedding_agent import EmbeddingAgent
from app.ai.agents.evidence_retrieval_agent import EvidenceRetrievalAgent
from app.ai.agents.bias_detection_agent import BiasDetectionAgent
from app.ai.agents.performance_analysis_agent import PerformanceAnalysisAgent
from app.ai.agents.explainability_agent import ExplainabilityAgent
from app.ai.agents.report_generation_agent import ReportGenerationAgent
from app.ai.agents.human_approval_agent import HumanApprovalAgent
from app.ai.agents.finalization_agent import FinalizationAgent

from app.ai.graph.graph import ReviewGuardGraph

intake_agent = IntakeAgent()
embedding_agent = EmbeddingAgent(
    embedding_service=embedding_service,
    vector_store_service=vector_store_service
)
retrieval_agent = EvidenceRetrievalAgent(
    embedding_service=embedding_service,
    vector_store_service=vector_store_service
)
bias_agent = BiasDetectionAgent(
    llm_service=llm_service,
    prompt_registry=prompt_registry
)
analysis_agent = PerformanceAnalysisAgent(
    llm_service=llm_service,
    prompt_registry=prompt_registry
)
explainability_agent = ExplainabilityAgent(
    llm_service=llm_service,
    prompt_registry=prompt_registry
)
report_agent = ReportGenerationAgent(
    llm_service=llm_service,
    prompt_registry=prompt_registry
)
approval_agent = HumanApprovalAgent(
    llm_service=llm_service,
    prompt_registry=prompt_registry
)
finalization_agent = FinalizationAgent()

pipeline_graph = ReviewGuardGraph(
    intake_agent=intake_agent,
    embedding_agent=embedding_agent,
    retrieval_agent=retrieval_agent,
    bias_agent=bias_agent,
    analysis_agent=analysis_agent,
    explainability_agent=explainability_agent,
    report_agent=report_agent,
    approval_agent=approval_agent,
    finalization_agent=finalization_agent
)
