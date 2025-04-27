FROM python:3.9-slim

WORKDIR /app

# Upgrade pip to the latest version
RUN pip install --no-cache-dir --upgrade pip

# Install system dependencies required for some Python packages
RUN apt-get update && \
    apt-get install -y \
        tesseract-ocr \
        poppler-utils \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies from requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]