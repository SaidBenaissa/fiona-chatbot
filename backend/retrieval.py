import logging
import time
import numpy as np
import functools
from typing import List, Dict, Any # Import List, Dict, Any
from embedding_manager import model # Assuming model is imported from embedding_manager

# Initialize logger for this module
logger = logging.getLogger(__name__)

# Adjusted MAX_CONTEXT_LENGTH to match llm_generator
DEFAULT_MAX_CONTEXT_LENGTH = 2000


# Cache query embeddings to avoid redundant computations
@functools.lru_cache(maxsize=100)
def get_query_embedding(query: str):
    return model.encode([query])

# Optimize the retrieval process
# Limit the number of documents and their size
# Add performance logging and similarity threshold
MIN_SIMILARITY_THRESHOLD = 0.1 # Adjust as needed

def search_embeddings(query: str, documents: list, embeddings: np.ndarray) -> list:
    start_time = time.time()

    query_embedding = get_query_embedding(query)
    similarities = np.dot(query_embedding, embeddings.T)
    # Get top N indices, ensure N is not greater than the number of documents
    num_docs = embeddings.shape[0]
    top_n = min(5, num_docs) # Get top 5 or fewer if less documents exist
    if top_n <= 0:
        logger.warning("No documents or embeddings available for search.")
        return []
    
    # Ensure indices are within bounds
    sorted_indices = np.argsort(similarities[0])[::-1]
    top_indices = sorted_indices[:top_n]

    results = []
    for idx in top_indices:
        score = float(similarities[0][idx]) if isinstance(similarities[0][idx], np.float32) else similarities[0][idx]
        # Apply similarity threshold
        if score < MIN_SIMILARITY_THRESHOLD:
            continue # Skip results below threshold

        if idx < len(documents):
             # Ensure metadata includes filename, provide default if missing
            metadata = documents[idx].get("metadata", {})
            if "filename" not in metadata:
                 metadata["filename"] = "Unknown"
                 
            results.append({
                "content": documents[idx]["content"][:DEFAULT_MAX_CONTEXT_LENGTH],  # Truncate content
                "metadata": metadata, # Pass potentially updated metadata
                "score": score
            })
        else:
            logger.warning(f"Index {idx} out of bounds for documents list (length {len(documents)}). Skipping.")


    elapsed_time = time.time() - start_time
    logger.info(f"Search embeddings took {elapsed_time:.2f} seconds. Found {len(results)} results above threshold {MIN_SIMILARITY_THRESHOLD}.")

    return results