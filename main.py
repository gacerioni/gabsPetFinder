import uvicorn
from fastapi import FastAPI
from app.routes import pet  # Import the pet router
from app.utils.logger import logger  # Import the logger
from app.config.config import Settings  # Import settings (e.g., for environment-specific configs)


# Define lifespan for startup and shutdown actions
async def app_lifespan(app: FastAPI):
    """
    Lifespan function to handle startup and shutdown.
    """
    logger.info("Starting up the Pet Finder API...")
    try:
        # Perform startup actions here
        logger.info("Initializing Redis connection...")
        logger.info("Verifying S3 bucket access...")
        # Example: Connect to Redis, preload data, etc.

        yield  # The app is now running!

    finally:
        # Perform shutdown actions here
        logger.info("Shutting down the Pet Finder API...")
        # Example: Close Redis connections, cleanup resources, etc.


# Create the FastAPI app and pass the lifespan function
app = FastAPI(
    title="Pet Finder API",
    description="API for registering and finding lost pets using embeddings and metadata",
    version="1.0.0",
    contact={
        "name": "Gabriel Cerioni",
        "url": "https://github.com/gacerioni",
        "email": "gabriel.cerioni@redis.com",
    },
    docs_url="/docs",  # Swagger UI documentation
    redoc_url="/redoc",  # ReDoc documentation
    lifespan=app_lifespan,  # Use lifespan for startup/shutdown
)


# Include the pet router
app.include_router(pet.router, prefix="/pets", tags=["Pets"])


# Define the entry point to run the server
if __name__ == "__main__":
    settings = Settings()  # Load settings (e.g., environment variables)
    logger.info("Starting the API with the following configuration:")
    logger.info(f"Host: {settings.host}, Port: {settings.port}")
    logger.info(f"Reload: {settings.reload}")

    # Run the FastAPI server with Uvicorn
    uvicorn.run(
        "main:app",  # Path to the app instance
        host=settings.host,  # 0.0.0.0 to make the app accessible externally
        port=settings.port,  # Port number
        reload=settings.reload,  # Enable hot reload in development
    )