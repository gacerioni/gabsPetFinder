import boto3
from botocore.exceptions import NoCredentialsError
from app.config.config import Config
from app.utils.logger import logger

s3_client = boto3.client("s3", region_name=Config.AWS_REGION)

def upload_to_s3(file_path, s3_key):
    """Upload a file to S3."""
    try:
        s3_client.upload_file(file_path, Config.S3_BUCKET_NAME, s3_key)
        s3_url = f"https://{Config.S3_BUCKET_NAME}.s3.{Config.AWS_REGION}.amazonaws.com/{s3_key}"
        logger.info(f"Uploaded to S3: {s3_url}")
        return s3_url
    except NoCredentialsError:
        logger.error("AWS credentials not found.")
        raise
    except Exception as e:
        logger.error(f"Error uploading to S3: {e}")
        raise