FROM python:3.11-slim

WORKDIR /app

# System deps (Pillow needs a few libs sometimes; this is a safe minimal set)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libjpeg62-turbo \
    zlib1g \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY tests ./tests

# Run the consumer
CMD ["python", "-m", "app.consumer"]