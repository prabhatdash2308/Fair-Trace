import os
from pathlib import Path

bootstrap_dir = Path("backend/app/ai/bootstrap")
bootstrap_dir.mkdir(parents=True, exist_ok=True)

# __init__.py
(bootstrap_dir / "__init__.py").write_text("")

# provider_factory.py
(bootstrap_dir / "provider_factory.py").write_text('''"""
Bootstrap factory for AI providers.
"""
import os
from app.ai.services.llm.providers import OpenAIProvider
from app.ai.services.embeddings.providers import OpenAIEmbeddingProvider
from app.ai.services.vector_store.providers import QdrantProvider

api_key = os.getenv("OPENAI_API_KEY", "dummy-key")

llm_provider = OpenAIProvider(api_key=api_key)
embedding_provider = OpenAIEmbeddingProvider(api_key=api_key)
vector_store_provider = QdrantProvider(host="localhost", port=6333)
''')

# service_factory.py
(bootstrap_dir / "service_factory.py").write_text('''"""
Bootstrap factory for AI services.
"""
import os
from pathlib import Path

from app.ai.services.llm.llm_service import LLMService
from app.ai.services.llm.config import LLMConfig
from app.ai.services.llm.circuit_breaker import CircuitBreaker
from app.ai.services.llm.retry import RetryManager
from app.ai.services.llm.telemetry import Telemetry as LLMTelemetry

from app.ai.services.embeddings.embedding_service import EmbeddingService
from app.ai.services.embeddings.config import EmbeddingConfig
from app.ai.services.embeddings.cache import EmbeddingCache
from app.ai.services.embeddings.telemetry import Telemetry as EmbeddingTelemetry

from app.ai.services.vector_store.vector_store_service import VectorStoreService
from app.ai.services.vector_store.config import VectorStoreConfig
from app.ai.services.vector_store.telemetry import Telemetry as VectorStoreTelemetry

from app.ai.prompts.registry import PromptRegistry
from app.ai.prompts.loader import PromptLoader

from app.ai.bootstrap.provider_factory import (
    llm_provider,
    embedding_provider,
    vector_store_provider
)

llm_service = LLMService(
    provider=llm_provider,
    config=LLMConfig(),
    circuit_breaker=CircuitBreaker(),
    retry_manager=RetryManager(),
    telemetry=LLMTelemetry()
)

embedding_service = EmbeddingService(
    provider=embedding_provider,
    config=EmbeddingConfig(),
    cache=EmbeddingCache(),
    telemetry=EmbeddingTelemetry()
)

vector_store_service = VectorStoreService(
    provider=vector_store_provider,
    config=VectorStoreConfig(collection_name="reviewguard_documents"),
    telemetry=VectorStoreTelemetry()
)

base_dir = Path(os.path.abspath(__file__)).parent.parent / "prompts"
prompt_registry = PromptRegistry(loader=PromptLoader(base_dir=base_dir))
''')

# graph_factory.py
(bootstrap_dir / "graph_factory.py").write_text('''"""
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
''')

# Modify pipeline_service.py
pipeline_file = Path("backend/services/pipeline_service.py")
content = pipeline_file.read_text(encoding="utf-8")
content = content.replace("from app.ai.graph.graph import pipeline_graph", "from app.ai.bootstrap.graph_factory import pipeline_graph")
pipeline_file.write_text(content, encoding="utf-8")

print("Bootstrap layer created successfully!")
