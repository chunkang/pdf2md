"""Markdown formatting for structured PDF content.

This module provides utilities to convert structured elements extracted
from PDF documents into properly formatted Markdown text.
"""

from pdf2md.extractors.structure import ElementType, StructuredElement


class MarkdownFormatter:
    """Converts structured elements to Markdown format.

    This class takes structured elements from the structure extractor
    and formats them as valid Markdown text.
    """

    # Mapping of heading levels to Markdown prefix
    HEADING_PREFIXES = {
        ElementType.HEADING1: "#",
        ElementType.HEADING2: "##",
        ElementType.HEADING3: "###",
        ElementType.HEADING4: "####",
        ElementType.HEADING5: "#####",
        ElementType.HEADING6: "######",
    }

    def __init__(self, pages: list[list[StructuredElement]]) -> None:
        """Initialize the markdown formatter.

        Args:
            pages: List of pages, where each page is a list of StructuredElement.
        """
        self.pages = pages

    def format(self) -> str:
        """Format all pages as Markdown.

        Returns:
            Complete Markdown document as a string.
        """
        formatted_pages: list[str] = []

        for page_elements in self.pages:
            page_content = self._format_page(page_elements)
            if page_content.strip():
                formatted_pages.append(page_content)

        return "\n\n".join(formatted_pages)

    def _format_page(self, elements: list[StructuredElement]) -> str:
        """Format a single page of elements.

        Args:
            elements: List of StructuredElement objects for the page.

        Returns:
            Formatted Markdown string for the page.
        """
        if not elements:
            return ""

        lines: list[str] = []
        numbered_list_counter = 0
        prev_element_type: ElementType | None = None

        for element in elements:
            # Reset numbered list counter if not a numbered list item
            if element.element_type != ElementType.NUMBERED_LIST_ITEM:
                numbered_list_counter = 0

            # Add blank line before headings (if not first element)
            if (
                element.element_type in self.HEADING_PREFIXES
                and prev_element_type is not None
            ):
                lines.append("")

            # Add blank line after headings
            if prev_element_type in self.HEADING_PREFIXES:
                # Don't add if we already have one from above
                if lines and lines[-1] != "":
                    lines.append("")

            # Format the element
            formatted_line = self._format_element(element, numbered_list_counter)

            # Update numbered list counter
            if element.element_type == ElementType.NUMBERED_LIST_ITEM:
                numbered_list_counter += 1

            lines.append(formatted_line)
            prev_element_type = element.element_type

        return "\n".join(lines)

    def _format_element(
        self, element: StructuredElement, numbered_list_counter: int
    ) -> str:
        """Format a single element as Markdown.

        Args:
            element: The StructuredElement to format.
            numbered_list_counter: Current counter for numbered lists.

        Returns:
            Formatted Markdown string for the element.
        """
        element_type = element.element_type
        text = element.text

        # Handle headings
        if element_type in self.HEADING_PREFIXES:
            prefix = self.HEADING_PREFIXES[element_type]
            return f"{prefix} {text}"

        # Handle bullet lists
        if element_type == ElementType.BULLET_LIST_ITEM:
            return f"- {text}"

        # Handle numbered lists
        if element_type == ElementType.NUMBERED_LIST_ITEM:
            number = numbered_list_counter + 1
            return f"{number}. {text}"

        # Handle paragraphs and other text
        return text
