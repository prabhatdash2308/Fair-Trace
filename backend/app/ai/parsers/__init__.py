from app.ai.parsers.registry import ParserRegistry
from app.ai.parsers.pdf_parser import PDFParser
from app.ai.parsers.docx_parser import DOCXParser
from app.ai.parsers.txt_parser import TXTParser

# Register default parsers
ParserRegistry.register(PDFParser())
ParserRegistry.register(DOCXParser())
ParserRegistry.register(TXTParser())
