from fastapi import FastAPI, Depends, HTTPException
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


@app.get("/messages/{message_id}")
def get_message(message_id: int, db: Session = Depends(get_db)):
    message = db.query(models.HL7Message).get(message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return message


@app.post("/messages/{message_id}/replay")
def replay_message(message_id: int, db: Session = Depends(get_db)):
    message = db.query(models.HL7Message).get(message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    from ..jobs.tasks import replay_message as replay_task

    replay_task.delay(message_id)
    return {"status": "queued"}
