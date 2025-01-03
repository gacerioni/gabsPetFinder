import os
import random
from faker import Faker
from app.services.pet_service import register_pet
from app.utils.logger import logger

# Initialize Faker for generating fake data
fake = Faker()

# Folder containing the pet images
IMAGE_FOLDER = "../../query_images/stanford_pet_images"

# Configurable constant to limit the number of images processed per folder
MAX_IMAGES_PER_FOLDER = 10


def generate_pet_metadata(breed, image_name):
    """Generate fake metadata for a pet."""
    species = "Dog" if "dog" in breed.lower() else "Cat"
    color = random.choice(["Brown", "Black", "White", "Golden", "Gray", "Spotted"])
    size = random.choice(["Small", "Medium", "Large"])
    age = random.randint(1, 15)  # Age in years
    gender = random.choice(["Male", "Female"])
    last_seen_location = f"{random.uniform(-180, 180):.6f},{random.uniform(-90, 90):.6f}"  # Random lat/lon
    city = fake.city()
    state = fake.state()
    owner_name = fake.name()
    owner_contact = fake.email()

    return {
        "name": image_name.split(".")[0],  # Use the file name (without extension) as the pet name
        "species": species,
        "breed": breed.replace("_", " ").capitalize(),  # Replace underscores with spaces for better readability
        "color": color,
        "size": size,
        "age": age,
        "gender": gender,
        "last_seen_location": last_seen_location,
        "city": city,
        "state": state,
        "owner_name": owner_name,
        "owner_contact": owner_contact,
        "found_status": "false",  # Default to "not found"
    }


def populate_redis_from_folder():
    """Iterate through the folder structure and populate Redis with fake pet data."""
    for breed_folder in os.listdir(IMAGE_FOLDER):
        breed_path = os.path.join(IMAGE_FOLDER, breed_folder)
        if os.path.isdir(breed_path):
            # Breed name is derived from the folder name
            breed_name = breed_folder.split("-")[-1]  # Extract the breed name

            # Get all .jpg files in the folder
            image_files = [f for f in os.listdir(breed_path) if f.endswith(".jpg")]

            # Shuffle the images to pick random ones
            random.shuffle(image_files)

            # Process up to MAX_IMAGES_PER_FOLDER images
            for image_file in image_files[:MAX_IMAGES_PER_FOLDER]:
                image_path = os.path.join(breed_path, image_file)

                # Generate fake metadata for the pet
                pet_metadata = generate_pet_metadata(breed_name, image_file)

                # Register the pet in Redis
                success = register_pet(image_path, pet_metadata)
                if success:
                    logger.info(f"Successfully added {pet_metadata['name']} to Redis.")
                else:
                    logger.error(f"Failed to add {pet_metadata['name']} to Redis.")


if __name__ == "__main__":
    logger.info("Starting to populate Redis with fake pet data...")
    populate_redis_from_folder()
    logger.info("Finished populating Redis.")