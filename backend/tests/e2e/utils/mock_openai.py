import json
from typing import Dict, Any, List

class MockOpenAI:
    def __init__(self, api_key=None):
        self.chat = MockChat()
        self.embeddings = MockEmbeddings()

class MockChat:
    def __init__(self):
        self.completions = MockCompletions()

class MockCompletions:
    def create(self, model: str, messages: List[Dict[str, str]], response_format: Any = None, **kwargs):
        # We need to simulate the various JSON structures requested by LangGraph Agents.
        
        # Determine which agent is calling by looking at the system prompt
        system_prompt = messages[0]["content"] if messages else ""
        
        # 1. Performance Agent
        if "Performance Analysis Agent" in system_prompt or "PerformanceAnalysisSchema" in system_prompt:
            content = json.dumps({
                "summary": "Employee demonstrated strong performance.",
                "overall_score": 4.5,
                "strengths": ["Leadership", "Coding"],
                "improvement_areas": ["Communication"],
                "goal_progress": [{"goal_name": "Deliver API", "status": "Completed"}],
                "confidence_score": 0.9,
                "confidence_reason": "Clear evidence in text",
                "missing_information": []
            })
            
        # 2. Bias Detection Agent
        elif "Bias Detection Agent" in system_prompt or "BiasAnalysisSchema" in system_prompt:
            # We look at the user message to see if we passed the "biased" text
            user_msg = str(messages[-1]["content"])
            if "dinosaur" in user_msg or "too old" in user_msg:
                content = json.dumps({
                    "bias_detected": True,
                    "overall_risk_score": 0.8,
                    "detected_biases": [
                        {
                            "category": "Age Bias",
                            "severity": "HIGH",
                            "description": "Language used implies negative age stereotypes",
                            "evidence_quotes": ["Sam is a dinosaur and too old"],
                            "recommended_correction": "Focus on specific skills rather than age"
                        }
                    ],
                    "unsupported_claims": [],
                    "confidence_score": 0.95
                })
            else:
                content = json.dumps({
                    "bias_detected": False,
                    "overall_risk_score": 0.1,
                    "detected_biases": [],
                    "unsupported_claims": [],
                    "confidence_score": 0.95
                })
                
        # 3. Explainability Agent
        elif "Explainability Agent" in system_prompt or "ExplainabilityAnalysisSchema" in system_prompt:
            content = json.dumps({
                "decision_graph": [
                    {"node": "Performance", "inputs": ["text"], "outputs": ["4.5 score"]}
                ],
                "evidence_map": [
                    {"claim": "Strong leadership", "quotes": ["led the project"]}
                ],
                "confidence_breakdown": {
                    "overall_confidence": 0.9,
                    "factors": ["Consistent praise"]
                },
                "transparency_score": 0.9,
                "limitations": []
            })
            
        # 4. Report Generation Agent
        elif "Report Generation Agent" in system_prompt or "EnterprisePerformanceReportSchema" in system_prompt:
            content = json.dumps({
                "executive_summary": "Comprehensive review summary.",
                "overall_rating": "EXCEEDS_EXPECTATIONS",
                "kpi_summary": {"goals_met": 3, "goals_missed": 0, "quality_score": 4.5},
                "strengths": ["Architecture", "Testing"],
                "improvement_areas": [],
                "recommendations": ["Promote to Senior"],
                "development_plan": {"90_day_goals": ["Learn Rust"]},
                "manager_notes": "Great job.",
                "risk_summary": "Low risk.",
                "requires_hr_review": False
            })
            
        else:
            # Fallback
            content = "{}"

        class MockMessage:
            def __init__(self, c):
                self.content = c
                
        class MockChoice:
            def __init__(self, msg):
                self.message = msg
                
        class MockUsage:
            def __init__(self):
                self.prompt_tokens = 100
                self.completion_tokens = 50
                self.total_tokens = 150
                
        class MockResponse:
            def __init__(self, content):
                self.choices = [MockChoice(MockMessage(content))]
                self.usage = MockUsage()
                self.model = "gpt-4o-mock"
                
        return MockResponse(content)

class MockEmbeddings:
    def create(self, model: str, input: List[str]):
        class MockData:
            def __init__(self):
                self.embedding = [0.1] * 1536
                
        class MockUsage:
            def __init__(self):
                self.prompt_tokens = 50
                self.total_tokens = 50
                
        class MockResponse:
            def __init__(self, data_list):
                self.data = data_list
                self.usage = MockUsage()
                self.model = "text-embedding-3-small-mock"
                
        return MockResponse([MockData() for _ in input])
