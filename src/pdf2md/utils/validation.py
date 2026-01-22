"""Input and output validation utilities for PDF to Markdown conversion.

This module provides validation functions to ensure input files are valid PDFs
and output paths are writable.
"""

from pathlib import Path

import fitz  # pymupdf


class ValidationError(Exception):
    """Exception raised when validation fails.

    Attributes:
        message: Human-readable error description.
        exit_code: Exit code for CLI (0=success, 1-5=various errors).
    """

    def __init__(self, message: str, exit_code: int = 5) -> None:
        """Initialize ValidationError.

        Args:
            message: Human-readable error description.
            exit_code: Exit code for CLI. Defaults to 5 (unexpected error).
        """
        super().__init__(message)
        self.exit_code = exit_code


def validate_input_file(path: str | Path) -> None:
    """Validate that the input file is a valid, readable PDF.

    Args:
        path: Path to the input PDF file.

    Raises:
        ValidationError: If the file is not found (exit_code=1),
            not a valid PDF (exit_code=2), or password-protected (exit_code=3).
    """
    filepath = Path(path) if isinstance(path, str) else path

    # Check if file exists
    if not filepath.exists():
        raise ValidationError(
            f"Input file not found: {filepath}",
            exit_code=1,
        )

    # Check if file has .pdf extension
    if filepath.suffix.lower() != ".pdf":
        raise ValidationError(
            f"Input file is not a PDF (invalid extension): {filepath}",
            exit_code=2,
        )

    # Try to open the PDF to validate it
    try:
        doc = fitz.open(str(filepath))
    except Exception as e:
        raise ValidationError(
            f"Input file is not a valid PDF: {filepath}. Error: {e}",
            exit_code=2,
        ) from e

    # Check if PDF is password-protected (encrypted and needs password)
    try:
        if doc.is_encrypted:
            # Try to authenticate without password
            if not doc.authenticate(""):
                raise ValidationError(
                    f"PDF is password-protected and cannot be processed: {filepath}",
                    exit_code=3,
                )
    except ValidationError:
        doc.close()
        raise
    except Exception:
        # If we can't check encryption, assume it's okay
        pass

    doc.close()


def validate_output_path(
    path: str | Path,
    force: bool = False,
) -> None:
    """Validate that the output path is writable.

    Args:
        path: Path for the output Markdown file.
        force: If True, allow overwriting existing files.

    Raises:
        ValidationError: If the parent directory does not exist (exit_code=4)
            or if the file exists and force is False (exit_code=4).
    """
    filepath = Path(path) if isinstance(path, str) else path
    parent = filepath.parent

    # Check if parent directory exists
    if not parent.exists():
        raise ValidationError(
            f"Output directory not found: {parent}",
            exit_code=4,
        )

    # Check if file already exists and force is not set
    if filepath.exists() and not force:
        raise ValidationError(
            f"Output file already exists: {filepath}. Use --force to overwrite.",
            exit_code=4,
        )
