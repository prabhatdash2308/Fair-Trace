import os

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), '..', 'fixtures')
os.makedirs(FIXTURES_DIR, exist_ok=True)

FIXTURES = {
    "excellent_employee.pdf": "<h1>Performance Review</h1><p>John has exceeded all expectations this year. He consistently delivers high-quality code and mentors junior developers.</p>",
    "average_employee.pdf": "<h1>Performance Review</h1><p>Jane met most of her goals. She struggles occasionally with deadlines but her code quality is adequate.</p>",
    "biased_review.pdf": "<h1>Performance Review</h1><p>Sam is too old to understand new frameworks. He should stick to legacy code. He is a 'dinosaur' in the team.</p>",
    "corrupt_document.pdf": "Not a PDF file",
    "empty_document.pdf": "<h1></h1>"
}

from fpdf import FPDF

def create_pdf(filepath, text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", size=12)
    pdf.multi_cell(0, 10, txt=text)
    pdf.output(filepath)

def generate_fixtures():
    for filename, html_content in FIXTURES.items():
        filepath = os.path.join(FIXTURES_DIR, filename)
        if filename == "corrupt_document.pdf":
            with open(filepath, "wb") as f:
                f.write(b"CORRUPT DATA NO PDF HEADER")
        else:
            # simple strip HTML for FPDF since we only have basic p and h1 tags here
            text = html_content.replace("<h1>", "").replace("</h1>", "\n\n").replace("<p>", "").replace("</p>", "\n")
            create_pdf(filepath, text)
            
    # Huge document
    huge_text = "Huge Review\n\n" + "Sample text for chunking test.\n" * 1000
    create_pdf(os.path.join(FIXTURES_DIR, "huge_document.pdf"), huge_text)
    
    # Word doc
    # For now just touch a dummy docx
    with open(os.path.join(FIXTURES_DIR, "promotion_case.docx"), "wb") as f:
        f.write(b"DUMMY DOCX")

if __name__ == "__main__":
    generate_fixtures()
    print("Fixtures generated.")
