from sqlmodel import Session, create_engine, SQLModel

DATABASE_URL = "sqlite:///./materiels.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def get_db():
    with Session(engine) as session:
        yield session