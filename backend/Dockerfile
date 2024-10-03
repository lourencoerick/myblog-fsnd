# Use the official Python image.
FROM python:3.11-slim

# Set the working directory in the container.
WORKDIR /app

# Copy the rest of the application code.
COPY ./src /app

# Install dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on.
EXPOSE 5000

# Set environment variables if needed.
ENV FLASK_APP=src/api/api.py

# Run the Flask app (ensure it's set to use the correct app and run on 0.0.0.0 for Docker).
# CMD ["flask", "run", "--host=0.0.0.0"]
# Run the application using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "src.api.api:create_app()"]
