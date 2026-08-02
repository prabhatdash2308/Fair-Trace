from app.ai.agents.performance.prompts.system import V1_0_SYSTEM_PROMPT
from app.ai.agents.performance.prompts.developer import V1_0_DEVELOPER_PROMPT

# Centralized mapping of prompt versions
PROMPT_VERSIONS = {
    "1.0": {
        "system": V1_0_SYSTEM_PROMPT,
        "developer": V1_0_DEVELOPER_PROMPT
    }
}
