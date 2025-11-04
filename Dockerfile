# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all project files into container
COPY . .

# Install dependencies from main folder
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 5000

# Move into backend folder to run app
WORKDIR /app/backend

# Run the Flask application
CMD ["python", "app.py"]
