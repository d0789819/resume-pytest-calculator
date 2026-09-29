from unittest.mock import Mock
import requests
from app.services import send_audit_event

def test_send_audit_event_posts_json(monkeypatch):
    response = Mock()
    response.raise_for_status.return_value = None
    post_mock = Mock(return_value=response)
    monkeypatch.setattr("app.services.requests.post", post_mock)

    sent = send_audit_event("https://audit.example.test/events", {"id": 7})

    assert sent is True
    post_mock.assert_called_once_with(
        "https://audit.example.test/events", json={"id": 7}, timeout=2
    )

def test_send_audit_event_handles_network_error(monkeypatch):
    post_mock = Mock(side_effect=requests.ConnectionError("offline"))
    monkeypatch.setattr("app.services.requests.post", post_mock)

    assert send_audit_event("https://audit.example.test/events", {"id": 7}) is False

def test_send_audit_event_is_disabled_without_url(monkeypatch):
    post_mock = Mock()
    monkeypatch.setattr("app.services.requests.post", post_mock)

    assert send_audit_event("", {"id": 7}) is False
    post_mock.assert_not_called()
