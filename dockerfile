# Use the official Python image as the base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Copy project requirements file
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . /app/

# Expose port 80 for the Gunicorn server
EXPOSE 8000

# Command to run the Gunicorn server
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
