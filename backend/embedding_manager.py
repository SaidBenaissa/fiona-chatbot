from sentence_transformers import SentenceTransformer
import numpy as np
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

model = SentenceTransformer('all-MiniLM-L6-v2')

def create_embeddings(documents: List[Dict[str, Any]]) -> np.ndarray:
    if not documents:
        logger.warning("Warning: No documents provided for embedding creation.")
        return np.array([])
    try:
        contents = [doc['content'] for doc in documents if 'content' in doc]
        if not contents:
             logger.warning("Warning: No content found in the provided documents.")
             return np.array([])

        new_embeddings = model.encode(contents)
        logger.info(f"Created embeddings for {len(contents)} document contents. Embedding shape: {new_embeddings.shape}")
        return new_embeddings
    except Exception as e:
        logger.error(f"Error encoding documents: {e}", exc_info=True)
        return np.array([])