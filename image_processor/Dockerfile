FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY consumer.py ./

ENV BACKEND_URL=http://backend:5001/api
ENV RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/

CMD ["python", "consumer.py"]
