
# Use Python 3.9 image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask app on port 5000
EXPOSE 5000

# Run the Flask application
CMD ["python", "app.py"]
