from app.hl7.router import Router


def test_load_from_yaml(tmp_path):
    rules = tmp_path / "routes.yml"
    rules.write_text(
        "routes:\n  ADT^A01: app.jobs.tasks.handle_adt_a01\n"  
    )
    router = Router()
    router.load_from_yaml(str(rules))
    assert any(r["type"] == "ADT^A01" for r in router._rules)


def test_conditional_route(tmp_path):
    rules = tmp_path / "routes.yml"
    rules.write_text(
        """
routes:
  - type: ADT^A01
    field: PID.3
    equals: '1234'
    handler: app.jobs.tasks.handle_adt_a01
"""
    )
    router = Router()
    router.load_from_yaml(str(rules))

    class Dummy:
        pass

    from app.hl7.parser import parse_hl7_message

    sample = "MSH|^~\\&|S|F|R|F|20200101||ADT^A01|1|P|2.5\rPID|1||1234"
    msg = parse_hl7_message(sample)
    called = {}

    def handler(m):
        called["ok"] = True

    router._rules[0]["handler"] = handler
    router.route(msg)
    assert called.get("ok")
