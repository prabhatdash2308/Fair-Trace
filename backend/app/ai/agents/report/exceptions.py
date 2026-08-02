class ReportGenerationError(Exception):
    pass

class OutputValidationError(ReportGenerationError):
    pass

class TokenLimitError(ReportGenerationError):
    pass
