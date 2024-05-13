# Use Python runtime as parent image
FROM python:3.11.9-slim

# Set work directory
WORKDIR /

# Copy project
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /deepsee

# Expose port
EXPOSE 8000

# Command to run uvicorn server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]