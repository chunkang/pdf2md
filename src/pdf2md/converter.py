"""PDF to Markdown converter orchestrator.

This module provides the main conversion pipeline that coordinates
text extraction, structure detection, and markdown formatting.
"""

from dataclasses import dataclass
from pathlib import Path

from pdf2md.extractors.structure import StructureExtractor
from pdf2md.extractors.text import TextExtractor
from pdf2md.formatters.markdown import MarkdownFormatter
from pdf2md.utils.validation import (
    ValidationError,
    validate_input_file,
    validate_output_path,
)


@dataclass
class ConversionResult:
    """Result of a PDF to Markdown conversion.

    Attributes:
        success: Whether the conversion was successful.
        exit_code: Exit code (0 for success, 1-5 for various errors).
        output_path: Path to the output file (if successful).
        pages_converted: Number of pages converted (if successful).
        error_message: Error message (if failed).
    """

    success: bool
    exit_code: int
    output_path: Path | None = None
    pages_converted: int = 0
    error_message: str | None = None


class PDFToMarkdownConverter:
    """Orchestrates the PDF to Markdown conversion pipeline.

    This class coordinates the extraction, structure detection, and
    formatting stages to convert a PDF file to Markdown.
    """

    def __init__(
        self,
        input_path: str | Path,
        output_path: str | Path,
        force: bool = False,
    ) -> None:
        """Initialize the converter.

        Args:
            input_path: Path to the input PDF file.
            output_path: Path for the output Markdown file.
            force: If True, overwrite existing output file.
        """
        self.input_path = Path(input_path) if isinstance(input_path, str) else input_path
        self.output_path = Path(output_path) if isinstance(output_path, str) else output_path
        self.force = force

    def convert(self) -> ConversionResult:
        """Execute the PDF to Markdown conversion.

        Returns:
            ConversionResult with success status and details.
        """
        # Validate input file
        try:
            validate_input_file(self.input_path)
        except ValidationError as e:
            return ConversionResult(
                success=False,
                exit_code=e.exit_code,
                error_message=str(e),
            )

        # Validate output path
        try:
            validate_output_path(self.output_path, force=self.force)
        except ValidationError as e:
            return ConversionResult(
                success=False,
                exit_code=e.exit_code,
                error_message=str(e),
            )

        # Extract text from PDF
        try:
            text_extractor = TextExtractor(self.input_path)
            pages = text_extractor.extract()
        except Exception as e:
            return ConversionResult(
                success=False,
                exit_code=5,
                error_message=f"Error extracting text: {e}",
            )

        # Detect structure
        try:
            structure_extractor = StructureExtractor(pages)
            structured_pages = structure_extractor.extract()
        except Exception as e:
            return ConversionResult(
                success=False,
                exit_code=5,
                error_message=f"Error detecting structure: {e}",
            )

        # Format as Markdown
        try:
            formatter = MarkdownFormatter(structured_pages)
            markdown_content = formatter.format()
        except Exception as e:
            return ConversionResult(
                success=False,
                exit_code=5,
                error_message=f"Error formatting markdown: {e}",
            )

        # Write output file
        try:
            self.output_path.write_text(markdown_content, encoding="utf-8")
        except Exception as e:
            return ConversionResult(
                success=False,
                exit_code=4,
                error_message=f"Error writing output file: {e}",
            )

        return ConversionResult(
            success=True,
            exit_code=0,
            output_path=self.output_path,
            pages_converted=len(pages),
        )
