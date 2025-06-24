from hl7apy.parser import parse_message, parse_segment
from hl7apy.exceptions import HL7apyException


def parse_hl7_message(data: str):
    """Parse an HL7 message string and return the message object."""
    try:
        return parse_message(data, find_groups=False)
    except HL7apyException as exc:
        raise ValueError(f"Invalid HL7 message: {exc}") from exc


def get_message_type(message) -> str:
    """Return the HL7 message type (MSH-9)."""
    try:
        return message.MSH.MSH_9.to_er7()
    except AttributeError:
        return "UNKNOWN"
