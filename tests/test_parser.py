from app.hl7.parser import parse_hl7_message, get_message_type


def test_parse_and_type():
    message = "MSH|^~\\&|SENDING|FAC|RECV|FAC|202001010000||ADT^A01|MSG00001|P|2.5\rPID|1||1234||DOE^JOHN"
    parsed = parse_hl7_message(message)
    assert get_message_type(parsed) == "ADT^A01"
