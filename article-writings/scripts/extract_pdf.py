"""
Extract text from a PDF file for use in article writing.

Usage:
  python scripts/extract_pdf.py <input.pdf> <output.txt>

Example:
  python scripts/extract_pdf.py paper.pdf scripts/extracted_source.txt

Dependencies:
  pip install PyPDF2
"""

import sys
import os

def extract_text(pdf_path, output_path):
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        print("PyPDF2 not installed. Install with: pip install PyPDF2")
        sys.exit(1)

    if not os.path.exists(pdf_path):
        print(f"Error: File not found: {pdf_path}")
        sys.exit(1)

    reader = PdfReader(pdf_path)
    full_text = []

    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            full_text.append(f"--- Page {i+1} ---\n{text}")

    result = "\n\n".join(full_text)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result)

    print(f"Extracted {len(reader.pages)} pages -> {output_path}")
    print(f"Total characters: {len(result)}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python extract_pdf.py <input.pdf> <output.txt>")
        sys.exit(1)

    extract_text(sys.argv[1], sys.argv[2])
