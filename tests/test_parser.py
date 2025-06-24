from app.hl7.parser import parse_hl7_message, get_message_type


def test_parse_and_type():
    message = "MSH|^~\\&|SENDING|FAC|RECV|FAC|202001010000||ADT^A01|MSG00001|P|2.5\rPID|1||1234||DOE^JOHN"
    parsed = parse_hl7_message(message)
    assert get_message_type(parsed) == "ADT^A01"
from app.fhir.parser import parse_fhir_message
from app.cda.parser import parse_cda_message


def test_parse_fhir():
    data = '{"resourceType":"Patient","id":"p1"}'
    res = parse_fhir_message(data)
    assert res["resourceType"] == "Patient"


def test_parse_cda():
    xml = "<ClinicalDocument><id root='1'/></ClinicalDocument>"
    root = parse_cda_message(xml)
    assert 'ClinicalDocument' in root.tag
