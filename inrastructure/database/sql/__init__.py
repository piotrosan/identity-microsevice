
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from inrastructure.settings.database import SQLALCHEMY_DATABASE_URI

# Create sql_database engine
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=False)

# Create sql_database session
Session = sessionmaker(bind=engine)
session = Session(expire_on_commit=False)
