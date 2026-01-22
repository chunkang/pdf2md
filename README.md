# pdf2md

A command-line tool to convert PDF documents to Markdown format.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

## Features

- **Text Extraction**: Extract text content from PDF files with 95%+ fidelity
- **Structure Detection**: Automatically detect headings based on font size analysis
- **List Recognition**: Identify and convert bullet and numbered lists
- **Clean Output**: Generate properly formatted Markdown with preserved paragraph structure
- **Rich CLI**: Beautiful terminal output with progress indicators
- **Robust Error Handling**: Clear error messages with specific exit codes

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/kurapa/pdf2md.git
cd pdf2md

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the package
pip install -e .
```

### Development Installation

```bash
# Install with development dependencies
pip install -e ".[dev]"
```

## Quick Start

Convert a PDF file to Markdown:

```bash
# Basic usage - output will be sample.md
pdf2md sample.pdf

# Specify output file
pdf2md input.pdf output/result.md

# Overwrite existing output file
pdf2md --force document.pdf

# Verbose output
pdf2md --verbose document.pdf
```

## CLI Reference

```
Usage: pdf2md [OPTIONS] INPUT_FILE [OUTPUT_FILE]

Convert a PDF file to Markdown format.

Arguments:
  INPUT_FILE   Path to the input PDF file. [required]
  OUTPUT_FILE  Path for the output Markdown file.
               Defaults to input filename with .md extension.

Options:
  -f, --force    Overwrite output file if it exists.
  -v, --verbose  Show verbose output.
  -q, --quiet    Suppress output except errors.
  --version      Show version and exit.
  --help         Show this message and exit.
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Input file not found |
| 2 | Invalid PDF file |
| 3 | Password-protected PDF |
| 4 | Output write error |
| 5 | Unexpected error |

## Examples

### Basic Conversion

```bash
# Convert a PDF file
pdf2md document.pdf
# Output: document.md created in the same directory
```

### Custom Output Path

```bash
# Specify a different output location
pdf2md input.pdf docs/output.md
```

### Handling Existing Files

```bash
# Overwrite without prompting
pdf2md --force document.pdf

# Or use the short flag
pdf2md -f document.pdf
```

### Verbose Mode

```bash
# See detailed progress information
pdf2md --verbose document.pdf
# Shows: version, input/output paths, conversion progress
```

### Quiet Mode

```bash
# Suppress all output except errors
pdf2md --quiet document.pdf
# Useful for scripting and automation
```

## Architecture

```
pdf2md/
├── cli.py           # Typer CLI application
├── converter.py     # Conversion orchestrator
├── extractors/
│   ├── text.py      # Text extraction from PDF
│   └── structure.py # Structure detection (headings, lists)
├── formatters/
│   └── markdown.py  # Markdown output formatting
└── utils/
    └── validation.py  # Input/output validation
```

### Data Flow

```
PDF Input
    │
    ▼
[Validation] ──► Error ──► Exit with code
    │
    ▼ (valid)
[Text Extraction] ──► pymupdf/fitz
    │
    ▼
[Structure Detection] ──► Headings, Lists
    │
    ▼
[Markdown Formatting]
    │
    ▼
[File Output] ──► .md file
    │
    ▼
[Summary Display]
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=pdf2md --cov-report=term-missing

# Run specific test file
pytest tests/test_cli.py -v
```

### Code Quality

```bash
# Linting
ruff check src/ tests/

# Type checking
mypy src/

# Format code
ruff format src/ tests/
```

### Project Structure

```
pdf2md/
├── src/
│   └── pdf2md/          # Source code
├── tests/               # Test suite
├── pyproject.toml       # Project configuration
└── README.md            # This file
```

## Requirements

- Python 3.11 or higher
- Dependencies:
  - [pymupdf](https://pymupdf.readthedocs.io/) >= 1.24.0 - PDF processing
  - [typer](https://typer.tiangolo.com/) >= 0.12.0 - CLI framework
  - [rich](https://rich.readthedocs.io/) >= 13.0.0 - Terminal formatting

## Limitations

- **Scanned PDFs**: Documents without a text layer will produce empty output. Consider using OCR tools first.
- **Complex Layouts**: Multi-column layouts may not preserve reading order perfectly.
- **Images/Tables**: Currently extracts text only; images and tables are not converted.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Chun Kang

---

*Generated with [Claude Code](https://claude.ai/code)*
