"""Tests for structure detection from PDF documents.

TDD RED Phase: These tests define the expected behavior of the structure extractor.
"""

from pathlib import Path

from pdf2md.extractors.structure import (
    ElementType,
    StructuredElement,
    StructureExtractor,
)
from pdf2md.extractors.text import TextExtractor


class TestStructureExtractor:
    """Tests for StructureExtractor class."""

    def test_detects_heading_by_large_font_size(self, pdf_with_headings: Path) -> None:
        """Should detect headings based on larger font sizes."""
        text_extractor = TextExtractor(pdf_with_headings)
        pages = text_extractor.extract()

        structure_extractor = StructureExtractor(pages)
        result = structure_extractor.extract()

        # Should have one page of results
        assert len(result) == 1

        # Find the title (largest font - should be H1)
        headings = [
            elem
            for elem in result[0]
            if elem.element_type in (ElementType.HEADING1, ElementType.HEADING2)
        ]
        assert len(headings) >= 1

        # "Document Title" should be detected as a heading
        title_found = any("Document Title" in elem.text for elem in headings)
        assert title_found, "Document Title should be detected as a heading"

    def test_detects_multiple_heading_levels(self, pdf_with_headings: Path) -> None:
        """Should detect different heading levels based on font size ratios."""
        text_extractor = TextExtractor(pdf_with_headings)
        pages = text_extractor.extract()

        structure_extractor = StructureExtractor(pages)
        result = structure_extractor.extract()

        # Get all heading types
        heading_types = {elem.element_type for elem in result[0]}

        # Should have at least 2 different heading levels
        heading_element_types = {
            ElementType.HEADING1,
            ElementType.HEADING2,
            ElementType.HEADING3,
            ElementType.HEADING4,
            ElementType.HEADING5,
            ElementType.HEADING6,
        }
        detected_headings = heading_types & heading_element_types
        assert len(detected_headings) >= 2, "Should detect multiple heading levels"

    def test_detects_paragraph_text(self, pdf_with_headings: Path) -> None:
        """Should detect regular text as paragraphs."""
        text_extractor = TextExtractor(pdf_with_headings)
        pages = text_extractor.extract()

        structure_extractor = StructureExtractor(pages)
        result = structure_extractor.extract()

        # Find paragraphs
        paragraphs = [
            elem for elem in result[0] if elem.element_type == ElementType.PARAGRAPH
        ]
        assert len(paragraphs) >= 1

        # Regular text should be detected as paragraph
        para_found = any("paragraph" in elem.text.lower() for elem in paragraphs)
        assert para_found, "Paragraph text should be detected"

    def test_detects_bullet_list_items(self, pdf_with_lists: Path) -> None:
        """Should detect bullet list items (-, *, +)."""
        text_extractor = TextExtractor(pdf_with_lists)
        pages = text_extractor.extract()

        structure_extractor = StructureExtractor(pages)
        result = structure_extractor.extract()

        # Find bullet list items
        bullets = [
            elem
            for elem in result[0]
            if elem.element_type == ElementType.BULLET_LIST_ITEM
        ]
        assert len(bullets) >= 3, "Should detect at least 3 bullet items"

        # Verify bullet item content (without the bullet marker)
        first_items_text = " ".join(b.text for b in bullets[:3])
        assert "First" in first_items_text or "item" in first_items_text.lower()

    def test_detects_numbered_list_items(self, pdf_with_lists: Path) -> None:
        """Should detect numbered list items (1., 2., etc.)."""
        text_extractor = TextExtractor(pdf_with_lists)
        pages = text_extractor.extract()

        structure_extractor = StructureExtractor(pages)
        result = structure_extractor.extract()

        # Find numbered list items
        numbered = [
            elem
            for elem in result[0]
            if elem.element_type == ElementType.NUMBERED_LIST_ITEM
        ]
        assert len(numbered) >= 3, "Should detect at least 3 numbered items"

    def test_preserves_text_content(self, sample_pdf: Path) -> None:
        """Should preserve the original text content."""
        text_extractor = TextExtractor(sample_pdf)
        pages = text_extractor.extract()

        structure_extractor = StructureExtractor(pages)
        result = structure_extractor.extract()

        # All text should be preserved
        all_text = " ".join(elem.text for elem in result[0])
        assert "Hello" in all_text
        assert "World" in all_text

    def test_handles_empty_page(self, empty_pdf: Path) -> None:
        """Should handle empty pages gracefully."""
        text_extractor = TextExtractor(empty_pdf)
        pages = text_extractor.extract()

        structure_extractor = StructureExtractor(pages)
        result = structure_extractor.extract()

        # Should return an empty list for the page
        assert len(result) == 1
        assert len(result[0]) == 0 or all(
            elem.text.strip() == "" for elem in result[0]
        )

    def test_handles_multi_page_document(self, multi_page_pdf: Path) -> None:
        """Should process all pages of a multi-page document."""
        text_extractor = TextExtractor(multi_page_pdf)
        pages = text_extractor.extract()

        structure_extractor = StructureExtractor(pages)
        result = structure_extractor.extract()

        # Should have 3 pages of results
        assert len(result) == 3


class TestStructuredElement:
    """Tests for StructuredElement data class."""

    def test_structured_element_has_type(self) -> None:
        """StructuredElement should have element_type attribute."""
        element = StructuredElement(
            element_type=ElementType.PARAGRAPH,
            text="Test text",
        )
        assert element.element_type == ElementType.PARAGRAPH

    def test_structured_element_has_text(self) -> None:
        """StructuredElement should have text attribute."""
        element = StructuredElement(
            element_type=ElementType.PARAGRAPH,
            text="Test text",
        )
        assert element.text == "Test text"

    def test_structured_element_has_level(self) -> None:
        """StructuredElement should have level attribute."""
        element = StructuredElement(
            element_type=ElementType.HEADING1,
            text="Title",
            level=1,
        )
        assert element.level == 1


class TestElementType:
    """Tests for ElementType enum."""

    def test_heading_types_exist(self) -> None:
        """Should have heading types 1-6."""
        assert ElementType.HEADING1.value == "heading1"
        assert ElementType.HEADING2.value == "heading2"
        assert ElementType.HEADING3.value == "heading3"
        assert ElementType.HEADING4.value == "heading4"
        assert ElementType.HEADING5.value == "heading5"
        assert ElementType.HEADING6.value == "heading6"

    def test_paragraph_type_exists(self) -> None:
        """Should have paragraph type."""
        assert ElementType.PARAGRAPH.value == "paragraph"

    def test_list_types_exist(self) -> None:
        """Should have bullet and numbered list item types."""
        assert ElementType.BULLET_LIST_ITEM.value == "bullet_list_item"
        assert ElementType.NUMBERED_LIST_ITEM.value == "numbered_list_item"
