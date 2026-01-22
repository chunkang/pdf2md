"""Tests for input/output validation utilities.

TDD RED Phase: These tests define the expected behavior of the validation module.
"""

from pathlib import Path

import pytest

from pdf2md.utils.validation import (
    ValidationError,
    validate_input_file,
    validate_output_path,
)


class TestValidateInputFile:
    """Tests for validate_input_file function."""

    def test_valid_pdf_file_passes_validation(self, sample_pdf: Path) -> None:
        """A valid PDF file should pass validation without raising."""
        # Should not raise any exception
        result = validate_input_file(sample_pdf)
        assert result is None

    def test_nonexistent_file_raises_validation_error(self, temp_dir: Path) -> None:
        """A file that does not exist should raise ValidationError with exit code 1."""
        nonexistent = temp_dir / "does_not_exist.pdf"
        with pytest.raises(ValidationError) as exc_info:
            validate_input_file(nonexistent)
        assert exc_info.value.exit_code == 1
        assert "not found" in str(exc_info.value).lower()

    def test_invalid_pdf_raises_validation_error(self, non_pdf_file: Path) -> None:
        """A file that is not a valid PDF should raise ValidationError with exit code 2."""
        with pytest.raises(ValidationError) as exc_info:
            validate_input_file(non_pdf_file)
        assert exc_info.value.exit_code == 2
        assert "invalid" in str(exc_info.value).lower() or "not a valid pdf" in str(exc_info.value).lower()

    def test_password_protected_pdf_raises_validation_error(
        self, password_protected_pdf: Path
    ) -> None:
        """A password-protected PDF should raise ValidationError with exit code 3."""
        with pytest.raises(ValidationError) as exc_info:
            validate_input_file(password_protected_pdf)
        assert exc_info.value.exit_code == 3
        assert "password" in str(exc_info.value).lower()

    def test_non_pdf_extension_raises_validation_error(self, text_file: Path) -> None:
        """A file without .pdf extension should raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            validate_input_file(text_file)
        # Could be exit code 1 (not found as PDF) or 2 (invalid)
        assert exc_info.value.exit_code in (1, 2)

    def test_accepts_pathlib_path(self, sample_pdf: Path) -> None:
        """Should accept pathlib.Path objects."""
        result = validate_input_file(sample_pdf)
        assert result is None

    def test_accepts_string_path(self, sample_pdf: Path) -> None:
        """Should accept string paths."""
        result = validate_input_file(str(sample_pdf))
        assert result is None

    def test_empty_pdf_passes_validation(self, empty_pdf: Path) -> None:
        """An empty but valid PDF should pass validation."""
        result = validate_input_file(empty_pdf)
        assert result is None


class TestValidateOutputPath:
    """Tests for validate_output_path function."""

    def test_valid_output_path_passes(self, temp_dir: Path) -> None:
        """A valid output path in an existing directory should pass."""
        output_path = temp_dir / "output.md"
        result = validate_output_path(output_path)
        assert result is None

    def test_output_path_with_nonexistent_parent_raises_error(
        self, temp_dir: Path
    ) -> None:
        """An output path in a non-existent directory should raise ValidationError."""
        output_path = temp_dir / "nonexistent_dir" / "output.md"
        with pytest.raises(ValidationError) as exc_info:
            validate_output_path(output_path)
        assert exc_info.value.exit_code == 4
        assert "directory" in str(exc_info.value).lower() or "not found" in str(exc_info.value).lower()

    def test_existing_file_without_force_raises_error(self, temp_dir: Path) -> None:
        """An existing output file without force flag should raise ValidationError."""
        output_path = temp_dir / "existing.md"
        output_path.write_text("Existing content")

        with pytest.raises(ValidationError) as exc_info:
            validate_output_path(output_path, force=False)
        assert exc_info.value.exit_code == 4
        assert "exists" in str(exc_info.value).lower() or "overwrite" in str(exc_info.value).lower()

    def test_existing_file_with_force_passes(self, temp_dir: Path) -> None:
        """An existing output file with force flag should pass validation."""
        output_path = temp_dir / "existing.md"
        output_path.write_text("Existing content")

        result = validate_output_path(output_path, force=True)
        assert result is None

    def test_accepts_pathlib_path(self, temp_dir: Path) -> None:
        """Should accept pathlib.Path objects."""
        output_path = temp_dir / "output.md"
        result = validate_output_path(output_path)
        assert result is None

    def test_accepts_string_path(self, temp_dir: Path) -> None:
        """Should accept string paths."""
        output_path = temp_dir / "output.md"
        result = validate_output_path(str(output_path))
        assert result is None


class TestValidationError:
    """Tests for ValidationError exception class."""

    def test_validation_error_has_message(self) -> None:
        """ValidationError should store the error message."""
        error = ValidationError("Test error message", exit_code=1)
        assert str(error) == "Test error message"

    def test_validation_error_has_exit_code(self) -> None:
        """ValidationError should store the exit code."""
        error = ValidationError("Test error", exit_code=3)
        assert error.exit_code == 3

    def test_validation_error_default_exit_code(self) -> None:
        """ValidationError should have a default exit code of 5 (unexpected error)."""
        error = ValidationError("Test error")
        assert error.exit_code == 5

    def test_validation_error_is_exception(self) -> None:
        """ValidationError should be an Exception subclass."""
        error = ValidationError("Test", exit_code=1)
        assert isinstance(error, Exception)
