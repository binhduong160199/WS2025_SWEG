# Use official Python image - Updated to 3.12
FROM python:3.12-slim

# Set workdir
WORKDIR /app

# Install system dependencies for psycopg2 (for database connectivity)
RUN apt-get update && apt-get install -y build-essential libpq-dev \ 
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
# The context is expected to be the 'backend' directory.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY . .

# Expose port
EXPOSE 5001

# Set environment variables for Flask
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5001

# Entrypoint to run the Flask application
CMD ["flask", "run"]