from app.jobs import tasks
from app.jobs.tasks import process_message, retry_failed_messages


def test_retry_failed(monkeypatch):
    # ensure eager execution
    monkeypatch.setattr(tasks.deposit_message, "delay", tasks.deposit_message.run)
    monkeypatch.setattr(tasks.process_message, "delay", tasks.process_message.run)
    # handler that raises to force error
    def bad_handler(msg):
        raise RuntimeError("boom")

    tasks.router._rules[0]["handler"] = bad_handler
    msg_id = process_message.run("MSH|^~\&|S|F|R|F|20200101||ADT^A01|1|P|2.5")
    count = retry_failed_messages.run()
    assert count >= 1


def test_deposit_message_error(monkeypatch):
    monkeypatch.setattr(tasks, "upload_file", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("boom")))
    monkeypatch.setattr(tasks.deposit_message, "delay", tasks.deposit_message.run)
    monkeypatch.setattr(tasks.process_message, "delay", tasks.process_message.run)

    msg_id = process_message.run("MSH|^~\&|S|F|R|F|20200101||ADT^A01|1|P|2.5")
    assert not tasks.deposit_message.run(msg_id)

    from app.db.session import SessionLocal
    from app.db.models import HL7Message

    db = SessionLocal()
    status = db.query(HL7Message).get(msg_id).status
    db.close()
    assert status == "error"
