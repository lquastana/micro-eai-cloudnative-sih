from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./messages.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    from .models import Base

    Base.metadata.create_all(bind=engine)
    # simple migration to ensure new columns exist
    with engine.begin() as conn:
        cols = [row[1] for row in conn.execute(text("PRAGMA table_info(hl7_messages)")).fetchall()]
        if "status" not in cols:
            conn.execute(text("ALTER TABLE hl7_messages ADD COLUMN status VARCHAR(20)"))
