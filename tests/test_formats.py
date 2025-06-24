from app.jobs.tasks import process_message


def test_process_fhir():
    data = '{"resourceType":"Patient","id":"ex"}'
    msg_id = process_message.run(data)
    assert isinstance(msg_id, int)


def test_process_cda():
    xml = "<ClinicalDocument><id root='1'/></ClinicalDocument>"
    msg_id = process_message.run(xml)
    assert isinstance(msg_id, int)
