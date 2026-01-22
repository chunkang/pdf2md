# SPEC-PDF2MD-001: Implementation Plan

## TAG Reference

- **SPEC ID**: SPEC-PDF2MD-001
- **Title**: PDF to Markdown Converter MVP
- **Phase**: Implementation Planning

---

## Overview

This plan outlines the implementation strategy for the PDF to Markdown converter MVP, following Test-Driven Development (TDD) methodology with the RED-GREEN-REFACTOR cycle.

---

## Priority-Based Milestones

### Primary Goal: Core Text Extraction

**Objective**: Establish the foundation with PDF parsing and basic text extraction.

**Deliverables**:
- Project structure with pyproject.toml
- pymupdf integration for PDF reading
- Basic text extraction from PDF pages
- Unit tests for text extraction

**Tasks**:
| Task ID | Description | Dependencies | Complexity |
|---------|-------------|--------------|------------|
| T-001 | Create project structure with src/ and tests/ directories | None | Low |
| T-002 | Configure pyproject.toml with dependencies | T-001 | Low |
| T-003 | Implement PDF validation module (utils/validation.py) | T-002 | Medium |
| T-004 | Implement text extractor (extractors/text.py) | T-003 | Medium |
| T-005 | Write unit tests for text extraction | T-004 | Medium |

**Success Criteria**:
- Text extracted from sample PDF matches expected content
- All validation error cases handled with appropriate exit codes
- Test coverage >= 85% for extraction module

---

### Secondary Goal: Structure Detection

**Objective**: Implement heading and list detection based on text analysis.

**Deliverables**:
- Heading detection based on font size ratios
- List pattern recognition (bullets, numbers)
- Structure detection unit tests

**Tasks**:
| Task ID | Description | Dependencies | Complexity |
|---------|-------------|--------------|------------|
| T-006 | Implement heading detector (extractors/structure.py) | T-004 | High |
| T-007 | Implement list pattern detector | T-006 | Medium |
| T-008 | Write unit tests for structure detection | T-007 | Medium |
| T-009 | Integration test: extraction + structure | T-008 | Medium |

**Success Criteria**:
- Headings correctly identified by font size analysis
- Bullet and numbered lists detected with 90%+ accuracy
- Integration tests pass for sample documents

---

### Tertiary Goal: Markdown Formatting

**Objective**: Convert extracted structure to valid Markdown syntax.

**Deliverables**:
- Heading level conversion (h1-h6)
- List formatting (unordered and ordered)
- Paragraph preservation
- Markdown formatter unit tests

**Tasks**:
| Task ID | Description | Dependencies | Complexity |
|---------|-------------|--------------|------------|
| T-010 | Implement Markdown formatter (formatters/markdown.py) | T-009 | Medium |
| T-011 | Implement heading level mapping | T-010 | Low |
| T-012 | Implement list syntax generation | T-010 | Low |
| T-013 | Write unit tests for formatter | T-012 | Medium |

**Success Criteria**:
- Output is valid Markdown syntax
- Heading levels correctly mapped (h1-h6)
- Lists render correctly in Markdown viewers

---

### Final Goal: CLI Interface

**Objective**: Create user-facing CLI with typer framework.

**Deliverables**:
- CLI application with typer
- Input/output path handling
- Progress display with rich
- Error handling with exit codes
- End-to-end integration tests

**Tasks**:
| Task ID | Description | Dependencies | Complexity |
|---------|-------------|--------------|------------|
| T-014 | Implement CLI structure (cli.py) | T-013 | Medium |
| T-015 | Implement argument parsing (input, output, flags) | T-014 | Low |
| T-016 | Implement conversion orchestrator (converter.py) | T-015 | Medium |
| T-017 | Implement progress display with rich | T-016 | Low |
| T-018 | Implement error handling and exit codes | T-017 | Medium |
| T-019 | Write end-to-end CLI tests | T-018 | High |
| T-020 | Documentation and README update | T-019 | Low |

**Success Criteria**:
- CLI accepts PDF input and produces Markdown output
- All exit codes function as specified
- Help text accurately describes all options
- End-to-end tests pass for all major scenarios

---

## Technical Approach

### Architecture Pattern: Pipeline

The implementation follows a pipeline architecture:

```
[Input Validation] -> [Text Extraction] -> [Structure Detection] -> [Markdown Formatting] -> [File Output]
```

Each stage is isolated and testable independently.

### TDD Cycle per Module

1. **RED**: Write failing tests for the module
2. **GREEN**: Implement minimum code to pass tests
3. **REFACTOR**: Optimize and clean up implementation

### Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| pymupdf over pdfplumber | Faster performance, better text extraction |
| typer over click | Modern type hints, automatic help |
| Pipeline pattern | Testability, separation of concerns |
| Exit codes for errors | CLI best practices, scriptability |

---

## Risk Assessment

### Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Font size detection unreliable | Medium | High | Implement heuristic fallbacks |
| Complex PDF layouts break extraction | Medium | Medium | Focus on text-heavy PDFs for MVP |
| pymupdf API changes | Low | High | Pin version, monitor releases |

### Schedule Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Heading detection more complex than expected | Medium | Medium | Reduce initial heading level support |
| Test fixture creation time | Medium | Low | Use existing sample PDFs |

---

## Quality Gates

### Per-Milestone Gates

- [ ] All unit tests pass
- [ ] Test coverage >= 85%
- [ ] No ruff linting errors
- [ ] mypy type check passes
- [ ] Documentation updated

### Final Release Gates

- [ ] End-to-end tests pass
- [ ] Performance benchmarks met (<5s/page)
- [ ] README complete with examples
- [ ] All exit codes documented
- [ ] pyproject.toml version updated

---

## Agent Delegation Plan

| Task Group | Recommended Agent | Rationale |
|------------|-------------------|-----------|
| Project setup (T-001, T-002) | expert-backend | Python project configuration |
| Core extraction (T-003 to T-009) | expert-backend | Python implementation |
| Formatter (T-010 to T-013) | expert-backend | String processing |
| CLI (T-014 to T-018) | expert-backend | typer CLI patterns |
| Testing (all test tasks) | expert-testing | TDD expertise |
| Documentation (T-020) | manager-docs | Documentation standards |

---

## Dependencies and Blockers

### Prerequisites

- [ ] Python 3.11+ available
- [ ] Virtual environment created
- [ ] Sample PDF test fixtures available

### External Dependencies

- pymupdf installation (requires compilation on some platforms)
- No network dependencies for core functionality

---

## Implementation Notes

### Heading Detection Strategy

1. Extract text with font size metadata from pymupdf
2. Calculate font size distribution across document
3. Identify distinct font size clusters
4. Map largest sizes to h1, progressively smaller to h2-h6
5. Apply minimum size threshold to avoid false positives

### List Detection Strategy

1. Identify lines starting with bullet characters (-, *, +)
2. Identify lines starting with numbers followed by . or )
3. Detect indentation levels for nested lists
4. Group consecutive list items

### Error Handling Strategy

1. Validate input file existence and extension
2. Attempt PDF open with pymupdf
3. Check for password protection
4. Check for extractable text content
5. Handle each error with specific exit code and message

---

## Traceability

| Milestone | Requirements Covered |
|-----------|---------------------|
| Primary Goal | REQ-U-001, REQ-S-001, REQ-S-002, REQ-S-004 |
| Secondary Goal | REQ-E-004, REQ-E-005 |
| Tertiary Goal | REQ-U-002, REQ-O-001 |
| Final Goal | REQ-E-001, REQ-E-002, REQ-E-003, REQ-E-006, REQ-S-003, REQ-N-001, REQ-N-002, REQ-N-003 |

---

## Next Steps

After SPEC approval:
1. Run `/moai:2-run SPEC-PDF2MD-001` to begin TDD implementation
2. expert-backend implements core modules
3. expert-testing validates test coverage
4. manager-quality performs final validation
