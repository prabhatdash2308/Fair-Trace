# Phase 11.12: Export Engine Architecture

## Overview
The Export Engine converts the structured LangGraph final `EnterprisePerformanceReport` into immutable Enterprise PDFs and HTML reports. This encapsulates Phase 11.12 and represents the terminal operation of the AI-driven Review Guard system.

## Provider Registry Pattern
The export engine is built generically:
- **`HTMLProvider`**: Consumes Jinja2 templates (`enterprise.html`, `styles.css`, `header.html`, `footer.html`) injected directly with the `report` JSON block and workflow `metadata`.
- **`PDFProvider`**: Uses **WeasyPrint** (and `pydyf`) to process the HTML bytes and return a print-ready, pixel-perfect PDF.

## Security & Auditing
- **Cryptographic Hashing**: An embedded SHA256 signature hashes the exact report content, workflow ID, and approval timestamps to ensure report integrity.
- **`ReportExport` Table**: The DB model tracks `checksum`, `storage_path`, and precise `generated_at` timestamps to act as an unassailable audit trail.

## Immutability Rule
Once a `ReportExport` transitions to `READY`, it cannot be altered. The generated signature proves mathematically that the report matches exactly the content evaluated and approved by the Human-in-the-Loop stage.
