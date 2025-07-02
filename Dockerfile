# Use official Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt first (for layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app
COPY main.py .

#Expose the default port
EXPOSE 5000

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]