from backend.app.ai.state.review_state import ReviewState
import json

# Initialize state
state = ReviewState()

# Validate that we can serialize to JSON
state_json = state.model_dump_json(indent=2)
print("Initialization successful!")
print("Top-level keys:", list(json.loads(state_json).keys()))

# Quick nested test
state.metadata.current_agent = "Intake Agent"
state.bias.bias_score = 45.5
state.execution.completed_steps.append("intake")

new_json = state.model_dump_json()
print("Nested update and serialization successful!")
