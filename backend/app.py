import logging
import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from document_loader import load_documents
from embedding_manager import create_embeddings
from retrieval import search_embeddings
from llm_generator import generate_answer
from models.query_model import QueryRequest # QueryResponse removed as we return dict
from typing import List, Dict, Any # Import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this as needed for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store documents (as dicts) and embeddings globally
loaded_docs: List[Dict[str, Any]] = []
app_embeddings: np.ndarray = np.array([]) # Initialize as empty numpy array

@app.on_event("startup")
async def startup_event():
    global loaded_docs, app_embeddings
    logger.info("Starting up the application...")
    loaded_docs = load_documents() # Now returns List[Dict[str, Any]]
    logger.info(f"Loaded {len(loaded_docs)} documents with metadata.")
    app_embeddings = create_embeddings(loaded_docs) # Expects List[Dict], returns np.ndarray
    if app_embeddings.size == 0 and loaded_docs: # Check if empty despite having docs
         logger.error("Embeddings creation failed or returned empty.")
    elif app_embeddings.size > 0:
        logger.info(f"Embeddings created successfully. Shape: {app_embeddings.shape}")
    else:
        logger.info("No documents loaded, so no embeddings created.")

# Return type is now Dict[str, Any]
@app.post("/query")
async def query(request: QueryRequest) -> Dict[str, Any]:
    logger.info(f"Received query: {request.query}")
    # Pass loaded_docs (List[Dict]) AND app_embeddings (np.ndarray)
    # search_embeddings now returns List[Dict[str, Any]]
    results = search_embeddings(request.query, loaded_docs, app_embeddings)
    logger.info(f"Search results: {results}")

    # Check if the result is the specific "unrelated" or error message structure
    # search_embeddings now returns the dict directly in case of error/unrelated
    if isinstance(results, list) and len(results) == 1 and isinstance(results[0], dict) and "answer" in results[0]:
        logger.info(f"Search returned a direct answer/error: {results[0]['answer']}")
        return results[0] # Return the dictionary directly
    elif not results or not isinstance(results, list): # Handle unexpected empty or non-list results
         logger.warning(f"Search returned unexpected results: {results}")
         return {"answer": "Could not find relevant information."}

    # If related documents found (results is List[Dict[str, Any]])
    try:
        # Pass the list of result dictionaries (results) AND the original query
        # generate_answer now returns { "answer": str, "references": List[Dict] }
        answer_data = generate_answer(results, request.query)
        logger.info(f"Generated answer data: {answer_data}")

        # Ensure the response format is correct
        if isinstance(answer_data, dict) and "answer" in answer_data:
             # Return the full dictionary including answer and references
             return answer_data
        else:
             logger.error(f"LLM generator returned unexpected format: {answer_data}")
             # Fallback response if answer generation failed or format is wrong
             # Include empty references for consistency
             return {"answer": "Error generating response.", "references": []}
    except Exception as e:
        logger.error(f"Error during answer generation: {e}", exc_info=True)
        # Fallback response on exception
        # Include empty references for consistency
        return {"answer": "An error occurred while generating the response.", "references": []}

@app.get("/")
async def root():
    return {"message": "Welcome to the Fiona Chatbot API!"}