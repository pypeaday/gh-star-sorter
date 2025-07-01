import logging
import os
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Use an absolute path to be clear about where the DB file is.
# The working directory in the container is /app.
db_path = os.path.abspath("./data/gh_stars.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}"

logging.info(f"DATABASE_URL is configured to: {SQLALCHEMY_DATABASE_URL}")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    """Initializes the database and creates tables, with detailed error logging."""
    logging.info("Attempting to initialize database...")
    try:
        from . import models
        Base.metadata.create_all(bind=engine)
        logging.info("Database tables checked/created successfully.")
    except OperationalError as e:
        logging.error("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        logging.error(f"!! DATABASE CONNECTION FAILED: Could not open the database file.")
        logging.error(f"!! Path: {db_path}")
        logging.error(f"!! Underlying Error: {e}")
        logging.error("!!")
        logging.error("!! COMMON CAUSES & SOLUTIONS:")
        logging.error("!! 1. PERMISSIONS: The user running the app does not have write access to the directory.")
        logging.error(f"!!    -> Check permissions for the directory: {os.path.dirname(db_path)}")
        logging.error("!! 2. MISSING DIRECTORY: The directory does not exist.")
        logging.error("!!    -> Ensure your entrypoint script or Dockerfile creates the directory.")
        logging.error("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        raise e


