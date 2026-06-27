# ============================================================
# pdf_reader.py
# This file's only job: open a PDF and return its text.
# ============================================================

import PyPDF2  # The library that knows how to read PDF files
import io      # Helps us handle file data from Streamlit uploads


def extract_text_from_pdf(pdf_file):
    """
    Takes a PDF file (either a file path string OR an uploaded file object)
    and returns all the text inside it as one big string.
    """

    text = ""  # We'll build up our text here, starting empty

    try:
        # PyPDF2 needs to read the file in binary mode ("rb" = read binary)
        # The 'io.BytesIO' part converts Streamlit's uploaded file into
        # something PyPDF2 can read
        reader = PyPDF2.PdfReader(io.BytesIO(pdf_file.read()))

        # PDFs have multiple pages. We loop through every page.
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]           # Get one page
            page_text = page.extract_text()         # Pull the text out

            # Sometimes a page has no text (like an image-only page)
            # The 'if page_text' check prevents a crash in that case
            if page_text:
                text += page_text + "\n"  # Add this page's text + a line break

    except Exception as e:
        # If something goes wrong, tell us what happened instead of just crashing
        print(f"Error reading PDF: {e}")
        return ""

    return text  # Hand back all the text we collected


def clean_text(raw_text):
    """
    Cleans up the raw text from the PDF.
    PDFs often have weird spacing, extra blank lines, etc.
    This makes the text nicer to work with.
    """

    # Split the text into individual lines
    lines = raw_text.split('\n')

    cleaned_lines = []
    for line in lines:
        line = line.strip()        # Remove spaces from start and end of each line
        if line:                   # Only keep lines that have actual content
            cleaned_lines.append(line)

    # Join all cleaned lines back together with a single newline between them
    return '\n'.join(cleaned_lines)