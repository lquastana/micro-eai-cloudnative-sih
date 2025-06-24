import os
from prometheus_client import Counter

ENABLE_MONITORING = os.getenv("ENABLE_MONITORING", "false").lower() == "true"

if ENABLE_MONITORING:
    processed_counter = Counter(
        "processed_messages_total", "Total processed messages"
    )
else:
    processed_counter = None
