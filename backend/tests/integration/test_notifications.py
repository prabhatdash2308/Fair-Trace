import pytest
from app.workflows.notification_service import NotificationService, LogProvider

def test_notification_service_log_provider():
    provider = LogProvider()
    assert provider.health()["status"] == "healthy"
    
    result = provider.send("test@example.com", "Subject", "Message")
    assert result is True
    
    bulk_results = provider.send_bulk(["test@example.com", "test2@example.com"], "Subj", "Msg")
    assert bulk_results["test@example.com"] is True
    assert bulk_results["test2@example.com"] is True

def test_notification_service_singleton():
    NotificationService.set_provider(LogProvider())
    assert NotificationService.notify("a@b.com", "Test", "Test Message") is True
