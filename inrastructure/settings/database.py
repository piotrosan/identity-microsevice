POSTGRES_HOST_WITH_PORT = "localhost:5432"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "example"
DATABASE_NAME = "identity_user"

SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST_WITH_PORT}/{DATABASE_NAME}"


MONGO_DB_USER = ""
MONGO_DB_PASSWORD = ""
MONGO_DB_DATABASE = ""
MONGO_DB_HOST = ""
MONGO_DB_PORT = ""