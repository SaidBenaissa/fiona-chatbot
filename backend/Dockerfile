FROM python:3.9-slim

WORKDIR /app

# Install Python dependencies from requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Install poppler-utils for PDF processing
RUN apt-get update && apt-get install -y poppler-utils && apt-get clean

# Install Tesseract OCR for pytesseract
RUN apt-get update && apt-get install -y tesseract-ocr && apt-get clean

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]