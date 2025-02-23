FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the project files into the container
COPY src /app/
COPY requirements.txt /app/
COPY .env /app/.env 

# Install dependencies from requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Expose the port that the FastAPI app runs on
EXPOSE 8001

# Command to run the application
CMD ["uvicorn", "retrieval_agent.main:app", "--host", "0.0.0.0", "--port", "8001"]
