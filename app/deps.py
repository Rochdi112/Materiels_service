from contextlib import contextmanager
from sqlmodel import Session
from app.database import get_session

def get_db():
    db = get_session()
    try:
        yield db
    finally:
        db.close()
