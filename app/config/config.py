import os

from pydantic.v1 import BaseSettings


class Config:
    # Redis Configuration
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    REDIS_VL_INDEX_NAME = "pet_index"  # Name of the vector search index
    REDIS_VL_PREFIX = "pet_docs"  # Prefix for pet documents stored in Redis
    REDIS_MAX_CONNECTIONS = int(os.getenv("REDIS_MAX_CONNECTIONS", 10))  # Connection pool limit

    # Redis Search Index Schema for Pets
    REDIS_VL_SCHEMA_FILE = os.getenv(
        "REDIS_VL_SCHEMA_FILE", "../schemas/pet_schema.yaml"
    )  # Path to the YAML schema file

    # AWS S3 Configuration
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")  # Default region for AWS services
    S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "gabs-lost-pet-bucket")  # S3 bucket name
    S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY", "")  # Optional: AWS Access Key for S3
    S3_SECRET_KEY = os.getenv("S3_SECRET_KEY", "")  # Optional: AWS Secret Key for S3

    # Safe Threshold for Vector Similarity
    SAFE_THRESHOLD = float(
        os.getenv("SAFE_THRESHOLD", 0.46)
    )  # Threshold for matching vectors

    # Default Embedding Model
    DEFAULT_EMBEDDING_MODEL = os.getenv("DEFAULT_EMBEDDING_MODEL", "Facenet")

    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")  # Set the logging level (DEBUG, INFO, WARN, ERROR)

    # Other Settings
    MAX_IMAGE_SIZE_MB = float(
        os.getenv("MAX_IMAGE_SIZE_MB", 5.0)
    )  # Max upload size for pet images in MB
    ENABLE_GEOLOCATION = os.getenv("ENABLE_GEOLOCATION", "true").lower() in [
        "true",
        "1",
        "yes",
    ]  # Enable geolocation indexing for pets

class Settings(BaseSettings):
    """
    Settings class that extends Config and allows validation through Pydantic.
    Also loads environment variables as needed.
    """

    # Define attributes to allow IDE auto-completion
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    reload: bool = False

    class Config:
        env_prefix = "APP_"  # Environment variable prefix for settings
        case_sensitive = True