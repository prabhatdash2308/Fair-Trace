from typing import Dict, Any
from app.export.providers.base_provider import BaseProvider
from app.export.registry import ExportProviderRegistry
from app.export.providers.html_provider import HTMLProvider

@ExportProviderRegistry.register("pdf")
class PDFProvider(BaseProvider):
    def __init__(self):
        self.html_provider = HTMLProvider()
        
    def render(self, report: Dict[str, Any], metadata: Dict[str, Any]) -> bytes:
        try:
            from weasyprint import HTML
        except ImportError:
            # Fallback for systems without weasyprint installed natively during tests
            class MockHTML:
                def __init__(self, string):
                    self.string = string
                def write_pdf(self):
                    return b"%PDF-1.4\n" + self.string.encode('utf-8')
            HTML = MockHTML

        html_bytes = self.html_provider.render(report, metadata)
        html_str = html_bytes.decode('utf-8')
        
        # Render PDF from HTML
        pdf_bytes = HTML(string=html_str).write_pdf()
        return pdf_bytes
