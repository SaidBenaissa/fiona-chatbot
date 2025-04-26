from embedding_manager import model
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import logging
from typing import List, Dict, Any # Import List, Dict, Any

logger = logging.getLogger(__name__)

# Accept list of document dictionaries and embeddings_list
def search_embeddings(query: str, documents: List[Dict[str, Any]], embeddings_list: np.ndarray) -> List[Dict[str, Any]]: # Return list of dicts
    if not isinstance(embeddings_list, np.ndarray) or embeddings_list.size == 0:
        logger.error("Error: Embeddings list provided is empty or invalid.")
        # Return structure expected by app.py for error handling
        return [{"answer": "I can only answer questions related to the loaded documents.", "references": []}]

    np_embeddings = embeddings_list # Already a numpy array from embedding_manager
    if len(np_embeddings.shape) != 2:
        logger.error(f"Error: Embeddings have incorrect shape: {np_embeddings.shape}")
        return [{"answer": "Error processing embeddings.", "references": []}]

    query_embedding = model.encode([query])
    logger.info(f"Query embedding shape: {query_embedding.shape}")

    try:
        if len(query_embedding.shape) == 1:
            query_embedding = query_embedding.reshape(1, -1)

        similarities = cosine_similarity(query_embedding, np_embeddings)
        logger.info(f"Similarity scores shape: {similarities.shape}") # Log shape
    except ValueError as e:
        logger.error(f"Error calculating cosine similarity: {e}")
        logger.error(f"Query embedding shape: {query_embedding.shape}, Embeddings shape: {np_embeddings.shape}")
        return [{"answer": "Error calculating similarity.", "references": []}]

    max_similarity = np.max(similarities[0])
    logger.info(f"Max similarity: {max_similarity}")
    # Calculate a dynamic relevance threshold based on the top 10% of similarity scores
    RELEVANCE_THRESHOLD = max(0.3, np.percentile(similarities[0], 90))
    logger.info(f"Dynamic relevance threshold set to: {RELEVANCE_THRESHOLD}")

    if max_similarity < RELEVANCE_THRESHOLD:
        logger.info(f"Query is unrelated (max similarity {max_similarity:.4f} < {RELEVANCE_THRESHOLD}).")
        # Return structure expected by app.py
        return [{"answer": "I can only answer questions related to the loaded documents.", "references": []}]

    if not documents:
        logger.error("Error: Documents list is empty.")
        return [{"answer": "Error retrieving document content.", "references": []}]

    # Get top indices and their scores
    top_indices = np.argsort(similarities[0])[::-1][:5]
    top_scores = similarities[0][top_indices]
    logger.info(f"Top indices: {top_indices}, Top scores: {top_scores}")

    # Build the results with content, source, and score
    results = []
    for i, score in zip(top_indices, top_scores):
        if i < len(documents):
            doc = documents[i]
            # Correctly access nested metadata
            doc_metadata = doc.get('metadata', {})
            results.append({
                "content": doc.get('content', 'Content not found'),
                "metadata": {"source": doc_metadata.get('source', 'Unknown source')}, # Get source from nested metadata
                "score": float(score)
            })
        else:
            logger.warning(f"Index {i} out of bounds for documents list (length {len(documents)}).")

    if not results:
        logger.error("Error: No valid document indices found or documents missing content/source.")
        return [{"answer": "Error retrieving document content.", "references": []}]

    logger.info(f"Returning {len(results)} relevant document snippets with metadata.")
    return results # Return the list of dictionaries