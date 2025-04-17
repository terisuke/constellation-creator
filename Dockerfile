# Build stage for Frontend
FROM node:18 AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Build stage for Backend
FROM python:3.11-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
  libgl1-mesa-glx \
  libglib2.0-0 \
  && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

# Create necessary directories
RUN mkdir -p static/assets

# Copy frontend build from frontend-builder
COPY --from=frontend-builder /app/frontend/dist/index.html ./static/
COPY --from=frontend-builder /app/frontend/dist/assets ./static/assets/

# Set environment variables
ENV PYTHONPATH=/app
ENV PORT=8080

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"] 