# Use Python runtime as parent image
FROM python:3.11.9-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY ./deepsee .

# Copy alembic.ini
COPY alembic.ini .

# Expose port
EXPOSE 8000

# Command to run uvicorn server with hot reloading
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--reload-dir", "/app"]