from enum import Enum

class BiasType(str, Enum):
    RECENCY = "Recency Bias"
    HALO = "Halo Effect"
    HORN = "Horn Effect"
    CONFIRMATION = "Confirmation Bias"
    SIMILARITY = "Similarity Bias"
    LENIENCY = "Leniency Bias"
    SEVERITY = "Severity Bias"
    CENTRAL_TENDENCY = "Central Tendency"
    GENDER = "Gender Bias"
    AGE = "Age Bias"
    ROLE = "Role Bias"
    DEPARTMENT = "Department Bias"
    EVIDENCE_GAP = "Evidence Gap"
    UNSUPPORTED_CONCLUSION = "Unsupported Conclusion"
    GOAL_COVERAGE = "Missing Goal Coverage"
    PERFORMANCE_METRICS_MISSING = "Missing Performance Metrics"
