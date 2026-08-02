from app.ai.agents.report.prompts.system import V1_0_SYSTEM_PROMPT
from app.ai.agents.report.prompts.developer import V1_0_DEVELOPER_PROMPT
from app.ai.agents.report.prompts.output_schema import REPORT_OUTPUT_SCHEMA

PROMPT_VERSIONS = {
    "1.0": {
        "system": V1_0_SYSTEM_PROMPT,
        "developer": V1_0_DEVELOPER_PROMPT,
        "schema": REPORT_OUTPUT_SCHEMA
    }
}
