import PyPDF2
from io import BytesIO

def extract_text_from_pdf(uploaded_file):
    try:
        text = ""
        pdf_reader = PyPDF2.PdfReader(BytesIO(uploaded_file.read()))
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        raise ValueError(f"PDF extraction failed: {str(e)}")