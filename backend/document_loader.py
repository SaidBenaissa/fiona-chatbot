import os
import glob
from venv import logger
import chardet
from typing import List, Tuple, Dict, Any

import pdfplumber
import pytesseract
from PIL import Image
from pdf2image import convert_from_path

# Function to extract text from PDF files with OCR fallback
def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    if not text.strip():
        # Fallback to OCR if no text is extracted
        logger.warning(f"No text extracted using pdfplumber. Falling back to OCR for: {pdf_path}")
        images = convert_from_path(pdf_path)
        for image in images:
            text += pytesseract.image_to_string(image)

    return text

def load_documents_from_directory(directory: str) -> List[Tuple[str, str, Dict[str, Any]]]: # Return metadata
    documents = []
    for file_path in glob.glob(os.path.join(directory, '*')):
        filename = os.path.basename(file_path)
        ext = os.path.splitext(filename)[1].lower()
        metadata = {"filename": filename} # Store filename in metadata
        content = ""
        try:
            if ext == '.pdf':
                content = extract_text_from_pdf(file_path)
                logger.info(f"Extracted {len(content)} characters from PDF: {filename}")
                # logger.debug(f"Extracted content preview from PDF {filename}: {content[:200]}...") # Keep debug short
                if not content.strip():
                    logger.warning(f"No text extracted from PDF: {filename}")
            elif ext in ['.txt', '.js']:
                with open(file_path, 'rb') as f:
                    raw = f.read()
                    encoding = chardet.detect(raw)['encoding'] or 'utf-8'
                    content = raw.decode(encoding, errors='replace')
                logger.info(f"Loaded text file: {filename}")
            # ...existing code for other file types if any...
            else:
                logger.warning(f"Unsupported file type: {filename}")
                continue # Skip unsupported files

            if content.strip(): # Only add documents with content
                documents.append((filename, content, metadata))
            else:
                logger.warning(f"Skipping document with no content: {filename}")

        except Exception as e:
            logger.error(f"Error processing file {filename}: {e}", exc_info=True)

    return documents