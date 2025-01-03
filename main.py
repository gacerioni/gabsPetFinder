import uvicorn
from fastapi import FastAPI
from app.routers import pet  # Import the pet router
from app.utils.logger import logger  # Import the logger
from app.config.settings import Settings  # Import settings (e.g., for environment-specific configs)

# Create an instance of FastAPI
app = FastAPI(
    title="Pet Finder API",
    description="API for registering and finding lost pets using embeddings and metadata",
    version="1.0.0",
    contact={
        "name": "Your Name",
        "url": "https://github.com/your-repo",
        "email": "youremail@example.com",
    },
    docs_url="/docs",  # Swagger UI documentation
    redoc_url="/redoc",  # ReDoc documentation
)

# Include the pet router
app.include_router(pet.router, prefix="/pets", tags=["Pets"])


@app.on_event("startup")
async def startup_event():
    """
    Actions to perform when the application starts.
    For example, verify external services or pre-load models.
    """
    logger.info("Starting up the Pet Finder API...")
    # Add any startup-specific initialization here
    # For example: Connect to Redis, Verify S3 bucket access, etc.


@app.on_event("shutdown")
async def shutdown_event():
    """
    Actions to perform when the application shuts down.
    For example, close DB connections, disconnect from services.
    """
    logger.info("Shutting down the Pet Finder API...")


# Define the entry point to run the server
if __name__ == "__main__":
    settings = Settings()  # Load settings (e.g., environment variables)
    logger.info("Starting the API with the following configuration:")
    logger.info(f"Host: {settings.host}, Port: {settings.port}")
    logger.info(f"Debug: {settings.debug}, Reload: {settings.reload}")

    # Run the FastAPI server with Uvicorn
    uvicorn.run(
        "main:app",  # Path to the app instance
        host=settings.host,  # 0.0.0.0 to make the app accessible externally
        port=settings.port,  # Port number
        reload=settings.reload,  # Enable hot reload in development
        debug=settings.debug,  # Enable debug mode
    )