import logging
import fitz  # PyMuPDF
import os

# Configure logging
log_dir = "log"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, 'service_logs.log'),
    level=logging.INFO,
    format='%(filename)s - %(funcName)s - %(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from a PDF file.

    Args:
        pdf_path (str): The file path of the PDF.

    Returns:
        str: The extracted text from the PDF.
    """
    try:
        document = fitz.open(pdf_path)
        text = ""
        for page_num in range(len(document)):
            page = document.load_page(page_num)
            text += page.get_text()
        logger.info(f"Extracted text from {pdf_path}")
        return text
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}")
        raise
