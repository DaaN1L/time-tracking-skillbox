from sqlalchemy import create_engine

from ..settings import settings as s

engine = create_engine(
    url=f"{s.dbms_name}://{s.db_user}:{s.db_password}@{s.db_host}:{s.db_port}/{s.db_name}"
)
