import sys
import logging
import uuid

# Setup basic logging to catch output
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

from app.ai.state.review_state import ReviewState
from app.ai.base.exceptions import StateValidationError
from app.ai.base.base_agent import BaseAgent
from app.ai.agents.intake_agent import IntakeAgent

print("Testing Intake Agent...")

print("\n1. Testing Inheritance...")
if issubclass(IntakeAgent, BaseAgent):
    print("SUCCESS: IntakeAgent inherits from BaseAgent")
else:
    print("FAIL: IntakeAgent does not inherit from BaseAgent")
    sys.exit(1)

print("\n2. Testing Validation (Missing IDs)...")
agent = IntakeAgent()
state = ReviewState()

# Missing employee/review IDs should fail
try:
    agent.execute(state)
    print("FAIL: Should have raised StateValidationError for missing metadata")
    sys.exit(1)
except StateValidationError as e:
    if "employee_id" in str(e):
        print("SUCCESS: Missing employee_id caught")
    else:
        print("FAIL: Wrong validation error")
        sys.exit(1)

state.metadata.employee_id = uuid.uuid4()
try:
    agent.execute(state)
except StateValidationError as e:
    if "review_cycle_id" in str(e):
        print("SUCCESS: Missing review_cycle_id caught")

state.metadata.review_cycle_id = uuid.uuid4()

print("\n3. Testing Normalization, Duplicates, and Classification...")
# Add some messy inputs
state.input.self_assessment = "   I did good \r\n\r\n\r\n things.   "
state.input.manager_feedback = "   " # empty after strip
state.input.peer_feedback = ["Great!", "Great!", ""] # One duplicate, one empty
state.input.uploaded_documents = [
    "This is my self assessment for the year.",
    "A generic unknown document."
]

result = agent.execute(state)

if result.input.self_assessment == "I did good\n\nthings.\n\nThis is my self assessment for the year.":
    print("SUCCESS: Normalization works (whitespace and line endings fixed)")
else:
    print(f"FAIL: Normalization failed. Got: {repr(result.input.self_assessment)}")
    sys.exit(1)

# Empty check
if result.input.manager_feedback is None:
    print("SUCCESS: Empty inputs are removed")
else:
    print("FAIL: Empty inputs were not removed")
    sys.exit(1)

# Duplicate check
if len(result.input.peer_feedback) == 1 and result.input.peer_feedback[0] == "Great!":
    print("SUCCESS: Duplicate detection works (and removed empty from list)")
else:
    print(f"FAIL: Duplicates/empty not removed from list correctly. Got {result.input.peer_feedback}")
    sys.exit(1)

# Classification check
if "This is my self assessment for the year." in result.input.self_assessment:
    print("SUCCESS: Document classification correctly appended to self_assessment")
else:
    print("FAIL: Document classification failed for self assessment")
    sys.exit(1)

if len(result.input.uploaded_documents) == 1 and "generic unknown" in result.input.uploaded_documents[0]:
    print("SUCCESS: Unknown documents remain in uploaded_documents")
else:
    print("FAIL: Unknown documents were not handled correctly")
    sys.exit(1)

print("\n4. Testing State Updates...")
if "IntakeAgent" in result.execution.completed_steps:
    print("SUCCESS: ExecutionState updated")
else:
    print("FAIL: ExecutionState not updated")
    sys.exit(1)

if len(result.audit.agent_logs) > 0 and len(result.audit.warnings) > 0:
    print("SUCCESS: AuditState updated with logs and warnings")
else:
    print("FAIL: AuditState not updated correctly")
    sys.exit(1)

print("\nAll verifications passed!")
