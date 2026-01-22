# SPEC-PDF2MD-001: Acceptance Criteria

## TAG Reference

- **SPEC ID**: SPEC-PDF2MD-001
- **Title**: PDF to Markdown Converter MVP
- **Phase**: Acceptance Testing

---

## Test Scenarios

### Scenario 1: Basic PDF Conversion

**Feature**: Convert a simple text PDF to Markdown

```gherkin
Given a valid PDF file "sample.pdf" containing plain text
When the user runs "pdf2md sample.pdf"
Then the system shall create "sample.md" in the same directory
And the Markdown file shall contain all text from the PDF
And the text fidelity shall be 95% or higher
And the exit code shall be 0
```

**Test Data**:
- Input: sample.pdf with known text content
- Expected: sample.md with matching text

---

### Scenario 2: Custom Output Path

**Feature**: Specify custom output file path

```gherkin
Given a valid PDF file "input.pdf"
When the user runs "pdf2md input.pdf output/result.md"
Then the system shall create "result.md" in the "output" directory
And the exit code shall be 0
```

**Test Data**:
- Input: input.pdf
- Output path: output/result.md

---

### Scenario 3: Heading Detection

**Feature**: Detect and convert headings based on font size

```gherkin
Given a PDF file with text at font sizes 24pt, 18pt, 14pt, and 12pt
When the user runs "pdf2md document.pdf"
Then the 24pt text shall be converted to "# Heading 1"
And the 18pt text shall be converted to "## Heading 2"
And the 14pt text shall be converted to "### Heading 3"
And the 12pt text shall be body text without heading markup
```

**Test Data**:
- PDF with multiple font sizes
- Expected Markdown with appropriate heading levels

---

### Scenario 4: List Detection

**Feature**: Detect and convert bullet and numbered lists

```gherkin
Given a PDF file containing:
  - Lines starting with "- " (bullet items)
  - Lines starting with "1. " (numbered items)
When the user runs "pdf2md list-document.pdf"
Then bullet items shall be converted to "- item" Markdown syntax
And numbered items shall be converted to "1. item" Markdown syntax
```

**Test Data**:
- PDF with bullet list
- PDF with numbered list
- PDF with mixed lists

---

### Scenario 5: File Not Found Error

**Feature**: Handle missing input file gracefully

```gherkin
Given no file exists at path "nonexistent.pdf"
When the user runs "pdf2md nonexistent.pdf"
Then the system shall display error message "Error: File 'nonexistent.pdf' not found"
And the exit code shall be 1
And no output file shall be created
```

---

### Scenario 6: Invalid PDF File

**Feature**: Handle non-PDF input gracefully

```gherkin
Given a text file "fake.pdf" that is not a valid PDF
When the user runs "pdf2md fake.pdf"
Then the system shall display error message "Error: 'fake.pdf' is not a valid PDF file"
And the exit code shall be 2
And no output file shall be created
```

---

### Scenario 7: Password-Protected PDF

**Feature**: Handle encrypted PDFs gracefully

```gherkin
Given a password-protected PDF file "protected.pdf"
When the user runs "pdf2md protected.pdf"
Then the system shall display error message "Error: 'protected.pdf' is password-protected"
And the system shall suggest "Remove password protection and try again"
And the exit code shall be 3
```

---

### Scenario 8: Overwrite Confirmation

**Feature**: Prevent accidental file overwrite

```gherkin
Given a valid PDF file "document.pdf"
And a file "document.md" already exists
When the user runs "pdf2md document.pdf"
Then the system shall prompt "Output file 'document.md' exists. Overwrite? [y/N]"
And if user enters "n" then no file shall be modified and exit code shall be 0
And if user enters "y" then the file shall be overwritten
```

---

### Scenario 9: Force Overwrite Flag

**Feature**: Skip overwrite confirmation with --force flag

```gherkin
Given a valid PDF file "document.pdf"
And a file "document.md" already exists
When the user runs "pdf2md --force document.pdf"
Then the system shall overwrite "document.md" without prompting
And the exit code shall be 0
```

---

### Scenario 10: No Extractable Text Warning

**Feature**: Handle scanned PDFs without text layer

```gherkin
Given a scanned PDF file "scanned.pdf" with no text layer
When the user runs "pdf2md scanned.pdf"
Then the system shall display warning "Warning: No extractable text found in 'scanned.pdf'"
And the system shall suggest "This appears to be a scanned document. Consider using OCR."
And an empty Markdown file shall be created
And the exit code shall be 0
```

---

### Scenario 11: Verbose Mode

**Feature**: Display detailed progress in verbose mode

```gherkin
Given a valid PDF file "document.pdf" with 5 pages
When the user runs "pdf2md --verbose document.pdf"
Then the system shall display progress for each page
And the system shall display processing time
And the system shall display character count statistics
```

---

### Scenario 12: Quiet Mode

**Feature**: Suppress output in quiet mode

```gherkin
Given a valid PDF file "document.pdf"
When the user runs "pdf2md --quiet document.pdf"
Then the system shall produce no stdout output
And errors shall still be written to stderr
And the exit code shall be 0 on success
```

---

### Scenario 13: Help Display

**Feature**: Display usage help

```gherkin
Given the pdf2md application is installed
When the user runs "pdf2md --help"
Then the system shall display usage information
And the system shall list all available options
And the system shall show examples
```

---

### Scenario 14: Version Display

**Feature**: Display version information

```gherkin
Given the pdf2md application is installed
When the user runs "pdf2md --version"
Then the system shall display the current version number
And the version shall match pyproject.toml version
```

---

### Scenario 15: Original File Unchanged

**Feature**: Ensure PDF file is never modified

```gherkin
Given a valid PDF file "document.pdf" with known checksum
When the user runs "pdf2md document.pdf"
Then the checksum of "document.pdf" shall remain unchanged
And the file modification time shall remain unchanged
```

---

## Quality Gate Criteria

### Functional Criteria

| Criterion | Target | Validation Method |
|-----------|--------|-------------------|
| Text extraction accuracy | >= 95% | Character comparison test |
| Heading detection accuracy | >= 90% | Manual review of test documents |
| List detection accuracy | >= 90% | Pattern matching validation |
| Error handling coverage | 100% | All error paths tested |

### Non-Functional Criteria

| Criterion | Target | Validation Method |
|-----------|--------|-------------------|
| Processing speed | < 5s per page | Benchmark test suite |
| Memory usage | < 500MB for 100 pages | Memory profiling |
| Startup time | < 1s | CLI response time test |
| Exit code correctness | 100% | Exit code assertions |

### Code Quality Criteria

| Criterion | Target | Validation Method |
|-----------|--------|-------------------|
| Test coverage | >= 85% | pytest-cov report |
| Type coverage | >= 90% | mypy strict mode |
| Linting | 0 errors | ruff check |
| Documentation | All public APIs | docstring coverage |

---

## Test Fixtures Required

### Sample PDFs

| Fixture | Description | Purpose |
|---------|-------------|---------|
| simple_text.pdf | Plain text, single font | Basic extraction test |
| multi_heading.pdf | Multiple heading levels | Heading detection test |
| bullet_list.pdf | Unordered list items | List detection test |
| numbered_list.pdf | Ordered list items | List detection test |
| mixed_content.pdf | Headings, lists, paragraphs | Integration test |
| protected.pdf | Password-protected | Error handling test |
| scanned.pdf | Image-only, no text | Warning test |
| large_100pages.pdf | 100 pages of text | Performance test |
| unicode.pdf | Non-ASCII characters | Encoding test |
| empty.pdf | Valid PDF, no content | Edge case test |

---

## Definition of Done

### Feature Complete

- [x] All 15 acceptance scenarios pass
- [x] All exit codes implemented and tested (0-5)
- [x] CLI help text complete and accurate
- [x] Progress display functional with rich

### Quality Complete

- [x] Test coverage >= 85% (92.19% achieved)
- [x] mypy strict mode passes
- [x] ruff check passes with 0 errors (4 warnings)
- [x] All docstrings complete

### Documentation Complete

- [x] README.md with installation and usage
- [x] Examples for common use cases
- [x] Error message guide

### Release Ready

- [x] pyproject.toml version set (v0.1.0)
- [x] CHANGELOG entry added
- [x] All test fixtures included
- [ ] CI/CD pipeline passes (not configured)

---

## Traceability Matrix

| Acceptance Scenario | Requirement IDs | Test Priority |
|---------------------|-----------------|---------------|
| Scenario 1: Basic Conversion | REQ-E-001, REQ-U-001 | Critical |
| Scenario 2: Custom Output | REQ-E-002 | High |
| Scenario 3: Heading Detection | REQ-E-004 | Critical |
| Scenario 4: List Detection | REQ-E-005 | Critical |
| Scenario 5: File Not Found | REQ-S-001 | High |
| Scenario 6: Invalid PDF | REQ-S-002 | High |
| Scenario 7: Password Protected | REQ-S-004 | Medium |
| Scenario 8: Overwrite Confirm | REQ-S-003 | High |
| Scenario 9: Force Overwrite | REQ-S-003, REQ-N-003 | Medium |
| Scenario 10: No Text Warning | REQ-S-005 | Medium |
| Scenario 11: Verbose Mode | REQ-O-003 | Low |
| Scenario 12: Quiet Mode | REQ-O-003 | Low |
| Scenario 13: Help Display | REQ-E-001 | Medium |
| Scenario 14: Version Display | REQ-E-001 | Low |
| Scenario 15: File Unchanged | REQ-N-001 | Critical |
