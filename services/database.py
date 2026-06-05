import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker


def get_connection_string() -> str:
    env_connection = os.getenv("SQL_SERVER_CONNECTION_STRING")
    if env_connection:
        return env_connection

    user = os.getenv("SQL_SERVER_USER", "sa")
    password = os.getenv("SQL_SERVER_PASSWORD", "YourPassword123")
    server = os.getenv("SQL_SERVER_HOST", "localhost\\SQLEXPRESS")
    database = os.getenv("SQL_SERVER_DATABASE", "POO_Proyecto")
    driver = os.getenv("SQL_SERVER_DRIVER", "ODBC Driver 18 for SQL Server")

    connection_url = URL.create(
        "mssql+pyodbc",
        username=user,
        password=password,
        host=server,
        database=database,
        query={"driver": driver, "TrustServerCertificate": "yes"},
    )
    return str(connection_url)


engine = create_engine(get_connection_string(), fast_executemany=True, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()
