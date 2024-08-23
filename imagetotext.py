import streamlit as st
import base64
import requests
import io
from PIL import Image

# Function to convert a local video file to base64
def convert_video_to_base64(video_path):
    try:
        with open(video_path, "rb") as video_file:
            video_base64 = base64.b64encode(video_file.read()).decode("utf-8")
        return video_base64
    except FileNotFoundError:
        st.error(f"File not found: {video_path}")
        return None

# Provide the local path to your video file
video_path = "C:\\Users\\nandh\\Downloads\\3a1744a7071a77acf1161a0bb6bcbec2.mp4"
video_base64 = convert_video_to_base64(video_path)

if video_base64:
    # Embed the video as a full-screen background
    video_bg_html = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
    background: none;
    }}
    [data-testid="stAppViewContainer"] {{
    background: none;
    position: relative;
    z-index: 1;
    }}
    </style>
    <video autoplay loop muted playsinline
        style="position: fixed; width: 100%; height: 100%; top: 0; left: 0; object-fit: cover; z-index: -1;">
        <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
    </video>
    """
    st.markdown(video_bg_html, unsafe_allow_html=True)
else:
    st.error("Could not load video background.")

# Your Streamlit app code continues here...

# Define API URL and Authorization headers
API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
headers = {"Authorization": "Bearer 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"}

# Function to query the API and get binary response
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        if response.headers.get('Content-Type') == 'image/jpeg':
            # Handle binary image response
            return response.content
        else:
            # Handle unexpected content type
            st.error(f"Unexpected content type: {response.headers.get('Content-Type')}")
            st.write("Raw response:", response.text)
            return None
    else:
        st.error(f"Failed to generate response: {response.status_code} - {response.text}")
        return None

st.title("Welcome to NANDS Image Generator !")

# Input for text prompt
prompt = st.text_input("Enter your Imagination:")

# Create a button to generate the output
if st.button("Generate Output"):
    if prompt:
        # Query the API with the provided prompt
        response_content = query({"inputs": prompt})
        if response_content:
            try:
                # Attempt to open the response as an image
                image = Image.open(io.BytesIO(response_content))
                st.image(image, caption="Generated Image")
            except IOError:
                # Handle cases where response is not an image
                st.write("Response is not an image. Displaying raw response.")
                st.write(response_content)
    else:
        st.warning("Please enter a prompt to generate output.")
