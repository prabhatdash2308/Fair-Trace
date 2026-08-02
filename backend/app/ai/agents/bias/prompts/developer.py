V1_0_DEVELOPER_PROMPT = """Analyze the provided PerformanceAnalysis alongside its source ContextBundle.

1. Detected Biases: Identify specific biases from the authorized taxonomy (e.g., Recency Bias, Gender Bias, Halo Effect). Include direct evidence, chunk IDs, and severity.
2. Fairness Assessment: Provide a professional summary evaluating the objective fairness of the review.
3. Unsupported Claims: List any claims or ratings in the PerformanceAnalysis that lack sufficient backing in the ContextBundle.
4. Missing Evidence: Identify what crucial performance data is missing.
5. Calculate the overall_bias_score (0.0 to 1.0).

Do not hallucinate. Do not infer biases without linguistic or structural evidence. If the review is perfectly fair, return an overall_bias_score of 0.0 with an empty detected_biases array.
"""
