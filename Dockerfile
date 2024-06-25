# Use the official Python image as the base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory
COPY . .

# Expose the port the app runs on
EXPOSE 4000

# Set the entry point for the container
CMD ["python", "main.py"]