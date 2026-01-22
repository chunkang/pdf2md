"""Text extraction from PDF documents using pymupdf.

This module provides utilities to extract text content from PDF files,
preserving position and font information for structure detection.
"""

from dataclasses import dataclass, field
from pathlib import Path

import fitz  # pymupdf


@dataclass
class TextBlock:
    """Represents a block of text extracted from a PDF page.

    Attributes:
        text: The text content of the block.
        bbox: Bounding box coordinates (x0, y0, x1, y1).
        font_size: The primary font size used in the block.
        font_name: The primary font name used in the block.
    """

    text: str
    bbox: tuple[float, float, float, float]
    font_size: float | None = None
    font_name: str | None = None


@dataclass
class PageContent:
    """Represents the extracted content from a single PDF page.

    Attributes:
        page_number: The 1-indexed page number.
        blocks: List of text blocks on the page.
        width: Page width in points.
        height: Page height in points.
    """

    page_number: int
    blocks: list[TextBlock] = field(default_factory=list)
    width: float = 0.0
    height: float = 0.0

    @property
    def text(self) -> str:
        """Return combined text from all blocks, preserving reading order."""
        return "\n".join(block.text for block in self.blocks if block.text.strip())


class TextExtractor:
    """Extracts text content from PDF documents.

    This class handles the extraction of text from PDF files using pymupdf,
    preserving text position, font size, and reading order.
    """

    def __init__(self, path: str | Path) -> None:
        """Initialize the text extractor.

        Args:
            path: Path to the PDF file.
        """
        self.path = Path(path) if isinstance(path, str) else path

    def extract(self) -> list[PageContent]:
        """Extract text content from all pages of the PDF.

        Returns:
            List of PageContent objects, one for each page.
        """
        pages: list[PageContent] = []

        doc = fitz.open(str(self.path))
        try:
            for page_num, page in enumerate(doc, start=1):
                page_content = self._extract_page(page, page_num)
                pages.append(page_content)
        finally:
            doc.close()

        return pages

    def _extract_page(self, page: fitz.Page, page_num: int) -> PageContent:
        """Extract content from a single page.

        Args:
            page: The pymupdf page object.
            page_num: The 1-indexed page number.

        Returns:
            PageContent object with extracted text blocks.
        """
        rect = page.rect
        page_content = PageContent(
            page_number=page_num,
            width=rect.width,
            height=rect.height,
        )

        # Extract text with detailed information using "dict" option
        text_dict = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)

        for block in text_dict.get("blocks", []):
            if block.get("type") == 0:  # Text block (not image)
                text_block = self._extract_text_block(block)
                if text_block:
                    page_content.blocks.append(text_block)

        return page_content

    def _extract_text_block(self, block: dict) -> TextBlock | None:
        """Extract a text block from pymupdf block dictionary.

        Args:
            block: Dictionary containing block information from pymupdf.

        Returns:
            TextBlock object or None if block has no text.
        """
        bbox = (
            block.get("bbox", (0, 0, 0, 0))
            if isinstance(block.get("bbox"), (list, tuple))
            else (0, 0, 0, 0)
        )

        # Collect all text from lines and spans
        lines_text: list[str] = []
        font_sizes: list[float] = []
        font_names: list[str] = []

        for line in block.get("lines", []):
            line_text_parts: list[str] = []
            for span in line.get("spans", []):
                span_text = span.get("text", "")
                if span_text:
                    line_text_parts.append(span_text)
                    if "size" in span:
                        font_sizes.append(span["size"])
                    if "font" in span:
                        font_names.append(span["font"])

            if line_text_parts:
                lines_text.append("".join(line_text_parts))

        if not lines_text:
            return None

        # Determine primary font size (most common or average)
        primary_font_size = None
        if font_sizes:
            primary_font_size = max(set(font_sizes), key=font_sizes.count)

        # Determine primary font name
        primary_font_name = None
        if font_names:
            primary_font_name = max(set(font_names), key=font_names.count)

        return TextBlock(
            text="\n".join(lines_text),
            bbox=tuple(bbox),  # type: ignore[arg-type]
            font_size=primary_font_size,
            font_name=primary_font_name,
        )
