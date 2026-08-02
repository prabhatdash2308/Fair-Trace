from app.ai.agents.bias.schemas import BiasAnalysisSchema

# In strict JSON mode for OpenAI, we provide the Pydantic class directly.
BIAS_OUTPUT_SCHEMA = BiasAnalysisSchema
