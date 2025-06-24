from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, StreamingResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..db.session import SessionLocal, init_db
from ..db import models


init_db()
app = FastAPI(title="micro-eai-cloudnative-sih")
templates = Jinja2Templates(directory="app/api/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/messages")
def list_messages(db: Session = Depends(get_db)):
    return db.query(models.HL7Message).all()


@app.get("/messages/export")
def export_messages(format: str = "json", db: Session = Depends(get_db)):
    messages = db.query(models.HL7Message).all()
    if format == "csv":
        import csv
        from io import StringIO

        buf = StringIO()
        writer = csv.writer(buf)
        writer.writerow(["id", "message_type", "raw"])
        for m in messages:
            writer.writerow([m.id, m.message_type, m.raw])
        buf.seek(0)
        return StreamingResponse(buf, media_type="text/csv")
    return messages


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


@app.get("/ui/messages", response_class=HTMLResponse)
def ui_list_messages(request: Request, db: Session = Depends(get_db)):
    messages = db.query(models.HL7Message).all()
    return templates.TemplateResponse(
        "messages.html", {"request": request, "messages": messages}
    )


@app.post("/ui/messages/{message_id}/replay")
def ui_replay_message(message_id: int, db: Session = Depends(get_db)):
    from ..jobs.tasks import replay_message as replay_task

    message = db.query(models.HL7Message).get(message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    replay_task.delay(message_id)
    return RedirectResponse(url="/ui/messages", status_code=303)
