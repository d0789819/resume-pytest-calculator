from unittest.mock import Mock


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_create_and_get_calculation(client, monkeypatch):
    audit_mock = Mock(return_value=True)
    monkeypatch.setattr("app.routes.send_audit_event", audit_mock)

    created = client.post(
        "/calculations", json={"operation": "add", "a": 2, "b": 3}
    )

    assert created.status_code == 201
    assert created.get_json()["result"] == 5.0
    calculation_id = created.get_json()["id"]

    fetched = client.get(f"/calculations/{calculation_id}")
    assert fetched.status_code == 200
    assert fetched.get_json()["operation"] == "add"
    audit_mock.assert_called_once_with(
        "https://audit.example.test/events",
        {"action": "calculation.created", "calculation_id": calculation_id},
    )


def test_list_update_and_delete_calculation(client, monkeypatch):
    monkeypatch.setattr("app.routes.send_audit_event", Mock(return_value=True))
    created = client.post(
        "/calculations", json={"operation": "add", "a": 4, "b": 2}
    )
    calculation_id = created.get_json()["id"]

    listed = client.get("/calculations")
    assert len(listed.get_json()) == 1

    updated = client.put(
        f"/calculations/{calculation_id}",
        json={"operation": "divide", "a": 9, "b": 3},
    )
    assert updated.status_code == 200
    assert updated.get_json()["result"] == 3.0

    deleted = client.delete(f"/calculations/{calculation_id}")
    assert deleted.status_code == 204
    assert client.get(f"/calculations/{calculation_id}").status_code == 404


def test_rejects_division_by_zero(client):
    response = client.post(
        "/calculations", json={"operation": "divide", "a": 9, "b": 0}
    )

    assert response.status_code == 400
    assert response.get_json() == {"error": "cannot divide by zero"}


def test_rejects_missing_field(client):
    response = client.post("/calculations", json={"operation": "add", "a": 1})

    assert response.status_code == 400
    assert response.get_json() == {"error": "missing fields: b"}


def test_rejects_non_numeric_operands(client):
    response = client.post(
        "/calculations", json={"operation": "add", "a": "1", "b": 2}
    )

    assert response.status_code == 400
    assert response.get_json() == {"error": "a and b must be numbers"}


def test_rejects_unknown_operation(client):
    response = client.post(
        "/calculations", json={"operation": "multiply", "a": 2, "b": 3}
    )

    assert response.status_code == 400
    assert response.get_json() == {"error": "operation must be 'add' or 'divide'"}
