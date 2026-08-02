from app.ai.agents.report.schemas import EnterprisePerformanceReportSchema

class BusinessValidator:
    """Applies strict enterprise business rules for final reports."""
    
    @staticmethod
    def validate(report: EnterprisePerformanceReportSchema) -> None:
        if report.overall_rating < 1.0 or report.overall_rating > 5.0:
            raise ValueError("overall_rating must be between 1.0 and 5.0.")
            
        if report.overall_confidence < 0.0 or report.overall_confidence > 1.0:
            raise ValueError("overall_confidence must be between 0.0 and 1.0.")
            
        # No duplicate recommendations based on title
        titles = [r.title.lower().strip() for r in report.recommended_actions]
        if len(titles) != len(set(titles)):
            raise ValueError("Duplicate recommended actions detected.")
            
        # Development plan checking
        if not report.development_plan.plan_90_day:
            raise ValueError("90-day development plan must be populated.")
