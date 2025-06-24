from fastapi.testclient import TestClient

from app.api.main import app
from app.jobs import tasks
from app.jobs.tasks import process_message


def setup_eager(monkeypatch):
    monkeypatch.setattr(tasks.deposit_message, "delay", tasks.deposit_message.run)
    monkeypatch.setattr(tasks.replay_message, "delay", tasks.replay_message.run)
    monkeypatch.setattr(tasks.process_message, "delay", tasks.process_message.run)


def test_list_and_get_message(tmp_path, monkeypatch):
    setup_eager(monkeypatch)
    sample = "MSH|^~\\&|SENDING|FAC|RECV|FAC|202001010000||ADT^A01|MSG00001|P|2.5\rPID|1||1234||DOE^JOHN"

    # store message using task in eager mode
    message_id = process_message.run(sample)

    client = TestClient(app)
    resp = client.get("/messages")
    assert resp.status_code == 200
    data = resp.json()
    assert any(m["id"] == message_id for m in data)

    resp = client.get(f"/messages/{message_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == message_id

    resp = client.get("/messages/export", params={"format": "csv"})
    assert resp.status_code == 200
    assert "text/csv" in resp.headers["content-type"]


def test_html_search_and_replay(tmp_path, monkeypatch):
    setup_eager(monkeypatch)
    sample = "MSH|^~\\&|S|F|R|F|20200101||ADT^A01|1|P|2.5\rPID|1||999"
    message_id = process_message.run(sample)

    client = TestClient(app)
    resp = client.get("/ui/messages", params={"q": "999"})
    assert resp.status_code == 200
    assert str(message_id) in resp.text


def test_deposit_message(monkeypatch):
    setup_eager(monkeypatch)

    uploads = {}

    def fake_upload(host, user, password, local_path, remote_path):
        uploads["path"] = remote_path

    monkeypatch.setenv("SFTP_HOST", "x")
    monkeypatch.setenv("SFTP_USER", "u")
    monkeypatch.setenv("SFTP_PASSWORD", "p")
    monkeypatch.setenv("SFTP_UPLOAD_DIR", "/out")
    monkeypatch.setattr(tasks, "upload_file", fake_upload)

    msg_id = process_message.run("MSH|^~\\&|S|F|R|F|20200101||ADT^A01|1|P|2.5")
    assert tasks.deposit_message.run(msg_id)
    assert uploads["path"].endswith(f"{msg_id}.hl7")
