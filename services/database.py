import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker


def get_connection_string() -> str:
    connection_url = URL.create(
        "mssql+pyodbc",
        host="localhost\\SQLEXPRESS",
        database="POO_Proyecto",
        query={
            "driver": "ODBC Driver 18 for SQL Server",
            "trusted_connection": "yes",
            "TrustServerCertificate": "yes",
        },
    )

    return str(connection_url)


engine = create_engine(get_connection_string(), fast_executemany=True, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()
