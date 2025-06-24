"""Celery tasks for message processing."""
import os
from celery import Celery

from ..hl7.parser import parse_hl7_message
from ..db.session import SessionLocal
from ..db.models import HL7Message


broker_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
celery_app = Celery(__name__, broker=broker_url)


@celery_app.task
def process_message(text: str):
    msg = parse_hl7_message(text)
    db = SessionLocal()
    db_msg = HL7Message(raw=text, message_type=msg.MSH.MSH_9.to_er7())
    db.add(db_msg)
    db.commit()
    db.close()
    return db_msg.id
