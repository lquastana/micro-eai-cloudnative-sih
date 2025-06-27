"""Loki logging integration for Loguru."""

import os
import time
import requests
from loguru import logger

LOKI_URL = os.getenv("LOKI_URL")


def _loki_sink(message):
    record = message.record
    ts = int(record["time"].timestamp() * 1_000_000_000)
    payload = {
        "streams": [
            {
                "stream": {"app": "micro-eai", "level": record["level"].name},
                "values": [[str(ts), record["message"]]],
            }
        ]
    }
    try:
        requests.post(LOKI_URL, json=payload, timeout=1)
    except Exception:
        pass


def setup_logging():
    if LOKI_URL:
        logger.add(_loki_sink)
