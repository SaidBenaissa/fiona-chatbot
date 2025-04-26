import os
from typing import List, Dict, Any

def load_documents() -> List[Dict[str, Any]]:
    documents = []
    base_path = "./documents"
    if not os.path.exists(base_path) or not os.listdir(base_path):
        print("Warning: No documents found in the documents directory or directory doesn't exist.")
        return []
    for filename in os.listdir(base_path):
        file_path = os.path.join(base_path, filename)
        if os.path.isfile(file_path):
            try:
                with open(file_path, "r", encoding='utf-8') as file:
                    documents.append({"content": file.read(), "source": filename})
            except Exception as e:
                print(f"Error reading file {filename}: {e}")
    return documents