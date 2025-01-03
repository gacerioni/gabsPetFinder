import streamlit as st
import requests
import json

# API base URL (update with your FastAPI host if deployed)
API_BASE_URL = "http://localhost:8000"

# Sidebar Navigation
st.sidebar.title("Pet Finder")
option = st.sidebar.radio("Navigation", ["Landing Page", "Register Pet", "Find Pet"])

# Landing Page
if option == "Landing Page":
    st.title("Welcome to Pet Finder")
    st.write("Redis-powered Pet Finder using vector embeddings. Recognize your pets or register new ones!")
    st.image("https://your-logo-url.com/logo.png", use_container_width=True)  # Replace with your logo

# Register Pet
elif option == "Register Pet":
    st.title("Register Your Pet")
    pet_name = st.text_input("Name")
    species = st.selectbox("Species", ["Dog", "Cat", "Other"])
    breed = st.text_input("Breed")
    color = st.text_input("Color")
    age = st.number_input("Age", min_value=0, step=1)
    owner_name = st.text_input("Owner's Name")
    owner_contact = st.text_input("Owner's Contact")
    last_known_location = st.text_input("Last Known Location (longitude,latitude)")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])

    pet_image = st.file_uploader("Upload Pet Image", type=["jpg", "jpeg", "png"])

    if st.button("Register Pet"):
        if pet_name and species and breed and pet_image:
            # Prepare file and data
            files = {"file": pet_image.read()}  # Read the file as binary
            pet_metadata = {
                "name": pet_name,
                "species": species,
                "breed": breed,
                "color": color,
                "age": age,
                "owner_name": owner_name,
                "owner_contact": owner_contact,
                "last_known_location": last_known_location,
                "gender": gender,
            }
            # Send request to backend
            response = requests.post(
                f"{API_BASE_URL}/pets/register/",
                files=files,
                data={"pet_metadata": json.dumps(pet_metadata)},  # Convert metadata to JSON string
            )
            if response.status_code == 200:
                st.success("Pet registered successfully!")
            else:
                st.error(f"Failed to register pet. Error: {response.text}")
        else:
            st.warning("Please fill in all required fields and upload an image.")

# Find Pet
# Find Pet
elif option == "Find Pet":
    st.title("Find Your Pet")
    pet_image = st.file_uploader("Upload Image to Find", type=["jpg", "jpeg", "png"])
    num_results = st.slider("Number of Similar Pets to Show", min_value=1, max_value=10, value=3)  # Configurable top K

    st.write(f"Slider value for 'num_results': {num_results}")  # Debug: Show slider value in the UI

    if st.button("Find Pet"):
        if pet_image:
            # Send request to backend
            files = {"file": pet_image.read()}  # Read the file as binary
            response = requests.post(
                f"{API_BASE_URL}/pets/find/",
                files=files,
                params={"num_results": num_results},  # Pass num_results as query parameter
            )
            if response.status_code == 200:
                results = response.json()
                if isinstance(results, list) and len(results) > 0:
                    st.success(f"🎉 Found {len(results)} similar pets:")
                    for result in results:
                        st.image(result["image_url"],
                                 caption=f"{result.get('name', 'Unknown')} ({result.get('species', 'Unknown')})",
                                 use_container_width=True)
                        st.markdown("### Owner Details")
                        st.write(f"**Name:** {result.get('owner_name', 'Unknown')}")
                        st.write(f"**Contact:** {result.get('owner_contact', 'Unknown')}")

                        st.markdown("### Pet Details")
                        st.write(f"**Breed:** {result.get('breed', 'Unknown')}")
                        st.write(f"**Color:** {result.get('color', 'Unknown')}")
                        st.write(f"**Age:** {result.get('age', 'Unknown')} years old")
                        st.write(f"**Gender:** {result.get('gender', 'Unknown')}")
                        st.markdown("---")
                else:
                    st.warning("No matches found.")
            else:
                st.error(f"Error: {response.text}")
        else:
            st.warning("Please upload an image to search for your pet.")