"""Structure detection for PDF documents.

This module provides utilities to detect document structure including
headings and lists based on font sizes and text patterns.
"""

import re
from dataclasses import dataclass
from enum import Enum

from pdf2md.extractors.text import PageContent, TextBlock


class ElementType(Enum):
    """Types of structural elements in a document."""

    HEADING1 = "heading1"
    HEADING2 = "heading2"
    HEADING3 = "heading3"
    HEADING4 = "heading4"
    HEADING5 = "heading5"
    HEADING6 = "heading6"
    PARAGRAPH = "paragraph"
    BULLET_LIST_ITEM = "bullet_list_item"
    NUMBERED_LIST_ITEM = "numbered_list_item"


@dataclass
class StructuredElement:
    """Represents a structural element detected in the document.

    Attributes:
        element_type: The type of structural element.
        text: The text content of the element.
        level: For headings, the level (1-6). For lists, the nesting level.
    """

    element_type: ElementType
    text: str
    level: int = 0


# Regex patterns for list detection
BULLET_PATTERN = re.compile(r"^\s*[-*+]\s+(.+)$")
NUMBERED_PATTERN = re.compile(r"^\s*(\d+)[.)]\s+(.+)$")


class StructureExtractor:
    """Detects document structure from extracted PDF content.

    This class analyzes text blocks to identify headings based on font size
    and lists based on text patterns.
    """

    # Font size thresholds for heading detection (relative to base font size)
    HEADING_RATIOS = {
        1: 1.8,  # H1: 1.8x or larger than base
        2: 1.5,  # H2: 1.5x - 1.8x
        3: 1.3,  # H3: 1.3x - 1.5x
        4: 1.15,  # H4: 1.15x - 1.3x
    }

    def __init__(self, pages: list[PageContent]) -> None:
        """Initialize the structure extractor.

        Args:
            pages: List of PageContent objects from text extraction.
        """
        self.pages = pages
        self._base_font_size: float | None = None

    def extract(self) -> list[list[StructuredElement]]:
        """Extract structural elements from all pages.

        Returns:
            List of lists, where each inner list contains StructuredElement
            objects for one page.
        """
        # Calculate base font size across all pages
        self._base_font_size = self._calculate_base_font_size()

        result: list[list[StructuredElement]] = []
        for page in self.pages:
            page_elements = self._extract_page_structure(page)
            result.append(page_elements)

        return result

    def _calculate_base_font_size(self) -> float:
        """Calculate the base (most common) font size across all pages.

        Returns:
            The most common font size, or 12.0 as default.
        """
        font_sizes: list[float] = []

        for page in self.pages:
            for block in page.blocks:
                if block.font_size is not None:
                    font_sizes.append(block.font_size)

        if not font_sizes:
            return 12.0

        # Return the most common font size
        return max(set(font_sizes), key=font_sizes.count)

    def _extract_page_structure(self, page: PageContent) -> list[StructuredElement]:
        """Extract structural elements from a single page.

        Args:
            page: The PageContent object to analyze.

        Returns:
            List of StructuredElement objects for the page.
        """
        elements: list[StructuredElement] = []

        for block in page.blocks:
            block_elements = self._analyze_block(block)
            elements.extend(block_elements)

        return elements

    def _analyze_block(self, block: TextBlock) -> list[StructuredElement]:
        """Analyze a text block and determine its structural type.

        Args:
            block: The TextBlock to analyze.

        Returns:
            List of StructuredElement objects (may be multiple for multi-line blocks).
        """
        elements: list[StructuredElement] = []
        text = block.text.strip()

        if not text:
            return elements

        # Split block into lines for list detection
        lines = text.split("\n")

        for line in lines:
            line = line.strip()
            if not line:
                continue

            element = self._classify_line(line, block.font_size)
            if element:
                elements.append(element)

        return elements

    def _classify_line(
        self, line: str, font_size: float | None
    ) -> StructuredElement | None:
        """Classify a single line of text.

        Args:
            line: The text line to classify.
            font_size: The font size of the line (if known).

        Returns:
            StructuredElement for the line, or None if empty.
        """
        if not line.strip():
            return None

        # Check for bullet list
        bullet_match = BULLET_PATTERN.match(line)
        if bullet_match:
            return StructuredElement(
                element_type=ElementType.BULLET_LIST_ITEM,
                text=bullet_match.group(1).strip(),
                level=1,
            )

        # Check for numbered list
        numbered_match = NUMBERED_PATTERN.match(line)
        if numbered_match:
            return StructuredElement(
                element_type=ElementType.NUMBERED_LIST_ITEM,
                text=numbered_match.group(2).strip(),
                level=1,
            )

        # Check for heading based on font size
        heading_level = self._detect_heading_level(font_size)
        if heading_level:
            element_type = self._get_heading_type(heading_level)
            return StructuredElement(
                element_type=element_type,
                text=line,
                level=heading_level,
            )

        # Default to paragraph
        return StructuredElement(
            element_type=ElementType.PARAGRAPH,
            text=line,
            level=0,
        )

    def _detect_heading_level(self, font_size: float | None) -> int | None:
        """Detect heading level based on font size ratio.

        Args:
            font_size: The font size to check.

        Returns:
            Heading level (1-6) or None if not a heading.
        """
        if font_size is None or self._base_font_size is None:
            return None

        if self._base_font_size == 0:
            return None

        ratio = font_size / self._base_font_size

        # Check heading levels from largest to smallest
        if ratio >= self.HEADING_RATIOS[1]:
            return 1
        elif ratio >= self.HEADING_RATIOS[2]:
            return 2
        elif ratio >= self.HEADING_RATIOS[3]:
            return 3
        elif ratio >= self.HEADING_RATIOS[4]:
            return 4

        return None

    def _get_heading_type(self, level: int) -> ElementType:
        """Get the ElementType for a heading level.

        Args:
            level: Heading level (1-6).

        Returns:
            Corresponding ElementType.
        """
        heading_types = {
            1: ElementType.HEADING1,
            2: ElementType.HEADING2,
            3: ElementType.HEADING3,
            4: ElementType.HEADING4,
            5: ElementType.HEADING5,
            6: ElementType.HEADING6,
        }
        return heading_types.get(level, ElementType.PARAGRAPH)
