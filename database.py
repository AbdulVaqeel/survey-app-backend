# from dotenv import load_dotenv
# load_dotenv()

# import os
# from sqlalchemy import create_engine
# from sqlalchemy.orm import declarative_base, sessionmaker

# DATABASE_URL = os.getenv("DATABASE_URL")

# if not DATABASE_URL:
#     raise ValueError("DATABASE_URL environment variable is not set")

# engine = create_engine(
#     DATABASE_URL,
#     pool_pre_ping=True,
#     pool_recycle=300,
#     connect_args={"sslmode": "require"},
# )

# SessionLocal = sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     bind=engine,
# )

# Base = declarative_base()


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()



from dotenv import load_dotenv
load_dotenv()


import os

# Load .env.local first (development), fall back to .env (production)
load_dotenv('.env.local', override=True)
load_dotenv('.env', override=False)
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker



DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

ENVIRONMENT = os.getenv("ENVIRONMENT", "production")

# SSL required on production (RDS/cloud), not needed locally
connect_args = {"sslmode": "require"} if ENVIRONMENT == "production" else {}

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args=connect_args,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()