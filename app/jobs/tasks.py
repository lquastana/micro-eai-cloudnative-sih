"""Celery tasks for message processing."""
import os
from celery import Celery
from loguru import logger
from pathlib import Path

from ..hl7.parser import parse_hl7_message
from ..fhir.parser import parse_fhir_message
from ..cda.parser import parse_cda_message
from ..hl7.router import Router
from ..sftp.client import download_files
from ..db.session import SessionLocal
from ..db.models import HL7Message


broker_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
celery_app = Celery(__name__, broker=broker_url)


# simple router instance with example handler
router = Router()


def handle_adt_a01(message):
    """Example handler for ADT^A01 messages."""
    logger.info("Handled ADT^A01 message")


def handle_oru_r01(message):
    """Example handler for ORU^R01 messages."""
    logger.info("Handled ORU^R01 message")


router.add_route("ADT^A01", handle_adt_a01)
router.add_route("ORU^R01", handle_oru_r01)

routes_file = os.getenv("ROUTES_FILE")
if routes_file and os.path.exists(routes_file):
    router.load_from_yaml(routes_file)


@celery_app.task
def poll_sftp():
    """Download HL7 files from an SFTP server and process them."""
    host = os.getenv("SFTP_HOST")
    user = os.getenv("SFTP_USER")
    password = os.getenv("SFTP_PASSWORD")
    remote_dir = os.getenv("SFTP_REMOTE_DIR", "/")
    local_dir = os.getenv("SFTP_LOCAL_DIR", "./sftp")
    if not host or not user or not password:
        logger.warning("SFTP credentials not configured")
        return 0
    download_files(host, user, password, remote_dir, local_dir)
    count = 0
    for file in Path(local_dir).iterdir():
        if file.is_file():
            text = file.read_text()
            process_message.delay(text)
            file.unlink()
            count += 1
    return count


@celery_app.task
def process_message(text: str):
    format = "HL7"
    try:
        msg = parse_hl7_message(text)
        message_type = msg.MSH.MSH_9.to_er7()
    except Exception:
        try:
            fhir = parse_fhir_message(text)
            format = "FHIR"
            message_type = f"FHIR:{fhir.get('resourceType')}"
            msg = None
        except Exception:
            cda = parse_cda_message(text)
            format = "CDA"
            message_type = f"CDA:{cda.tag}"
            msg = None
    db = SessionLocal()
    db_msg = HL7Message(raw=text, message_type=message_type)
    db.add(db_msg)
    db.commit()
    msg_id = db_msg.id
    db.close()
    if msg is not None:
        try:
            router.route(msg)
        except Exception as exc:
            logger.exception("Routing failed: {}", exc)
    return msg_id


@celery_app.task
def replay_message(message_id: int):
    db = SessionLocal()
    msg = db.query(HL7Message).get(message_id)
    db.close()
    if msg:
        process_message.delay(msg.raw)
        return True
    return False
