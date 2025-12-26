FROM pytorch/pytorch:latest

WORKDIR /app

COPY requirements.txt .

# REMOVE torch from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY tests ./tests

# Run the consumer
CMD ["python", "-m", "app.consumer"]