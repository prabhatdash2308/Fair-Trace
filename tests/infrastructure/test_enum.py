import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
e = postgresql.ENUM("A", "B", name="user_role", create_type=False)
print("create_type:", e.create_type)
