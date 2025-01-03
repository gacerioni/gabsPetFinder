from redis import Redis, ConnectionPool
from redisvl.index import SearchIndex
from app.config.config import Config
from app.utils.logger import logger
import yaml
import os

# Redis Connection Pool
pool = ConnectionPool.from_url(
    Config.REDIS_URL,
    max_connections=Config.REDIS_MAX_CONNECTIONS,
    decode_responses=True  # To decode stored data as Python types
)
redis_client = Redis(connection_pool=pool)

def load_schema_from_yaml(yaml_path: str) -> dict:
    """Load the RedisVL schema from a YAML file."""
    try:
        with open(yaml_path, "r") as f:
            schema = yaml.safe_load(f)
        logger.info(f"Schema loaded from {yaml_path}")
        return schema
    except Exception as e:
        logger.error(f"Error loading schema: {e}")
        raise e

# Load schema
schema_path = os.path.join(os.path.dirname(__file__), "../schemas/pet_schema.yaml")
schema = load_schema_from_yaml(schema_path)

# Create or retrieve RedisVL index
index = SearchIndex.from_dict(schema)
index.set_client(redis_client)
index.create(overwrite=True)

def get_index():
    return index

def get_redis_client():
    return redis_client