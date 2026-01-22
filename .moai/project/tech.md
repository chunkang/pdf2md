# pdf2md - Technology Stack

## Overview

This document outlines the recommended technology stack for the pdf2md project.

---

## Primary Language

| Attribute | Value |
|-----------|-------|
| **Language** | Python |
| **Version** | 3.11+ (recommended) |
| **Rationale** | Rich PDF processing ecosystem, excellent CLI tooling |

---

## Core Dependencies

<!-- TODO: Finalize dependency choices -->

### PDF Processing

| Library | Purpose | Status |
|---------|---------|--------|
| `pymupdf` (fitz) | Fast PDF parsing, text/image extraction | Recommended |
| `pdfplumber` | Table extraction, layout analysis | Alternative |
| `pypdf` | Basic PDF operations | Lightweight option |

### Markdown Generation

| Library | Purpose | Status |
|---------|---------|--------|
| Built-in string formatting | Simple Markdown output | Default |
| `mistune` | Markdown parsing/validation | Optional |

### CLI Framework

| Library | Purpose | Status |
|---------|---------|--------|
| `typer` | Modern CLI with type hints | Recommended |
| `click` | Mature CLI framework | Alternative |
| `argparse` | Standard library option | Fallback |

### Optional Enhancements

| Library | Purpose | Status |
|---------|---------|--------|
| `pytesseract` | OCR for scanned PDFs | Phase 3 |
| `rich` | Beautiful terminal output | Enhancement |
| `tqdm` | Progress bars for batch processing | Enhancement |

---

## Development Dependencies

### Testing

| Tool | Purpose |
|------|---------|
| `pytest` | Test framework |
| `pytest-cov` | Coverage reporting |
| `pytest-mock` | Mocking utilities |

### Code Quality

| Tool | Purpose |
|------|---------|
| `ruff` | Fast linting and formatting |
| `mypy` | Static type checking |
| `pre-commit` | Git hooks management |

### Documentation

| Tool | Purpose |
|------|---------|
| `mkdocs` | Documentation site generator |
| `mkdocs-material` | Modern documentation theme |

---

## Recommended pyproject.toml

```toml
[project]
name = "pdf2md"
version = "0.1.0"
description = "PDF to Markdown Converter"
requires-python = ">=3.11"
dependencies = [
    "pymupdf>=1.24.0",
    "typer>=0.12.0",
    "rich>=13.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.0.0",
    "ruff>=0.4.0",
    "mypy>=1.10.0",
]
ocr = [
    "pytesseract>=0.3.10",
    "pillow>=10.0.0",
]

[project.scripts]
pdf2md = "pdf2md.cli:app"

[tool.ruff]
line-length = 88
target-version = "py311"

[tool.mypy]
python_version = "3.11"
strict = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --cov=src"
```

---

## Architecture Decisions

### Decision 1: PDF Library Choice

**Decision:** Use `pymupdf` as primary PDF processor

**Rationale:**
- Fastest PDF processing in Python
- Excellent text extraction quality
- Good image and table support
- Active maintenance

**Trade-offs:**
- Larger binary size than pypdf
- C extension requires compilation

### Decision 2: CLI Framework

**Decision:** Use `typer` for CLI interface

**Rationale:**
- Modern Python type hints integration
- Automatic help generation
- Built on Click (mature foundation)
- Excellent developer experience

---

## Environment Setup

### Prerequisites

```bash
# Python 3.11+
python --version  # Should be 3.11 or higher

# Optional: uv for fast package management
pip install uv
```

### Installation (Development)

```bash
# Clone and setup
git clone <repository>
cd pdf2md

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -e ".[dev]"
```

---

## Build & Distribution

| Method | Command | Output |
|--------|---------|--------|
| Development | `pip install -e .` | Editable install |
| Build | `python -m build` | wheel + sdist |
| Publish | `twine upload dist/*` | PyPI release |

---

## Project Status

**Tech Stack Status:** Proposed (pre-development)

**Last Updated:** 2026-01-22
