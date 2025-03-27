FROM python:3.10-alpine

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Exposing port 80
EXPOSE 80

# Command to run the application
CMD ["uvicorn", "number_classification_api:app", "--host", "0.0.0.0", "--port", "80"]