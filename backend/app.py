import logging
import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from document_loader import load_documents_from_directory
from embedding_manager import create_embeddings # type: ignore
from retrieval import search_embeddings # type: ignore
from llm_generator import generate_answer
from models.query_model import QueryRequest
from typing import List, Dict, Any
from langdetect import detect # type: ignore
from deep_translator import GoogleTranslator # type: ignore

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
app_embeddings: np.ndarray = np.array([])  # type: ignore # Initialize as empty numpy array

@app.on_event("startup")
async def startup_event():
    global loaded_docs, app_embeddings
    logger.info("Starting up the application...")
    # Adjust to handle the new return format from load_documents_from_directory
    raw_docs = load_documents_from_directory("documents")
    loaded_docs = [
        {"filename": filename, "content": content, "metadata": metadata}
        for filename, content, metadata in raw_docs
    ]
    # logger.info(f"Loaded documents are: {loaded_docs}") # Avoid logging potentially large content
    logger.info(f"Loaded {len(loaded_docs)} documents with metadata.")
    if not loaded_docs:
        logger.warning("No documents were loaded successfully.")
        app_embeddings = np.array([])
        return

    # Pass only content to create_embeddings if it expects List[str]
    # Or adjust create_embeddings if it expects List[Dict]
    # Assuming create_embeddings expects List[Dict] based on previous context
    app_embeddings = create_embeddings(loaded_docs)  # Expects List[Dict], returns np.ndarray, 
    if app_embeddings.size == 0 and loaded_docs:  # Check if empty despite having docs
        logger.error("Embeddings creation failed or returned empty.")
    elif app_embeddings.size > 0:
        logger.info(f"Embeddings created successfully. Shape: {app_embeddings.shape}")
    else:
        logger.info("No documents loaded, so no embeddings created.")

@app.post("/query")
async def query(request: QueryRequest) -> Dict[str, Any]:
    logger.info(f"Received query: {request.query}")

    # Detect the language of the query
    detected_language = detect(request.query)
    logger.info(f"Detected language: {detected_language}")

    # Translate the query to English if it's not already in English
    if detected_language != "en":
        translated_query = GoogleTranslator(source=detected_language, target="en").translate(request.query)
        logger.info(f"Translated query: {translated_query}")
    else:
        translated_query = request.query

    # Pass the translated query to the search_embeddings function
    results = search_embeddings(translated_query, loaded_docs, app_embeddings)
    logger.info(f"Search results: {results}")

    # Check if the result is the specific "unrelated" or error message structure
    if isinstance(results, list) and len(results) == 1 and isinstance(results[0], dict) and "answer" in results[0]:
        logger.info(f"Search returned a direct answer/error: {results[0]['answer']}")
        return results[0]
    elif not results or not isinstance(results, list):  # Handle unexpected empty or non-list results
        logger.warning(f"Search returned unexpected results: {results}")
        return {"answer": "Could not find relevant information."}

    # If related documents found (results is List[Dict[str, Any]])
    try:
        logger.info(f"Passing results to LLM for answer generation: {results}")
        answer_data = generate_answer(results, translated_query)
        logger.info(f"Generated answer data: {answer_data}")

        if isinstance(answer_data, dict) and "answer" in answer_data:
            # Translate the answer back to the original language if necessary
            if detected_language != "en":
                answer_data["answer"] = GoogleTranslator(source="en", target=detected_language).translate(answer_data["answer"])
            return answer_data
        else:
            logger.error(f"LLM generator returned unexpected format: {answer_data}")
            return {"answer": "Error generating response.", "references": []}
    except Exception as e:
        logger.error(f"Error during answer generation: {e}", exc_info=True)
        return {"answer": "An error occurred while generating the response.", "references": []}

@app.get("/")
async def root():
    return {"message": "Welcome to the Fiona Chatbot API!"}