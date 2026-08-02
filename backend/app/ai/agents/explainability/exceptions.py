class ExplainabilityAgentException(Exception):
    pass

class OutputValidationError(ExplainabilityAgentException):
    pass

class TokenLimitError(ExplainabilityAgentException):
    pass
