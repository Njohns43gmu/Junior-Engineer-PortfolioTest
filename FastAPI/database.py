from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# load_dotenv() reads the .env file in the project root and injects each
# key=value pair into the process's environment variables (os.environ).
# This call must happen before any os.getenv() calls below, otherwise
# the variables won't exist yet when we try to read them.
load_dotenv()

# os.getenv() reads the value of DATABASE_URL from the environment.
# If the variable is missing entirely (e.g. the .env file was not created),
# the second argument acts as a fallback so the error message is clear
# rather than a cryptic NoneType crash inside SQLAlchemy.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "MISSING — create a .env file with DATABASE_URL set"
)

# The DATABASE_URL string follows the format:
#   postgresql://<user>:<password>@<host>/<database>
# By reading it from the environment rather than hard-coding it here,
# you can change credentials, host, or database name without touching
# source code — and without risking the password being committed to Git.
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
