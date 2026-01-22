# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-01-22

### Added

- Initial release of pdf2md CLI tool
- PDF text extraction using pymupdf
- Automatic heading detection based on font size analysis
- Bullet and numbered list recognition
- Paragraph structure preservation
- CLI interface with typer framework
- Rich terminal output with progress indicators
- Command-line options:
  - `--force` / `-f`: Overwrite existing output files
  - `--verbose` / `-v`: Show detailed progress
  - `--quiet` / `-q`: Suppress output except errors
  - `--version`: Display version information
- Comprehensive error handling with specific exit codes (0-5)
- Input validation for PDF files
- Password-protected PDF detection
- UTF-8 output encoding

### Technical Details

- Python 3.11+ support
- 87 unit tests with 92% code coverage
- Type hints throughout codebase
- Modular architecture with separation of concerns:
  - Extractors: text.py, structure.py
  - Formatters: markdown.py
  - Utils: validation.py

---

*Generated with [Claude Code](https://claude.ai/code)*
