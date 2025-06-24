from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from ..db.session import SessionLocal, init_db
from ..db import models


init_db()
app = FastAPI(title="micro-eai-cloudnative-sih")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/messages")
def list_messages(db: Session = Depends(get_db)):
    return db.query(models.HL7Message).all()
