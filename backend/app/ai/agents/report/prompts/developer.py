V1_0_DEVELOPER_PROMPT = """Analyze the provided PerformanceAnalysis, BiasAnalysis, ExplainabilityAnalysis, and ContextBundle.

Generate the final enterprise report payload including:
- Employee Summary
- Executive Summary (derive exclusively from inputs)
- Overall Rating (1.0 to 5.0)
- Overall Confidence
- Performance Highlights, Strengths, Improvement Areas
- Goal Progress
- Development Plan (90-day, learning, manager/employee actions)
- Recommended Actions (Prioritized with evidence_ids)
- Risk Summary (overall, bias, confidence, missing evidence counts)
- Manager Notes

Maintain a professional, objective, enterprise HR tone.
"""
