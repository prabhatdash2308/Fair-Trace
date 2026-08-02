from app.ai.agents.explainability.prompts.system import V1_0_SYSTEM_PROMPT
from app.ai.agents.explainability.prompts.developer import V1_0_DEVELOPER_PROMPT
from app.ai.agents.explainability.prompts.output_schema import EXPLAINABILITY_OUTPUT_SCHEMA

PROMPT_VERSIONS = {
    "1.0": {
        "system": V1_0_SYSTEM_PROMPT,
        "developer": V1_0_DEVELOPER_PROMPT,
        "schema": EXPLAINABILITY_OUTPUT_SCHEMA
    }
}
