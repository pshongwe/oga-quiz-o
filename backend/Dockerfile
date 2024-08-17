# Setup the Python environment and copy the built frontend files
FROM python:3.12-slim
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask application
COPY . /app

# Expose the port Flask is accessible on
EXPOSE 5000

# Run Gunicorn to serve Flask application
CMD ["python3", "-m", "api.v1.app"]