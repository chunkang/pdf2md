# pdf2md - Project Structure

## Directory Overview

<!-- TODO: Update this structure as the project develops -->

```
pdf2md/
├── .claude/                 # MoAI-ADK agent configuration
│   ├── agents/              # Specialized agent definitions
│   ├── commands/            # Slash command definitions
│   ├── hooks/               # Automation hooks
│   └── skills/              # Domain knowledge skills
├── .moai/                   # MoAI-ADK project configuration
│   ├── config/              # Project settings
│   ├── project/             # Project documentation (this file)
│   └── specs/               # Feature specifications
├── src/                     # Source code (TBD)
│   ├── __init__.py
│   ├── cli.py               # Command-line interface
│   ├── converter.py         # Core conversion logic
│   ├── extractors/          # PDF content extractors
│   │   ├── text.py
│   │   ├── images.py
│   │   └── tables.py
│   ├── formatters/          # Markdown formatters
│   │   ├── headings.py
│   │   ├── lists.py
│   │   └── code.py
│   └── utils/               # Utility functions
├── tests/                   # Test suite (TBD)
│   ├── __init__.py
│   ├── test_converter.py
│   ├── test_extractors/
│   └── fixtures/            # Sample PDFs for testing
├── docs/                    # User documentation (TBD)
├── pyproject.toml           # Project configuration (TBD)
├── README.md                # Project readme
└── LICENSE                  # License file
```

---

## Module Descriptions

### Core Modules

| Module | Purpose | Status |
|--------|---------|--------|
| `src/converter.py` | Main conversion orchestration | Planned |
| `src/cli.py` | Command-line interface | Planned |
| `src/extractors/` | PDF content extraction | Planned |
| `src/formatters/` | Markdown output formatting | Planned |

### Supporting Modules

| Module | Purpose | Status |
|--------|---------|--------|
| `src/utils/` | Common utility functions | Planned |
| `tests/` | Test suite | Planned |
| `docs/` | User documentation | Planned |

---

## Architecture Pattern

<!-- TODO: Define your architectural approach -->

**Proposed Pattern:** Pipeline Architecture

```
PDF Input → Extraction → Processing → Formatting → Markdown Output
```

### Pipeline Stages

1. **Extraction:** Parse PDF and extract raw content
2. **Processing:** Analyze structure (headings, lists, tables)
3. **Formatting:** Convert to Markdown syntax
4. **Output:** Write formatted Markdown file

---

## Key Files

<!-- TODO: Update as key files are created -->

| File | Description |
|------|-------------|
| `src/converter.py` | Entry point for conversion logic |
| `src/cli.py` | CLI argument parsing and execution |
| `pyproject.toml` | Dependencies and project metadata |
| `README.md` | User-facing documentation |

---

## Configuration Files

| File | Purpose |
|------|---------|
| `.moai/config/sections/language.yaml` | Language settings |
| `.moai/config/sections/user.yaml` | User preferences |
| `pyproject.toml` | Python project configuration |

---

## Project Status

**Structure Status:** Template (pre-development)

**Last Updated:** 2026-01-22
