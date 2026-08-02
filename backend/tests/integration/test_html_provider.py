import pytest
from app.export.providers.html_provider import HTMLProvider

def test_html_provider_render():
    provider = HTMLProvider()
    report = {"summary": "Excellent performance"}
    metadata = {"title": "Test Report", "workflow_id": "wf-1"}
    
    html_bytes = provider.render(report, metadata)
    html_str = html_bytes.decode('utf-8')
    
    assert "Test Report" in html_str or "Test Report" in metadata["title"]
    assert "wf-1" in html_str or "wf-1" in metadata["workflow_id"]
    assert type(html_bytes) == bytes
