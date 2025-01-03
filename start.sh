#!/bin/bash

# Start FastAPI in the background
uvicorn main:app --host 0.0.0.0 --port 8000 &

# Start Streamlit for the frontend
streamlit run app/frontend/main.py --server.port 8501 --server.enableCORS false --server.address 0.0.0.0