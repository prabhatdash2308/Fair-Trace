V1_0_DEVELOPER_PROMPT = """Analyze the provided PerformanceAnalysis, BiasAnalysis, and ContextBundle.

1. Reasoning Trace: Map each major finding or bias correction back to its source evidence.
2. Decision Graph: Build the logical flow from context retrieval through bias adjustments to final scores.
3. Transparency Metrics: Estimate coverage, consistency, and completeness.
4. Confidence: Provide individual confidence scores for performance, bias, reasoning, and overall.
5. Unsupported Claims: List any conclusions that lack evidence, why they lack it, and what actions HR should take.

Do not invent evidence. If something lacks support, flag it.
"""
