# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the application files to the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir flask

# Expose the port Flask runs on
EXPOSE 5000

# Define the environment variable to disable Flask debug mode in production
ENV FLASK_ENV=production

# Command to run the Flask app
CMD ["python", "app.py"]

