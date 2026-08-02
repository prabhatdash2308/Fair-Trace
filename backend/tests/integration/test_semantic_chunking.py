import pytest
from uuid import uuid4
from app.ai.chunking.semantic_chunker import SemanticChunker
from app.ai.chunking.utils import detect_document_type
from models.db.document import Document

def test_semantic_chunker_detects_hr_headings():
    chunker = SemanticChunker()
    
    text = """Employee Name: John Doe
Review Period: Q3 2026
Manager: Jane Smith

Manager Feedback:
""" + ("John has done a great job this quarter. " * 500) + """

Performance Rating:
Exceeds Expectations
""" + ("This rating is justified because... " * 500)
    
    doc = Document(
        id=uuid4(),
        owner_id=uuid4(),
        parsed_text=text,
        parser_version="1.0"
    )
    
    chunks = chunker.split_document(doc)
    
    # Check that metadata was extracted
    # HR info applies globally or dynamically
    assert chunks[0].metadata.employee_name == "John Doe"
    assert chunks[0].metadata.review_period == "Q3 2026"
    assert chunks[0].metadata.manager_name == "Jane Smith"
    
    # We should have identified the headings
    # chunks might be split by \n\n, let's see which chunk gets the Manager Feedback
    found_heading = False
    for c in chunks:
        if c.metadata.heading == "Manager Feedback":
            found_heading = True
            break
            
    assert found_heading

def test_detect_document_type():
    assert detect_document_type("This is an annual review for John.") == "Performance Review"
    assert detect_document_type("Here is my Curriculum Vitae") == "Resume"
    assert detect_document_type("Random text without keywords") == "Other"
