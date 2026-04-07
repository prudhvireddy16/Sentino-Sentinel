# 1. Use a lightweight Python image
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the requirements file first (for better caching)
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the application code
COPY . .

# 6. Expose the port FastAPI runs on
EXPOSE 8000

# 7. Command to run the API
CMD ["uvicorn", "app_api:app", "--host", "0.0.0.0", "--port", "8000"]