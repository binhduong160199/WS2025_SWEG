FROM python:3.11-slim

WORKDIR /app

ENV OMP_NUM_THREADS=1
ENV MKL_NUM_THREADS=1
ENV PYTORCH_NUM_THREADS=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir torch==2.1.2 --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY tests ./tests

CMD ["python", "-m", "app.consumer"]