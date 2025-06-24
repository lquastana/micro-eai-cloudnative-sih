from app.jobs import tasks
from app.jobs.tasks import process_message


def setup_eager(monkeypatch):
    monkeypatch.setattr(tasks.deposit_message, "delay", tasks.deposit_message.run)
    monkeypatch.setattr(tasks.process_message, "delay", tasks.process_message.run)


def test_process_fhir(monkeypatch):
    setup_eager(monkeypatch)
    data = '{"resourceType":"Patient","id":"ex"}'
    msg_id = process_message.run(data)
    assert isinstance(msg_id, int)


def test_process_cda(monkeypatch):
    setup_eager(monkeypatch)
    xml = "<ClinicalDocument><id root='1'/></ClinicalDocument>"
    msg_id = process_message.run(xml)
    assert isinstance(msg_id, int)
