import pytest
from unittest.mock import patch

def test_pdf_provider_render():
    with patch("app.export.providers.pdf_provider.PDFProvider.render") as mock_render:
        mock_render.return_value = b"%PDF-1.4\nMock PDF Content"
        
        from app.export.providers.pdf_provider import PDFProvider
        provider = PDFProvider()
        
        report = {"summary": "Excellent performance"}
        metadata = {"title": "Test Report", "workflow_id": "wf-1"}
        
        pdf_bytes = provider.render(report, metadata)
        
        assert type(pdf_bytes) == bytes
        assert pdf_bytes.startswith(b"%PDF")
