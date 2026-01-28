FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Expose default port (apps may read $PORT from environment)
EXPOSE 8080

# Default command
CMD ["python", "main.py"]
