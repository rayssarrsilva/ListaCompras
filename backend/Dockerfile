# backend/Dockerfile
FROM python:3.12-slim

WORKDIR /app

# system deps recommended for psycopg2 binary and common libs
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
 && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage cache
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r /app/requirements.txt

# Copy backend source
COPY backend /app

# Expose port used by FastAPI
EXPOSE 8000

# Use environment variable for DB (set via docker-compose)
ENV PYTHONUNBUFFERED=1

# Dev-friendly command (auto-reload)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
