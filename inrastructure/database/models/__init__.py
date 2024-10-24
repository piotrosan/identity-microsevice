
from sqlalchemy.ext.declarative import declarative_base
from inrastructure.database import engine


Base = declarative_base()


Base.metadata.create_all(engine)