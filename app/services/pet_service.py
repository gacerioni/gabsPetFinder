from redisvl.query import VectorQuery
from app.services.redis_service import get_index
from app.services.s3_service import upload_to_s3
from app.services.embedding_service import generate_embedding
from app.config.config import Config
from app.utils.logger import logger
import os

def register_pet(image_path, pet_metadata):
    """Register a new pet and store the data as JSON in Redis."""
    index = get_index()  # Get the RedisVL index
    try:
        # Step 1: Upload image to S3
        s3_key = f"{pet_metadata['name']}/{os.path.basename(image_path)}"
        s3_url = upload_to_s3(image_path, s3_key)

        # Step 2: Generate embedding
        embedding = generate_embedding(image_path)
        if embedding is None:
            raise ValueError("Failed to generate embedding.")

        # Step 3: Add S3 URL and embedding to pet metadata
        pet_metadata["image_url"] = s3_url
        pet_metadata["embedding"] = embedding.tolist()  # Convert embedding to a list for JSON
        pet_metadata["found_status"] = "false"  # Default to "not found"

        # Step 4: Insert pet metadata into Redis index
        pet_doc = {
            "name": pet_metadata["name"],
            "species": pet_metadata["species"],
            "breed": pet_metadata.get("breed", None),
            "color": pet_metadata.get("color", None),
            "size": pet_metadata.get("size", None),
            "age": pet_metadata.get("age", None),
            "gender": pet_metadata.get("gender", None),
            "embedding": pet_metadata["embedding"],  # Embedding as a list
            "image_url": s3_url,
            "last_seen_location": pet_metadata.get("last_seen_location", None),
            "city": pet_metadata.get("city", None),
            "state": pet_metadata.get("state", None),
            "owner_name": pet_metadata.get("owner_name", None),
            "owner_contact": pet_metadata.get("owner_contact", None),
            "found_status": pet_metadata.get("found_status", "false"),  # Default to "false"
        }

        # Insert into RedisVL
        index.load([pet_doc])
        logger.info(f"Pet {pet_metadata['name']} registered successfully.")
        return True
    except Exception as e:
        logger.error(f"Error registering pet: {e}")
        return False


def find_pet(image_path, num_results=1):
    """Find pets by comparing an image, returning top N matches."""
    index = get_index()  # Ensure this returns a RedisVL SearchIndex object
    embedding = generate_embedding(image_path)

    if embedding is None:
        logger.error("Failed to generate embedding for the image.")
        return {"message": "Failed to generate embedding"}

    try:
        # Define a vector query with configurable num_results
        query = VectorQuery(
            vector=embedding.tolist(),  # Convert the embedding to a list
            vector_field_name="embedding",  # Redis field storing embeddings
            return_fields=[
                "name",
                "species",
                "breed",
                "color",
                "size",
                "age",
                "gender",
                "image_url",
                "last_seen_location",
                "city",
                "state",
                "owner_name",
                "owner_contact",
                "found_status",
                "vector_distance",
            ],
            num_results=num_results,  # Configurable number of results
        )

        # Perform the query
        results = index.query(query)

        if results:
            logger.info(f"Found {len(results)} match(es).")
            return results  # Return the top N matches
        else:
            logger.info("No match found in the database.")
            return {"message": "No match found"}
    except Exception as e:
        logger.error(f"Error finding pet: {e}")
        return {"message": f"Error finding pet: {e}"}