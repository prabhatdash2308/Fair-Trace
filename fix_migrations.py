import re

file_path = 'backend/migrations/versions/0001_initial_schema.py'
with open(file_path, 'r') as f:
    content = f.read()

replacements = [
    (r'sa\.Enum\("ADMIN", "MANAGER", "EMPLOYEE", name="user_role"\)', 'user_role'),
    (r'sa\.Enum\("DRAFT","ACTIVE","PROCESSING","PENDING_APPROVAL","COMPLETED","CANCELLED", name="review_cycle_status"\)', 'review_cycle_status'),
    (r'sa\.Enum\("SELF_ASSESSMENT","MANAGER_NOTE","PEER_REVIEW","PROJECT_OUTCOME","GOAL","MEETING_NOTE", name="input_type"\)', 'input_type'),
    (r'sa\.Enum\("DRAFT","PENDING_APPROVAL","FINALIZED","REVISION_REQUESTED","REJECTED", name="report_status"\)', 'report_status'),
    (r'sa\.Enum\("HIGH","MEDIUM","LOW","INSUFFICIENT", name="confidence_level"\)', 'confidence_level'),
    (r'sa\.Enum\("TECHNICAL","COLLABORATION","LEADERSHIP","DELIVERY","GROWTH", name="performance_dimension"\)', 'performance_dimension'),
    (r'sa\.Enum\("RECENCY","HALO","HORN","LENIENCY","SEVERITY","UNSUPPORTED","IMBALANCE", name="bias_type"\)', 'bias_type'),
    (r'sa\.Enum\("HIGH","MEDIUM","LOW", name="severity"\)', 'severity'),
    (r'sa\.Enum\("REVIEW_CYCLE_CREATED","REVIEW_CYCLE_UPDATED","REVIEW_CYCLE_CANCELLED","INPUT_SUBMITTED","PIPELINE_TRIGGERED","PIPELINE_COMPLETED","PIPELINE_FAILED","AGENT_EXECUTED","REPORT_GENERATED","REPORT_APPROVED","REPORT_REJECTED","REPORT_REVISION_REQUESTED","USER_LOGIN","USER_LOGOUT","ACCESS_DENIED", name="audit_event_type"\)', 'audit_event_type'),
]

for pattern, repl in replacements:
    content = re.sub(pattern, repl, content)

with open(file_path, 'w') as f:
    f.write(content)
print('Done!')
