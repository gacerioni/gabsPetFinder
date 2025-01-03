# Use the official Python 3.12 image as a base
FROM python:3.12-slim

LABEL author="Gabriel Cerioni"

# Set the working directory in the container
WORKDIR /app

# Copy the project files into the container
COPY . /app

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose necessary ports
EXPOSE 8000 8501

# Set environment variables
ENV REDIS_URL=redis://localhost:6379 \
    REDIS_VL_INDEX_NAME=pet_index \
    REDIS_VL_PREFIX=pet_docs \
    AWS_REGION=sa-east-1 \
    S3_BUCKET_NAME=gabs-lost-pet-bucket \
    SAFE_THRESHOLD=0.46 \
    DEFAULT_EMBEDDING_MODEL=Facenet \
    LOG_LEVEL=INFO

# Command to run both FastAPI and Streamlit
CMD ["sh", "start.sh"]