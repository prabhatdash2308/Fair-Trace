import sys
import logging
from pathlib import Path
from backend.app.ai.prompts import PromptRegistry, PromptLoader, PromptMetadata
from backend.app.ai.prompts.exceptions import PromptNotFoundError, PromptValidationError, PromptRegistrationError

# Setup basic logging to catch output
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

print("Testing Prompt Management System...")
base_dir = Path("backend/app/ai/prompts")
loader = PromptLoader(base_dir=base_dir)
registry = PromptRegistry(loader=loader)

print("\n1. Testing Registry & Loading...")
metadata = PromptMetadata(
    name="bias_prompt",
    version="1.0",
    description="Detects bias in feedback",
    owner_agent="BiasDetectionAgent",
    required_variables=["employee_name", "manager_feedback"],
    system_prompt_path="system/bias.txt",
    user_prompt_path="user/bias.txt"
)

# Test successful registration
registry.register(metadata)
print("SUCCESS: Registered prompt successfully")

# Test duplicate registration
try:
    registry.register(metadata)
    print("FAIL: Should not allow duplicate registration")
    sys.exit(1)
except PromptRegistrationError:
    print("SUCCESS: Duplicate registration prevented")

print("\n2. Testing Cache...")
# The system prompt should now be in the cache
cache_hit = loader.cache.get("backend\\app\\ai\\prompts\\system\\bias.txt")
if cache_hit:
    print("SUCCESS: Cache works (content found in cache)")
else:
    print("FAIL: Cache failed to store prompt")
    sys.exit(1)

print("\n3. Testing Rendering & Validation...")
# Test successful render
sys_rendered, user_rendered = registry.render_prompt(
    "bias_prompt", 
    variables={"employee_name": "Alice", "manager_feedback": "Great job!"}
)
print("SUCCESS: Prompt rendered successfully")
print(f"System: {sys_rendered}")
print(f"User: {user_rendered}")

# Test missing variable validation
try:
    registry.render_prompt(
        "bias_prompt", 
        variables={"employee_name": "Alice"}
    )
    print("FAIL: Should have raised validation error for missing variable")
    sys.exit(1)
except PromptValidationError:
    print("SUCCESS: Missing variable validation works")

# Test unused variable validation
try:
    registry.render_prompt(
        "bias_prompt", 
        variables={"employee_name": "Alice", "manager_feedback": "Great", "unused_var": "Extra"}
    )
    print("FAIL: Should have raised validation error for unused variable")
    sys.exit(1)
except PromptValidationError:
    print("SUCCESS: Unused variable validation works")

print("\nAll verifications passed!")
