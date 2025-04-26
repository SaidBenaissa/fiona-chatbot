import logging
from transformers import pipeline
from typing import List, Dict, Any

# Configure logging for this module
logger = logging.getLogger(__name__)

# Use flan-t5-large which needs token to download (first time)
generator = pipeline("text2text-generation", model="google/flan-t5-large", device="cpu")

# Modify function to accept list of dictionaries and the query
def generate_answer(contexts: List[Dict[str, Any]], query: str) -> Dict[str, Any]:
    logger.info(f"Generating answer for query '{query}' based on {len(contexts)} contexts.")
    # Extract only the content for the prompt
    # Ensure context is a string, handle potential missing 'content' key
    context_texts = [ctx.get('content', '') for ctx in contexts if isinstance(ctx, dict)]
    context = "\n".join(context_texts) # Join the extracted content strings
    try:
        prompt = f"Based on the following context:\n\n{context}\n\nAnswer the question: {query}"
        logger.info(f"Sending prompt to generator: {prompt[:500]}...")
        # Increased max_length for potentially longer answers
        response = generator(prompt, max_length=250, num_return_sequences=1)
        logger.info(f"Received response from generator: {response}")

        if response and isinstance(response, list) and 'generated_text' in response[0]:
            generated_text = response[0]['generated_text']
            logger.info(f"Extracted generated text: {generated_text}")
            # Return the generated text and the original context dictionaries as references
            return {
                "answer": generated_text,
                "references": contexts # Pass the full context dicts back
            }
        else:
            logger.error(f"Generator returned unexpected response format: {response}")
            # Return original contexts even on error, so frontend might show sources
            return {"answer": "Error processing model response.", "references": contexts}
    except Exception as e:
        logger.error(f"Error during text generation: {e}", exc_info=True)
        # Return original contexts even on error
        return {"answer": "An error occurred during text generation.", "references": contexts}
