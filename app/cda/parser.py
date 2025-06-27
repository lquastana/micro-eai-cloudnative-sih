from xml.etree import ElementTree as ET


def parse_cda_message(data: str) -> ET.Element:
    """Parse a CDA XML document and return the root element."""
    root = ET.fromstring(data)
    if "ClinicalDocument" not in root.tag:
        raise ValueError("Invalid CDA document")
    return root
