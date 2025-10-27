from sqlalchemy import create_engine
from app.config import DATABASE_URL, SQLALCHEMY_ECHO

# Global SQLAlchemy synchronous engine
engine = create_engine(DATABASE_URL, future=True, echo=SQLALCHEMY_ECHO)
