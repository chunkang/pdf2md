"""Pytest configuration and fixtures for pdf2md tests."""

import tempfile
from collections.abc import Generator
from pathlib import Path

import fitz  # pymupdf
import pytest


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_pdf(temp_dir: Path) -> Path:
    """Create a simple PDF file for testing."""
    pdf_path = temp_dir / "sample.pdf"
    doc = fitz.open()

    # Add a page with some text
    page = doc.new_page()
    text_point = fitz.Point(72, 72)
    page.insert_text(text_point, "Hello, World!", fontsize=12)
    page.insert_text(fitz.Point(72, 100), "This is a test PDF document.", fontsize=12)

    doc.save(str(pdf_path))
    doc.close()
    return pdf_path


@pytest.fixture
def multi_page_pdf(temp_dir: Path) -> Path:
    """Create a multi-page PDF file for testing."""
    pdf_path = temp_dir / "multi_page.pdf"
    doc = fitz.open()

    for i in range(3):
        page = doc.new_page()
        page.insert_text(fitz.Point(72, 72), f"Page {i + 1} content", fontsize=12)
        page.insert_text(fitz.Point(72, 100), f"More text on page {i + 1}.", fontsize=12)

    doc.save(str(pdf_path))
    doc.close()
    return pdf_path


@pytest.fixture
def pdf_with_headings(temp_dir: Path) -> Path:
    """Create a PDF with different font sizes for heading detection."""
    pdf_path = temp_dir / "headings.pdf"
    doc = fitz.open()
    page = doc.new_page()

    # Title - largest font
    page.insert_text(fitz.Point(72, 72), "Document Title", fontsize=24)

    # Heading 1
    page.insert_text(fitz.Point(72, 120), "Chapter One", fontsize=18)

    # Regular paragraph
    page.insert_text(fitz.Point(72, 150), "This is regular paragraph text.", fontsize=12)

    # Heading 2
    page.insert_text(fitz.Point(72, 180), "Section 1.1", fontsize=14)

    # More paragraph text
    page.insert_text(fitz.Point(72, 210), "Another paragraph here.", fontsize=12)

    doc.save(str(pdf_path))
    doc.close()
    return pdf_path


@pytest.fixture
def pdf_with_lists(temp_dir: Path) -> Path:
    """Create a PDF with bullet and numbered lists."""
    pdf_path = temp_dir / "lists.pdf"
    doc = fitz.open()
    page = doc.new_page()

    y_pos = 72

    # Regular text
    page.insert_text(fitz.Point(72, y_pos), "Here is a bullet list:", fontsize=12)
    y_pos += 20

    # Bullet list
    bullets = ["- First item", "- Second item", "- Third item"]
    for bullet in bullets:
        page.insert_text(fitz.Point(72, y_pos), bullet, fontsize=12)
        y_pos += 18

    y_pos += 10
    page.insert_text(fitz.Point(72, y_pos), "Here is a numbered list:", fontsize=12)
    y_pos += 20

    # Numbered list
    numbers = ["1. First numbered item", "2. Second numbered item", "3. Third numbered item"]
    for num in numbers:
        page.insert_text(fitz.Point(72, y_pos), num, fontsize=12)
        y_pos += 18

    doc.save(str(pdf_path))
    doc.close()
    return pdf_path


@pytest.fixture
def password_protected_pdf(temp_dir: Path) -> Path:
    """Create a password-protected PDF file."""
    pdf_path = temp_dir / "protected.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text(fitz.Point(72, 72), "Secret content", fontsize=12)

    # Save with encryption
    doc.save(
        str(pdf_path),
        encryption=fitz.PDF_ENCRYPT_AES_256,
        user_pw="user123",
        owner_pw="owner456",
    )
    doc.close()
    return pdf_path


@pytest.fixture
def empty_pdf(temp_dir: Path) -> Path:
    """Create an empty PDF file (no pages)."""
    pdf_path = temp_dir / "empty.pdf"
    doc = fitz.open()
    doc.new_page()  # Add one blank page
    doc.save(str(pdf_path))
    doc.close()
    return pdf_path


@pytest.fixture
def non_pdf_file(temp_dir: Path) -> Path:
    """Create a non-PDF file with .pdf extension."""
    pdf_path = temp_dir / "not_a_pdf.pdf"
    pdf_path.write_text("This is not a PDF file, just plain text.")
    return pdf_path


@pytest.fixture
def text_file(temp_dir: Path) -> Path:
    """Create a plain text file."""
    txt_path = temp_dir / "document.txt"
    txt_path.write_text("This is a text file, not a PDF.")
    return txt_path
