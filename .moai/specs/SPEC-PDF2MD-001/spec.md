# SPEC-PDF2MD-001: PDF to Markdown Converter MVP

## Metadata

| Field | Value |
|-------|-------|
| **SPEC ID** | SPEC-PDF2MD-001 |
| **Title** | PDF to Markdown Converter MVP |
| **Status** | Planned |
| **Priority** | High |
| **Created** | 2026-01-22 |
| **Lifecycle** | spec-anchored |
| **Assigned** | manager-tdd |

---

## Environment

### Runtime Environment

- **Language**: Python 3.11+
- **Primary Library**: pymupdf (fitz) >= 1.24.0
- **CLI Framework**: typer >= 0.12.0
- **Terminal Enhancement**: rich >= 13.0.0

### Development Environment

- **Testing**: pytest >= 8.0.0, pytest-cov >= 4.0.0
- **Linting**: ruff >= 0.4.0
- **Type Checking**: mypy >= 1.10.0
- **Package Format**: pyproject.toml

### Target Platforms

- macOS 12+
- Linux (Ubuntu 20.04+, Debian 11+)
- Windows 10+

---

## Assumptions

### Technical Assumptions

| Assumption | Confidence | Risk if Wrong |
|------------|------------|---------------|
| pymupdf provides accurate text extraction for standard PDFs | High | Core functionality fails; fallback to pdfplumber |
| Font size ratios reliably indicate heading levels | Medium | Heading detection inaccurate; require heuristic tuning |
| Text blocks maintain reading order in extraction | Medium | Output sequence incorrect; require layout analysis |
| CLI users have Python 3.11+ installed | High | Installation fails; document prerequisites |

### Business Assumptions

| Assumption | Confidence | Risk if Wrong |
|------------|------------|---------------|
| Users primarily work with text-heavy PDFs | High | Feature scope expands to images/tables earlier |
| Single-file conversion is primary use case | High | Batch processing priority increases |
| Markdown output is destination format | High | Additional format support needed |

---

## Requirements

### Ubiquitous Requirements (Always Active)

| ID | Requirement |
|----|-------------|
| REQ-U-001 | The system **shall** preserve text content fidelity at 95% accuracy or higher during PDF to Markdown conversion. |
| REQ-U-002 | The system **shall** maintain UTF-8 encoding for all text output. |
| REQ-U-003 | The system **shall** log errors to stderr without interrupting conversion when recoverable. |
| REQ-U-004 | The system **shall** provide progress feedback during conversion operations. |

### Event-Driven Requirements (WHEN-THEN)

| ID | Requirement |
|----|-------------|
| REQ-E-001 | **WHEN** user provides a valid PDF file path **THEN** the system **shall** generate a Markdown file with extracted text content. |
| REQ-E-002 | **WHEN** user specifies an output path **THEN** the system **shall** write the Markdown to the specified location. |
| REQ-E-003 | **WHEN** user omits output path **THEN** the system **shall** generate output filename by replacing .pdf extension with .md. |
| REQ-E-004 | **WHEN** text with larger font size is detected **THEN** the system **shall** convert it to appropriate Markdown heading level (h1-h6). |
| REQ-E-005 | **WHEN** bullet or numbered list patterns are detected **THEN** the system **shall** convert them to Markdown list syntax. |
| REQ-E-006 | **WHEN** conversion completes successfully **THEN** the system **shall** display summary with page count and output path. |

### State-Driven Requirements (IF-THEN)

| ID | Requirement |
|----|-------------|
| REQ-S-001 | **IF** the input file does not exist **THEN** the system **shall** exit with error code 1 and descriptive message. |
| REQ-S-002 | **IF** the input file is not a valid PDF **THEN** the system **shall** exit with error code 2 and descriptive message. |
| REQ-S-003 | **IF** the output file already exists **THEN** the system **shall** prompt for overwrite confirmation unless --force flag is provided. |
| REQ-S-004 | **IF** the PDF is password-protected **THEN** the system **shall** exit with error code 3 and message indicating password protection. |
| REQ-S-005 | **IF** the PDF contains no extractable text **THEN** the system **shall** warn user and suggest OCR for scanned documents. |

### Unwanted Requirements (SHALL NOT)

| ID | Requirement |
|----|-------------|
| REQ-N-001 | The system **shall not** modify or alter the original PDF file. |
| REQ-N-002 | The system **shall not** process files without .pdf extension unless explicitly overridden. |
| REQ-N-003 | The system **shall not** silently overwrite existing files without user consent or --force flag. |
| REQ-N-004 | The system **shall not** expose internal stack traces to end users in production mode. |

### Optional Requirements (WHERE POSSIBLE)

| ID | Requirement |
|----|-------------|
| REQ-O-001 | **Where possible**, the system **shall** preserve paragraph structure from the original PDF. |
| REQ-O-002 | **Where possible**, the system **shall** detect and convert inline code patterns to backtick syntax. |
| REQ-O-003 | **Where possible**, the system **shall** provide rich terminal output with colors and formatting. |

---

## Specifications

### CLI Interface Specification

```
pdf2md [OPTIONS] INPUT_FILE [OUTPUT_FILE]

Arguments:
  INPUT_FILE   Path to the PDF file to convert (required)
  OUTPUT_FILE  Path for the output Markdown file (optional)

Options:
  --force, -f        Overwrite output file without confirmation
  --verbose, -v      Enable verbose output with debug information
  --quiet, -q        Suppress all output except errors
  --version          Show version and exit
  --help             Show help message and exit
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Input file not found |
| 2 | Invalid PDF file |
| 3 | Password-protected PDF |
| 4 | Output write error |
| 5 | Unexpected error |

### Module Architecture

```
src/
  __init__.py           # Package initialization
  cli.py                # Typer CLI application
  converter.py          # Main conversion orchestrator
  extractors/
    __init__.py
    text.py             # Text extraction from PDF
    structure.py        # Structure detection (headings, lists)
  formatters/
    __init__.py
    markdown.py         # Markdown formatting logic
  utils/
    __init__.py
    file_ops.py         # File I/O utilities
    validation.py       # Input validation
```

### Data Flow

```
PDF Input
    |
    v
[Validation] --> Error --> Exit with code
    |
    v (valid)
[Text Extraction] --> pymupdf fitz
    |
    v
[Structure Detection] --> Headings, Lists
    |
    v
[Markdown Formatting]
    |
    v
[File Output] --> .md file
    |
    v
[Summary Display]
```

---

## Traceability

| Requirement | Test Case | Implementation |
|-------------|-----------|----------------|
| REQ-U-001 | TC-001: Text fidelity validation | converter.py |
| REQ-E-001 | TC-002: Basic conversion test | cli.py, converter.py |
| REQ-E-004 | TC-003: Heading detection test | extractors/structure.py |
| REQ-E-005 | TC-004: List detection test | extractors/structure.py |
| REQ-S-001 | TC-005: Missing file error test | utils/validation.py |
| REQ-S-002 | TC-006: Invalid PDF error test | utils/validation.py |
| REQ-N-001 | TC-007: Original file unchanged test | converter.py |

---

## Dependencies

### External Dependencies

| Dependency | Version | Purpose |
|------------|---------|---------|
| pymupdf | >= 1.24.0 | PDF parsing and text extraction |
| typer | >= 0.12.0 | CLI framework with type hints |
| rich | >= 13.0.0 | Terminal formatting and progress |

### Development Dependencies

| Dependency | Version | Purpose |
|------------|---------|---------|
| pytest | >= 8.0.0 | Test framework |
| pytest-cov | >= 4.0.0 | Coverage reporting |
| ruff | >= 0.4.0 | Linting and formatting |
| mypy | >= 1.10.0 | Static type checking |

---

## Constraints

### Performance Constraints

- Processing speed: < 5 seconds per page for text-only PDFs
- Memory usage: < 500MB for PDFs up to 100 pages
- Startup time: < 1 second for CLI initialization

### Compatibility Constraints

- PDF versions: 1.0 through 2.0
- Text encoding: UTF-8 output only
- File size: Tested up to 50MB PDFs

### Security Constraints

- No network access required
- No elevated permissions needed
- No sensitive data logging

---

## Related SPECs

| SPEC ID | Relationship | Description |
|---------|--------------|-------------|
| SPEC-PDF2MD-002 | Extends | Image extraction and embedding (Phase 2) |
| SPEC-PDF2MD-003 | Extends | Table extraction and conversion (Phase 2) |
| SPEC-PDF2MD-004 | Extends | OCR for scanned documents (Phase 3) |

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-01-22 | manager-spec | Initial SPEC creation |
