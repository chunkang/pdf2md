"""Tests for the CLI interface.

TDD RED Phase: These tests define the expected behavior of the CLI.
"""

from pathlib import Path

from typer.testing import CliRunner

from pdf2md import __version__
from pdf2md.cli import app

runner = CliRunner()


class TestCLI:
    """Tests for the CLI application."""

    def test_version_flag(self) -> None:
        """Should display version with --version flag."""
        result = runner.invoke(app, ["--version"])

        assert result.exit_code == 0
        assert __version__ in result.stdout

    def test_help_flag(self) -> None:
        """Should display help with --help flag."""
        result = runner.invoke(app, ["--help"])

        assert result.exit_code == 0
        assert "pdf2md" in result.stdout.lower() or "PDF" in result.stdout
        assert "INPUT_FILE" in result.stdout or "input" in result.stdout.lower()

    def test_convert_simple_pdf(self, sample_pdf: Path, temp_dir: Path) -> None:
        """Should convert PDF to Markdown via CLI."""
        output_path = temp_dir / "output.md"

        result = runner.invoke(app, [str(sample_pdf), str(output_path)])

        assert result.exit_code == 0
        assert output_path.exists()
        content = output_path.read_text()
        assert "Hello" in content

    def test_convert_with_default_output(self, sample_pdf: Path) -> None:
        """Should use default output path (input.md) when not specified."""
        expected_output = sample_pdf.with_suffix(".md")

        try:
            result = runner.invoke(app, [str(sample_pdf)])

            assert result.exit_code == 0
            assert expected_output.exists()
        finally:
            # Cleanup
            if expected_output.exists():
                expected_output.unlink()

    def test_convert_nonexistent_file(self, temp_dir: Path) -> None:
        """Should exit with code 1 for non-existent file."""
        result = runner.invoke(
            app, [str(temp_dir / "nonexistent.pdf"), str(temp_dir / "output.md")]
        )

        assert result.exit_code == 1
        # The exit code is the main check; error messages may go to stderr
        # which typer's CliRunner may not capture in result.output

    def test_convert_invalid_pdf(self, non_pdf_file: Path, temp_dir: Path) -> None:
        """Should exit with code 2 for invalid PDF."""
        result = runner.invoke(app, [str(non_pdf_file), str(temp_dir / "output.md")])

        assert result.exit_code == 2

    def test_convert_password_protected_pdf(
        self, password_protected_pdf: Path, temp_dir: Path
    ) -> None:
        """Should exit with code 3 for password-protected PDF."""
        result = runner.invoke(
            app, [str(password_protected_pdf), str(temp_dir / "output.md")]
        )

        assert result.exit_code == 3
        # The exit code is the main check; error messages may go to stderr

    def test_convert_with_force_flag(self, sample_pdf: Path, temp_dir: Path) -> None:
        """Should overwrite existing file with --force flag."""
        output_path = temp_dir / "existing.md"
        output_path.write_text("Existing content")

        result = runner.invoke(app, [str(sample_pdf), str(output_path), "--force"])

        assert result.exit_code == 0
        assert "Hello" in output_path.read_text()

    def test_convert_without_force_existing_file(
        self, sample_pdf: Path, temp_dir: Path
    ) -> None:
        """Should fail when output exists without --force."""
        output_path = temp_dir / "existing.md"
        output_path.write_text("Existing content")

        result = runner.invoke(app, [str(sample_pdf), str(output_path)])

        assert result.exit_code == 4
        # Original content preserved
        assert output_path.read_text() == "Existing content"

    def test_verbose_flag(self, sample_pdf: Path, temp_dir: Path) -> None:
        """Should show verbose output with --verbose flag."""
        output_path = temp_dir / "output.md"

        result = runner.invoke(
            app, [str(sample_pdf), str(output_path), "--verbose"]
        )

        assert result.exit_code == 0
        # Verbose should show more information
        assert len(result.stdout) > 0

    def test_quiet_flag(self, sample_pdf: Path, temp_dir: Path) -> None:
        """Should suppress output with --quiet flag."""
        output_path = temp_dir / "output.md"

        result = runner.invoke(app, [str(sample_pdf), str(output_path), "--quiet"])

        assert result.exit_code == 0
        # Quiet should minimize output
        # (may still have minimal output, but should succeed)


class TestCLIShortFlags:
    """Tests for CLI short flags."""

    def test_force_short_flag(self, sample_pdf: Path, temp_dir: Path) -> None:
        """Should accept -f as short for --force."""
        output_path = temp_dir / "existing.md"
        output_path.write_text("Existing content")

        result = runner.invoke(app, [str(sample_pdf), str(output_path), "-f"])

        assert result.exit_code == 0

    def test_verbose_short_flag(self, sample_pdf: Path, temp_dir: Path) -> None:
        """Should accept -v as short for --verbose."""
        output_path = temp_dir / "output.md"

        result = runner.invoke(app, [str(sample_pdf), str(output_path), "-v"])

        assert result.exit_code == 0

    def test_quiet_short_flag(self, sample_pdf: Path, temp_dir: Path) -> None:
        """Should accept -q as short for --quiet."""
        output_path = temp_dir / "output.md"

        result = runner.invoke(app, [str(sample_pdf), str(output_path), "-q"])

        assert result.exit_code == 0


class TestCLIEdgeCases:
    """Edge case tests for CLI."""

    def test_output_to_nonexistent_directory(
        self, sample_pdf: Path, temp_dir: Path
    ) -> None:
        """Should exit with code 4 for non-existent output directory."""
        result = runner.invoke(
            app, [str(sample_pdf), str(temp_dir / "nonexistent" / "output.md")]
        )

        assert result.exit_code == 4
