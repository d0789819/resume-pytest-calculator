"""Clients for services outside this application."""

import requests


def send_audit_event(url: str, event: dict) -> bool:
    """Send an audit event; an empty URL disables the optional integration."""
    if not url:
        return False

    try:
        response = requests.post(url, json=event, timeout=2)
        response.raise_for_status()
    except requests.RequestException:
        # Auditing is intentionally best-effort and must not break the API.
        return False

    return True
