import numpy as np
import torch
from PIL import Image
from transformers import ViTImageProcessor, ViTModel
from app.utils.logger import logger

# Load the model and image processor globally
model_name = "google/vit-base-patch16-224"
device = "cuda" if torch.cuda.is_available() else "cpu"

vit_model = ViTModel.from_pretrained(model_name).to(device)
image_processor = ViTImageProcessor.from_pretrained(model_name)
vit_model.eval()

def generate_embedding(image_path: str) -> np.ndarray:
    """
    Generate an embedding for the given image using a pretrained ViT model.

    Args:
        image_path (str): Path to the image file.

    Returns:
        np.ndarray: The embedding vector for the image.
    """
    try:
        logger.info(f"Generating embedding for {image_path} using {model_name}")

        # Load and preprocess the image
        image = Image.open(image_path).convert("RGB")
        logger.info(f"Input image size: {image.size}")  # Log original image size
        inputs = image_processor(images=image, return_tensors="pt")

        # Move inputs to device
        inputs = {key: value.to(device) for key, value in inputs.items()}

        with torch.no_grad():
            outputs = vit_model(**inputs)
            # Typically, we take the [CLS] token (index 0) from last_hidden_state
            embedding = outputs.last_hidden_state[:, 0, :]  # shape: (1, hidden_size)

        # Convert to NumPy array for compatibility with Redis or downstream tasks
        return embedding.cpu().numpy().flatten()  # Flatten to 1D vector
    except Exception as e:
        logger.error(f"Failed to generate embedding for {image_path}: {e}")
        raise ValueError(f"Embedding generation failed: {e}")

def verify_embedding_support():
    """
    Verify that ViT embedding system is functional.
    """
    try:
        test_image = "test.jpg"  # Replace with an actual test image path
        generate_embedding(test_image)
        logger.info(f"{model_name} embedding system is functional.")
    except Exception as e:
        logger.error(f"Failed to verify embedding system: {e}")

if __name__ == "__main__":
    logger.info("Testing embedding generation with a sample image from Bart (my dog)...")
    image_path = "./bart_shiba.jpg"
    embedding = generate_embedding(image_path)
    print(f"General Info:\n  Model used: {model_name}\n  Using {device} to process the embeddings")
    print(f"  Embedding Shape Dimensions: {embedding.shape}")
    print(f"Embedding: {embedding}")