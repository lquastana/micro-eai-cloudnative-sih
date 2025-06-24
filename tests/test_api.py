from fastapi.testclient import TestClient

from app.api.main import app
from app.jobs.tasks import process_message


def test_list_and_get_message(tmp_path):
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
