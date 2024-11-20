from sqlalchemy.ext.declarative import declarative_base
from inrastructure.sql_database import engine

Base = declarative_base()
Base.metadata.create_all(engine)