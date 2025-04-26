import os
from typing import List, Dict, Any
import re # Import re for splitting
import logging

logger = logging.getLogger(__name__)

# Function to split text into chunks (e.g., by paragraphs)
def split_text_into_chunks(text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> List[str]:
    # Simple split by double newline first, then refine if needed
    paragraphs = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]
    # Further split large paragraphs if necessary (optional, can add later)
    # For now, treat each paragraph as a chunk
    return paragraphs

def load_documents() -> List[Dict[str, Any]]:
    documents_chunks = []
    base_path = "./documents"
    if not os.path.exists(base_path) or not os.listdir(base_path):
        logger.warning("Warning: No documents found in the documents directory or directory doesn't exist.")
        return []
    for filename in os.listdir(base_path):
        file_path = os.path.join(base_path, filename)
        if os.path.isfile(file_path) and filename.endswith('.txt'): # Ensure it's a txt file
            try:
                with open(file_path, "r", encoding='utf-8') as file:
                    content = file.read()
                    chunks = split_text_into_chunks(content)
                    for i, chunk in enumerate(chunks):
                        documents_chunks.append({
                            "content": chunk,
                            "metadata": {
                                "source": filename,
                                "chunk_index": i
                            }
                        })
                logger.info(f"Loaded and chunked {filename} into {len(chunks)} chunks.")
            except Exception as e:
                logger.error(f"Error reading or chunking file {filename}: {e}")
    logger.info(f"Total chunks loaded: {len(documents_chunks)}")
    return documents_chunks