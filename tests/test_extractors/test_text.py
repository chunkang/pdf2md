"""Tests for text extraction from PDF documents.

TDD RED Phase: These tests define the expected behavior of the text extractor.
"""

from pathlib import Path

from pdf2md.extractors.text import PageContent, TextExtractor


class TestTextExtractor:
    """Tests for TextExtractor class."""

    def test_extract_text_from_single_page_pdf(self, sample_pdf: Path) -> None:
        """Should extract text from a single-page PDF."""
        extractor = TextExtractor(sample_pdf)
        pages = extractor.extract()

        assert len(pages) == 1
        assert isinstance(pages[0], PageContent)
        assert "Hello" in pages[0].text
        assert "World" in pages[0].text

    def test_extract_text_from_multi_page_pdf(self, multi_page_pdf: Path) -> None:
        """Should extract text from all pages of a multi-page PDF."""
        extractor = TextExtractor(multi_page_pdf)
        pages = extractor.extract()

        assert len(pages) == 3
        for i, page in enumerate(pages):
            assert f"Page {i + 1}" in page.text
            assert page.page_number == i + 1

    def test_page_content_has_page_number(self, sample_pdf: Path) -> None:
        """PageContent should include the page number (1-indexed)."""
        extractor = TextExtractor(sample_pdf)
        pages = extractor.extract()

        assert pages[0].page_number == 1

    def test_page_content_has_text_blocks(self, sample_pdf: Path) -> None:
        """PageContent should include text blocks with position info."""
        extractor = TextExtractor(sample_pdf)
        pages = extractor.extract()

        assert len(pages[0].blocks) > 0
        # Each block should have text and position info
        for block in pages[0].blocks:
            assert hasattr(block, "text")
            assert hasattr(block, "bbox")

    def test_empty_pdf_returns_empty_page(self, empty_pdf: Path) -> None:
        """An empty PDF page should return PageContent with empty or minimal text."""
        extractor = TextExtractor(empty_pdf)
        pages = extractor.extract()

        assert len(pages) == 1
        # Empty page should have empty or whitespace-only text
        assert pages[0].text.strip() == ""

    def test_extractor_accepts_string_path(self, sample_pdf: Path) -> None:
        """TextExtractor should accept string paths."""
        extractor = TextExtractor(str(sample_pdf))
        pages = extractor.extract()

        assert len(pages) >= 1

    def test_extractor_accepts_pathlib_path(self, sample_pdf: Path) -> None:
        """TextExtractor should accept pathlib.Path objects."""
        extractor = TextExtractor(sample_pdf)
        pages = extractor.extract()

        assert len(pages) >= 1

    def test_extract_preserves_text_order(self, multi_page_pdf: Path) -> None:
        """Text extraction should preserve reading order."""
        extractor = TextExtractor(multi_page_pdf)
        pages = extractor.extract()

        # Each page should have content appearing in reading order
        for page in pages:
            # "Page X content" should appear before "More text"
            content_idx = page.text.find("content")
            more_idx = page.text.find("More")
            assert content_idx < more_idx


class TestPageContent:
    """Tests for PageContent data class."""

    def test_page_content_text_property(self, sample_pdf: Path) -> None:
        """PageContent.text should return combined text from all blocks."""
        extractor = TextExtractor(sample_pdf)
        pages = extractor.extract()

        assert isinstance(pages[0].text, str)
        assert len(pages[0].text) > 0

    def test_page_content_blocks_property(self, sample_pdf: Path) -> None:
        """PageContent.blocks should return list of TextBlock objects."""
        extractor = TextExtractor(sample_pdf)
        pages = extractor.extract()

        assert isinstance(pages[0].blocks, list)


class TestTextBlock:
    """Tests for TextBlock data class."""

    def test_text_block_has_bbox(self, sample_pdf: Path) -> None:
        """TextBlock should have bounding box coordinates."""
        extractor = TextExtractor(sample_pdf)
        pages = extractor.extract()

        if pages[0].blocks:
            block = pages[0].blocks[0]
            # bbox should be (x0, y0, x1, y1)
            assert len(block.bbox) == 4
            assert all(isinstance(coord, (int, float)) for coord in block.bbox)

    def test_text_block_has_font_info(self, pdf_with_headings: Path) -> None:
        """TextBlock should have font size information for structure detection."""
        extractor = TextExtractor(pdf_with_headings)
        pages = extractor.extract()

        # At least some blocks should have font_size
        has_font_size = any(
            hasattr(block, "font_size") and block.font_size is not None
            for block in pages[0].blocks
        )
        assert has_font_size
