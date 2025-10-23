# Use a Python 3.10 slim image for a smaller footprint
FROM python:3.10-slim

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY src/requirements.txt .

# Upgrade pip and install Python packages
RUN pip install --upgrade pip setuptools wheel \
    && pip install tensorflow==2.16.1 \
    && pip install scipy joblib pandas numpy scikit-learn openpyxl flask

# Copy all application code from src into the container's /app directory
COPY src/ /app/

# Add a 'serve' executable for AWS SageMaker
RUN echo '#!/bin/sh\npython serve.py' > /usr/local/bin/serve \
    && chmod +x /usr/local/bin/serve

# Expose the port specified in your serve.py
EXPOSE 8080

# Command to run your application
CMD ["python", "serve.py"]
