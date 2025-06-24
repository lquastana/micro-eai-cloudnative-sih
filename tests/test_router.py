from app.hl7.router import Router


def test_load_from_yaml(tmp_path):
    rules = tmp_path / "routes.yml"
    rules.write_text(
        "routes:\n  ADT^A01: app.jobs.tasks.handle_adt_a01\n"  
    )
    router = Router()
    router.load_from_yaml(str(rules))
    assert "ADT^A01" in router._routes
