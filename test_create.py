import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.schema import Table, Column, MetaData
from sqlalchemy import create_engine

e = postgresql.ENUM("A", "B", name="user_role", create_type=False)
metadata = MetaData()
t = Table("test", metadata, Column("role", e))

engine = create_engine("sqlite:///:memory:", echo=True)
metadata.create_all(engine)
