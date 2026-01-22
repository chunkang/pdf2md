"""Command-line interface for PDF to Markdown converter.

This module provides the CLI using typer with rich output formatting.
"""

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from pdf2md import __version__
from pdf2md.converter import PDFToMarkdownConverter

app = typer.Typer(
    name="pdf2md",
    help="Convert PDF documents to Markdown format.",
    add_completion=False,
)

console = Console()
error_console = Console(stderr=True)


def version_callback(value: bool) -> None:
    """Print version and exit."""
    if value:
        console.print(f"pdf2md version {__version__}")
        raise typer.Exit()


@app.command()
def main(
    input_file: Annotated[
        Path,
        typer.Argument(
            help="Path to the input PDF file.",
            exists=False,  # We handle existence check ourselves for better error messages
        ),
    ],
    output_file: Annotated[
        Path | None,
        typer.Argument(
            help="Path for the output Markdown file. Defaults to input filename with .md extension.",
        ),
    ] = None,
    force: Annotated[
        bool,
        typer.Option(
            "--force",
            "-f",
            help="Overwrite output file if it exists.",
        ),
    ] = False,
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose",
            "-v",
            help="Show verbose output.",
        ),
    ] = False,
    quiet: Annotated[
        bool,
        typer.Option(
            "--quiet",
            "-q",
            help="Suppress output except errors.",
        ),
    ] = False,
    version: Annotated[
        bool | None,
        typer.Option(
            "--version",
            callback=version_callback,
            is_eager=True,
            help="Show version and exit.",
        ),
    ] = None,
) -> None:
    """Convert a PDF file to Markdown format.

    The converter extracts text from the PDF, detects document structure
    (headings, lists, paragraphs), and outputs properly formatted Markdown.

    Exit Codes:
        0: Success
        1: Input file not found
        2: Invalid PDF file
        3: Password-protected PDF
        4: Output write error
        5: Unexpected error
    """
    # Determine output path
    if output_file is None:
        output_file = input_file.with_suffix(".md")

    # Show progress for conversion
    if not quiet:
        if verbose:
            console.print(f"[bold]pdf2md[/bold] version {__version__}")
            console.print(f"Input:  {input_file}")
            console.print(f"Output: {output_file}")
            console.print()

    # Create converter and run
    converter = PDFToMarkdownConverter(input_file, output_file, force=force)

    if not quiet:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True,
        ) as progress:
            progress.add_task("Converting PDF to Markdown...", total=None)
            result = converter.convert()
    else:
        result = converter.convert()

    # Handle result
    if result.success:
        if not quiet:
            console.print(
                f"[green]Success![/green] Converted {result.pages_converted} page(s) to {output_file}"
            )
        raise typer.Exit(0)
    else:
        error_console.print(f"[red]Error:[/red] {result.error_message}")
        raise typer.Exit(result.exit_code)


if __name__ == "__main__":
    app()
