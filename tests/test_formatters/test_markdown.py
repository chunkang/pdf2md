"""Tests for Markdown formatting of structured content.

TDD RED Phase: These tests define the expected behavior of the markdown formatter.
"""


from pdf2md.extractors.structure import ElementType, StructuredElement
from pdf2md.formatters.markdown import MarkdownFormatter


class TestMarkdownFormatter:
    """Tests for MarkdownFormatter class."""

    def test_format_heading1(self) -> None:
        """Should format H1 with single # prefix."""
        elements = [
            [
                StructuredElement(
                    element_type=ElementType.HEADING1,
                    text="Main Title",
                    level=1,
                )
            ]
        ]
        formatter = MarkdownFormatter(elements)
        result = formatter.format()

        assert "# Main Title" in result
        assert "## Main Title" not in result

    def test_format_heading2(self) -> None:
        """Should format H2 with ## prefix."""
        elements = [
            [
                StructuredElement(
                    element_type=ElementType.HEADING2,
                    text="Subtitle",
                    level=2,
                )
            ]
        ]
        formatter = MarkdownFormatter(elements)
        result = formatter.format()

        assert "## Subtitle" in result

    def test_format_all_heading_levels(self) -> None:
        """Should format all heading levels correctly."""
        elements = [
            [
                StructuredElement(ElementType.HEADING1, "H1", 1),
                StructuredElement(ElementType.HEADING2, "H2", 2),
                StructuredElement(ElementType.HEADING3, "H3", 3),
                StructuredElement(ElementType.HEADING4, "H4", 4),
                StructuredElement(ElementType.HEADING5, "H5", 5),
                StructuredElement(ElementType.HEADING6, "H6", 6),
            ]
        ]
        formatter = MarkdownFormatter(elements)
        result = formatter.format()

        assert "# H1" in result
        assert "## H2" in result
        assert "### H3" in result
        assert "#### H4" in result
        assert "##### H5" in result
        assert "###### H6" in result

    def test_format_paragraph(self) -> None:
        """Should format paragraph without prefix."""
        elements = [
            [
                StructuredElement(
                    element_type=ElementType.PARAGRAPH,
                    text="This is a regular paragraph.",
                    level=0,
                )
            ]
        ]
        formatter = MarkdownFormatter(elements)
        result = formatter.format()

        assert "This is a regular paragraph." in result
        assert "#" not in result

    def test_format_bullet_list(self) -> None:
        """Should format bullet list items with - prefix."""
        elements = [
            [
                StructuredElement(
                    element_type=ElementType.BULLET_LIST_ITEM,
                    text="First item",
                    level=1,
                ),
                StructuredElement(
                    element_type=ElementType.BULLET_LIST_ITEM,
                    text="Second item",
                    level=1,
                ),
                StructuredElement(
                    element_type=ElementType.BULLET_LIST_ITEM,
                    text="Third item",
                    level=1,
                ),
            ]
        ]
        formatter = MarkdownFormatter(elements)
        result = formatter.format()

        assert "- First item" in result
        assert "- Second item" in result
        assert "- Third item" in result

    def test_format_numbered_list(self) -> None:
        """Should format numbered list items with sequential numbers."""
        elements = [
            [
                StructuredElement(
                    element_type=ElementType.NUMBERED_LIST_ITEM,
                    text="First step",
                    level=1,
                ),
                StructuredElement(
                    element_type=ElementType.NUMBERED_LIST_ITEM,
                    text="Second step",
                    level=1,
                ),
                StructuredElement(
                    element_type=ElementType.NUMBERED_LIST_ITEM,
                    text="Third step",
                    level=1,
                ),
            ]
        ]
        formatter = MarkdownFormatter(elements)
        result = formatter.format()

        assert "1. First step" in result
        assert "2. Second step" in result
        assert "3. Third step" in result

    def test_format_mixed_content(self) -> None:
        """Should correctly format mixed content types."""
        elements = [
            [
                StructuredElement(ElementType.HEADING1, "Document Title", 1),
                StructuredElement(ElementType.PARAGRAPH, "Introduction paragraph.", 0),
                StructuredElement(ElementType.HEADING2, "Section 1", 2),
                StructuredElement(ElementType.BULLET_LIST_ITEM, "Point A", 1),
                StructuredElement(ElementType.BULLET_LIST_ITEM, "Point B", 1),
                StructuredElement(ElementType.PARAGRAPH, "Conclusion text.", 0),
            ]
        ]
        formatter = MarkdownFormatter(elements)
        result = formatter.format()

        assert "# Document Title" in result
        assert "Introduction paragraph." in result
        assert "## Section 1" in result
        assert "- Point A" in result
        assert "- Point B" in result
        assert "Conclusion text." in result

    def test_format_multi_page_document(self) -> None:
        """Should format multi-page documents with page separators."""
        elements = [
            [StructuredElement(ElementType.PARAGRAPH, "Page 1 content", 0)],
            [StructuredElement(ElementType.PARAGRAPH, "Page 2 content", 0)],
            [StructuredElement(ElementType.PARAGRAPH, "Page 3 content", 0)],
        ]
        formatter = MarkdownFormatter(elements)
        result = formatter.format()

        assert "Page 1 content" in result
        assert "Page 2 content" in result
        assert "Page 3 content" in result

    def test_format_empty_page(self) -> None:
        """Should handle empty pages gracefully."""
        elements = [[]]
        formatter = MarkdownFormatter(elements)
        result = formatter.format()

        # Should return empty or whitespace-only string
        assert result.strip() == ""

    def test_format_preserves_text_content(self) -> None:
        """Should preserve original text content."""
        original_text = "Special characters: <>&\"'"
        elements = [
            [StructuredElement(ElementType.PARAGRAPH, original_text, 0)]
        ]
        formatter = MarkdownFormatter(elements)
        result = formatter.format()

        assert original_text in result

    def test_format_adds_blank_lines_between_sections(self) -> None:
        """Should add appropriate spacing between sections."""
        elements = [
            [
                StructuredElement(ElementType.HEADING1, "Title", 1),
                StructuredElement(ElementType.PARAGRAPH, "Para 1", 0),
                StructuredElement(ElementType.HEADING2, "Section", 2),
                StructuredElement(ElementType.PARAGRAPH, "Para 2", 0),
            ]
        ]
        formatter = MarkdownFormatter(elements)
        result = formatter.format()

        # Should have blank lines between different element types
        lines = result.split("\n")
        # Check that there's proper spacing (implementation-specific)
        assert len(lines) >= 4

    def test_numbered_list_resets_after_other_element(self) -> None:
        """Numbered list counter should reset after a non-list element."""
        elements = [
            [
                StructuredElement(ElementType.NUMBERED_LIST_ITEM, "Item 1", 1),
                StructuredElement(ElementType.NUMBERED_LIST_ITEM, "Item 2", 1),
                StructuredElement(ElementType.PARAGRAPH, "Break", 0),
                StructuredElement(ElementType.NUMBERED_LIST_ITEM, "New Item 1", 1),
                StructuredElement(ElementType.NUMBERED_LIST_ITEM, "New Item 2", 1),
            ]
        ]
        formatter = MarkdownFormatter(elements)
        result = formatter.format()

        # First list should have 1., 2.
        # Second list should restart at 1.
        lines = [line.strip() for line in result.split("\n") if line.strip()]
        numbered_lines = [line for line in lines if line[0].isdigit()]
        assert len(numbered_lines) >= 4
        # Verify the second list starts at 1 again
        assert numbered_lines[2].startswith("1.")


class TestMarkdownFormatterEdgeCases:
    """Edge case tests for MarkdownFormatter."""

    def test_format_very_long_text(self) -> None:
        """Should handle very long text content."""
        long_text = "A" * 10000
        elements = [[StructuredElement(ElementType.PARAGRAPH, long_text, 0)]]
        formatter = MarkdownFormatter(elements)
        result = formatter.format()

        assert long_text in result

    def test_format_text_with_newlines(self) -> None:
        """Should handle text that already contains newlines."""
        text_with_newlines = "Line 1\nLine 2\nLine 3"
        elements = [[StructuredElement(ElementType.PARAGRAPH, text_with_newlines, 0)]]
        formatter = MarkdownFormatter(elements)
        result = formatter.format()

        # Text should be preserved
        assert "Line 1" in result

    def test_format_unicode_content(self) -> None:
        """Should handle Unicode content correctly."""
        unicode_text = "Unicode: \u00e9\u00e8\u00ea \u4e2d\u6587 \ud55c\uad6d\uc5b4"
        elements = [[StructuredElement(ElementType.PARAGRAPH, unicode_text, 0)]]
        formatter = MarkdownFormatter(elements)
        result = formatter.format()

        assert unicode_text in result
