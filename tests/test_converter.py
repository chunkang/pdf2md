"""Tests for the PDF to Markdown converter orchestrator.

TDD RED Phase: These tests define the expected behavior of the converter.
"""

from pathlib import Path

from pdf2md.converter import ConversionResult, PDFToMarkdownConverter


class TestPDFToMarkdownConverter:
    """Tests for PDFToMarkdownConverter class."""

    def test_convert_simple_pdf(self, sample_pdf: Path, temp_dir: Path) -> None:
        """Should convert a simple PDF to Markdown."""
        output_path = temp_dir / "output.md"

        converter = PDFToMarkdownConverter(sample_pdf, output_path)
        result = converter.convert()

        assert result.success is True
        assert result.exit_code == 0
        assert output_path.exists()

        content = output_path.read_text()
        assert "Hello" in content
        assert "World" in content

    def test_convert_multi_page_pdf(self, multi_page_pdf: Path, temp_dir: Path) -> None:
        """Should convert all pages of a multi-page PDF."""
        output_path = temp_dir / "output.md"

        converter = PDFToMarkdownConverter(multi_page_pdf, output_path)
        result = converter.convert()

        assert result.success is True
        content = output_path.read_text()
        assert "Page 1" in content
        assert "Page 2" in content
        assert "Page 3" in content

    def test_convert_pdf_with_headings(
        self, pdf_with_headings: Path, temp_dir: Path
    ) -> None:
        """Should preserve heading structure in Markdown output."""
        output_path = temp_dir / "output.md"

        converter = PDFToMarkdownConverter(pdf_with_headings, output_path)
        result = converter.convert()

        assert result.success is True
        content = output_path.read_text()
        # Should have markdown headings
        assert "#" in content

    def test_convert_pdf_with_lists(
        self, pdf_with_lists: Path, temp_dir: Path
    ) -> None:
        """Should preserve list structure in Markdown output."""
        output_path = temp_dir / "output.md"

        converter = PDFToMarkdownConverter(pdf_with_lists, output_path)
        result = converter.convert()

        assert result.success is True
        content = output_path.read_text()
        # Should have markdown lists
        assert "- " in content or "1. " in content

    def test_convert_nonexistent_file_returns_error(self, temp_dir: Path) -> None:
        """Should return error result for non-existent input file."""
        input_path = temp_dir / "nonexistent.pdf"
        output_path = temp_dir / "output.md"

        converter = PDFToMarkdownConverter(input_path, output_path)
        result = converter.convert()

        assert result.success is False
        assert result.exit_code == 1
        assert "not found" in result.error_message.lower()

    def test_convert_invalid_pdf_returns_error(
        self, non_pdf_file: Path, temp_dir: Path
    ) -> None:
        """Should return error result for invalid PDF file."""
        output_path = temp_dir / "output.md"

        converter = PDFToMarkdownConverter(non_pdf_file, output_path)
        result = converter.convert()

        assert result.success is False
        assert result.exit_code == 2

    def test_convert_password_protected_pdf_returns_error(
        self, password_protected_pdf: Path, temp_dir: Path
    ) -> None:
        """Should return error result for password-protected PDF."""
        output_path = temp_dir / "output.md"

        converter = PDFToMarkdownConverter(password_protected_pdf, output_path)
        result = converter.convert()

        assert result.success is False
        assert result.exit_code == 3
        assert "password" in result.error_message.lower()

    def test_convert_to_invalid_output_path_returns_error(
        self, sample_pdf: Path, temp_dir: Path
    ) -> None:
        """Should return error result for invalid output path."""
        output_path = temp_dir / "nonexistent_dir" / "output.md"

        converter = PDFToMarkdownConverter(sample_pdf, output_path)
        result = converter.convert()

        assert result.success is False
        assert result.exit_code == 4

    def test_convert_with_existing_output_without_force(
        self, sample_pdf: Path, temp_dir: Path
    ) -> None:
        """Should not overwrite existing file without force flag."""
        output_path = temp_dir / "existing.md"
        output_path.write_text("Existing content")

        converter = PDFToMarkdownConverter(sample_pdf, output_path, force=False)
        result = converter.convert()

        assert result.success is False
        assert result.exit_code == 4
        # Original content should be preserved
        assert output_path.read_text() == "Existing content"

    def test_convert_with_existing_output_with_force(
        self, sample_pdf: Path, temp_dir: Path
    ) -> None:
        """Should overwrite existing file with force flag."""
        output_path = temp_dir / "existing.md"
        output_path.write_text("Existing content")

        converter = PDFToMarkdownConverter(sample_pdf, output_path, force=True)
        result = converter.convert()

        assert result.success is True
        # Original content should be replaced
        assert output_path.read_text() != "Existing content"
        assert "Hello" in output_path.read_text()

    def test_convert_accepts_string_paths(
        self, sample_pdf: Path, temp_dir: Path
    ) -> None:
        """Should accept string paths."""
        output_path = temp_dir / "output.md"

        converter = PDFToMarkdownConverter(str(sample_pdf), str(output_path))
        result = converter.convert()

        assert result.success is True


class TestConversionResult:
    """Tests for ConversionResult data class."""

    def test_success_result(self) -> None:
        """Should create successful result."""
        result = ConversionResult(
            success=True,
            exit_code=0,
            output_path=Path("/test/output.md"),
            pages_converted=5,
        )

        assert result.success is True
        assert result.exit_code == 0
        assert result.pages_converted == 5
        assert result.error_message is None

    def test_error_result(self) -> None:
        """Should create error result."""
        result = ConversionResult(
            success=False,
            exit_code=1,
            error_message="File not found",
        )

        assert result.success is False
        assert result.exit_code == 1
        assert result.error_message == "File not found"
