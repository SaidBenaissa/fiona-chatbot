# Fiona Chatbot

## Overview
Fiona Chatbot is a full-stack application that utilizes FastAPI for the backend and a React-based frontend. The application is designed to facilitate chat interactions by leveraging document embeddings and a language model to generate responses based on user queries.

## Project Structure
The project is organized into two main directories: `backend` and `frontend`.

### Backend
- **app.py**: Main FastAPI application that sets up API endpoints.
- **document_loader.py**: Loads and splits documents into manageable chunks.
- **embedding_manager.py**: Creates and manages embeddings for document chunks.
- **retrieval.py**: Implements vector-based search functionality.
- **llm_generator.py**: Generates answers using retrieved document chunks.
- **models/**: Contains Pydantic models for API requests and responses.
- **documents/**: Directory for source documents (txt/pdf/md).
- **embeddings/**: Directory for storing the saved vector database.
- **requirements.txt**: Lists backend dependencies.
- **Dockerfile**: Instructions for building the backend Docker image.

### Frontend
- **public/**: Contains static public files (favicon, index.html).
- **src/**: Contains the main application code.
  - **App.js**: Root component of the frontend application.
  - **Chat.js**: Main Chat component for handling chat interactions.
  - **api.js**: Axios API connector for communication with the backend.
  - **components/**: UI components used in the chat interface.
  - **styles/**: CSS or Tailwind configuration files.
- **package.json**: Defines the dependencies, scripts, and metadata for the React-based frontend application.
- **Dockerfile**: Instructions for building the frontend Docker image.

### Docker Compose
- **docker-compose.yml**: Orchestrates the full stack application, defining services for both the frontend and backend.

## Getting Started
1. Clone the repository:
   ```
   git clone <repository-url>
   cd fiona-chatbot
   ```

2. Set up the backend:
   - Navigate to the `backend` directory.
   - Install dependencies:
     ```
     pip install -r requirements.txt
     ```
   - Run the FastAPI application:
     ```
     uvicorn app:app --reload
     ```

3. Set up the frontend:
   - Navigate to the `frontend` directory.
   - Install dependencies:
     ```
     npm install
     ```
   - Start the frontend application:
     ```
     npm start
     ```

4. Access the application:
   - Open your browser and go to `http://localhost:3000` for the frontend.
   - The backend API will be available at `http://localhost:8000`.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.