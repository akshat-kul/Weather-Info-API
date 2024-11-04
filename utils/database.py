from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from config.settings import settings
from sqlalchemy.engine.url import make_url

url_object = make_url(settings.db_url)

try:
    # Create the SQLAlchemy engine
    engine = create_engine(url_object, 
                           pool_size=10,  # Increase the pool size
                           max_overflow=20,  # Increase the overflow limit
                           pool_timeout=30,  # Adjust the timeout as needed
                           pool_pre_ping=True)  # Enable pre-ping to check connections
except Exception as e:
    raise e

# Create a sessionmaker to bind sessions to the engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative class definitions
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        raise
    finally:
        db.close()