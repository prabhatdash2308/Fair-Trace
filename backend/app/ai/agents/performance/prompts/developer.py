# Developer rules definitions

V1_0_DEVELOPER_PROMPT = """Analyze the provided context bundle carefully.
Extract:
- An overall numerical score.
- A confidence metric representing your confidence in the provided evidence.
- A concise list of strengths.
- A concise list of improvement areas.
- Key observations mapped to direct evidence.
- Status of established goals.
- Any risk flags (e.g., flight risk, compliance concerns, severe underperformance).
- A 2-3 paragraph professional summary of their overall performance.

DO NOT hallucinate. Do not infer anything outside the text. If evidence is lacking, lower the confidence score.
"""
