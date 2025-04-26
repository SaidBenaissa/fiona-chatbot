# ToDo List for Fiona Chatbot Project

## Tasks Completed
- Set up backend with FastAPI and integrated endpoints for chatbot functionality.
- Created `load_documents` function to load content from `features_of_steve.txt` and `plan_your_research_project.txt`.
- Implemented `create_embeddings` to generate embeddings for loaded documents.
- Enhanced `generate_answer` to include references to source documents in responses.
- Updated CI/CD pipeline to monitor changes in `backend/documents` and trigger rebuilds.
- Built Dockerfiles for both backend and frontend for deployment.
- Created a modern React-based frontend with a chatbot interface.
- Integrated `search_embeddings` to retrieve relevant content based on user queries.

## Tasks To Be Done
- Verify that the chatbot can handle queries in multiple European languages.
- Add more robust error handling for empty or invalid document directories.
- Improve the UI/UX of the chatbot interface for better user experience.
- Document the deployment process for Linux/Debian-based systems.
- Add integration steps for Apache2 and PHP (8.x) environments.
- Test the CI/CD pipeline to ensure it reacts correctly to document updates.
- Optimize the backend for better performance on CPU-based systems.
- Add unit tests for all critical backend and frontend components.
- Ensure compliance with GDPR and other data protection regulations.