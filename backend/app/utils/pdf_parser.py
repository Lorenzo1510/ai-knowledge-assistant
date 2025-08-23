import pymupdf


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from a PDF file.
    """
    doc = pymupdf.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text
