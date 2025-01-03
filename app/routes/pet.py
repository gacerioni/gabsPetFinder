from fastapi import APIRouter, File, UploadFile, Form, Query
import os
import json
from app.services.pet_service import register_pet, find_pet

router = APIRouter()

@router.post("/register/")
def register_pet_endpoint(
    file: UploadFile = File(...),
    pet_metadata: str = Form(...)  # Accept metadata as a string from multipart form
):
    try:
        # Parse pet_metadata JSON
        pet_metadata_dict = json.loads(pet_metadata)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON in pet_metadata"}

    # Ensure the directory exists
    upload_dir = "./query_images"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)  # Create the directory if it doesn't exist

    # Save the uploaded file
    image_path = os.path.join(upload_dir, file.filename)
    with open(image_path, "wb") as f:
        f.write(file.file.read())

    # Register the pet using the image and metadata
    success = register_pet(image_path, pet_metadata_dict)
    return {"success": success}

@router.post("/find/")
def find_pet_endpoint(
    file: UploadFile = File(...),
    num_results: int = Query(1)  # Default to 1 if not provided
):
    # Ensure the directory exists
    upload_dir = "./query_images"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)  # Create the directory if it doesn't exist

    # Save the uploaded file
    image_path = os.path.join(upload_dir, file.filename)
    with open(image_path, "wb") as f:
        f.write(file.file.read())

    # Find the pet using the image
    result = find_pet(image_path, num_results=num_results)
    return result or {"message": "No match found"}