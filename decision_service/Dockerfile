FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y \
  curl \
  && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app ./app

# Expose port
EXPOSE 8002

# Run service
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]
