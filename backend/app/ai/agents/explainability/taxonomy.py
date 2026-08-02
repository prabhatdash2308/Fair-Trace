from enum import Enum

class ExplanationType(str, Enum):
    EVIDENCE_BASED = "Evidence Based"
    SCORE_CALCULATION = "Score Calculation"
    BIAS_CORRECTION = "Bias Correction"
    GOAL_EVALUATION = "Goal Evaluation"
    PERFORMANCE_REASONING = "Performance Reasoning"
    MISSING_EVIDENCE = "Missing Evidence"
    CONFIDENCE_ESTIMATION = "Confidence Estimation"
