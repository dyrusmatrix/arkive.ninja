"""
PDF text extraction utility using pdfplumber.

Usage as a module:
    from tools.pdf_extractor import extract_text, extract_all_pages

Usage as a CLI:
    python tools/pdf_extractor.py file.pdf
    python tools/pdf_extractor.py file.pdf --page 0
    python tools/pdf_extractor.py file.pdf --output out.txt
"""

import argparse
import sys
from pathlib import Path


def extract_text(pdf_path: str, page_number: int = 0) -> str:
    """Extract text from a single page of a PDF.

    Args:
        pdf_path: Path to the PDF file.
        page_number: Zero-based page index (default: 0, i.e. first page).

    Returns:
        Extracted text string, or an empty string if the page has no text.

    Raises:
        FileNotFoundError: If the PDF file does not exist.
        IndexError: If page_number is out of range.
    """
    import pdfplumber

    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    with pdfplumber.open(path) as pdf:
        if page_number >= len(pdf.pages):
            raise IndexError(
                f"Page {page_number} does not exist; "
                f"the PDF has {len(pdf.pages)} page(s)."
            )
        text = pdf.pages[page_number].extract_text()
        return text or ""


def extract_all_pages(pdf_path: str) -> list[str]:
    """Extract text from every page of a PDF.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        A list where each element is the extracted text for one page.
        Pages with no selectable text are represented as empty strings.

    Raises:
        FileNotFoundError: If the PDF file does not exist.
    """
    import pdfplumber

    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    with pdfplumber.open(path) as pdf:
        return [page.extract_text() or "" for page in pdf.pages]


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Extract text from a PDF file using pdfplumber."
    )
    parser.add_argument("pdf", help="Path to the PDF file")
    parser.add_argument(
        "--page",
        type=int,
        default=None,
        metavar="N",
        help="Zero-based page index to extract (default: all pages)",
    )
    parser.add_argument(
        "--output",
        "-o",
        metavar="FILE",
        help="Write extracted text to FILE instead of stdout",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        if args.page is not None:
            text = extract_text(args.pdf, args.page)
        else:
            pages = extract_all_pages(args.pdf)
            separator = "\n\n" + "-" * 40 + "\n\n"
            text = separator.join(pages)
    except (FileNotFoundError, IndexError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
        print(f"Text written to {args.output}")
    else:
        print(text)

    return 0


if __name__ == "__main__":
    sys.exit(main())
