import json


def parse_fhir_message(data: str) -> dict:
    """Parse a FHIR JSON message and return the resource as a dict."""
    obj = json.loads(data)
    if "resourceType" not in obj:
        raise ValueError("Invalid FHIR resource")
    return obj
