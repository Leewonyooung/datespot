FROM python:3.12-slim

# Set the working directory
WORKDIR /fastapi

# Copy the application folder
COPY ./app ./app

# Set the working directory for the app
WORKDIR /fastapi/app

# Install dependencies
COPY ./app/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 6003

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "6003"]
