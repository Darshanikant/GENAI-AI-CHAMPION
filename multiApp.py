import os
import base64
import streamlit as st
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up Gemini API key
api_key = os.getenv("AIzaSyA8KpggPAGA9VRHIMebBEvsZOD5pgMDguk")

if not api_key:
    st.error("API Key not found. Please set the GEMINI_API_KEY environment variable.")
else:
    genai.configure(api_key=api_key)

# Function to encode local images as base64
def get_base64_of_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Set background image for Streamlit app
background_image_path = "background.jpg"
base64_image = get_base64_of_image(background_image_path)

st.markdown(f"""
    <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{base64_image}");
            background-size: cover;
            background-attachment: fixed;
        }}
        .footer {{
            text-align: center;
            font-size: 14px;
            color: white;
            padding: 20px;
        }}
    </style>
""", unsafe_allow_html=True)

# App sections
st.title("Gemini AI Chat App")
option = st.radio("Choose Mode", ["🏠 Home", "💬 Text Chat", "🖼️ Image Chat"])

if option == "🏠 Home":
    st.write("Welcome to the Gemini AI Chat App!")
elif option == "💬 Text Chat":
    st.write("Chat with AI below:")
    user_input = st.text_input("Enter your message:", key="user_input")
    if user_input:
        try:
            model = genai.GenerativeModel("gemini-2.0-flash-exp")
            response = model.generate_content(user_input)
            st.write(f"**AI:** {response.text}")
        except Exception as e:
            st.error(f"Error during API call: {e}")
elif option == "🖼️ Image Chat":
    st.write("Upload an image for AI insights.")
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image")
    else:
        st.warning("Please upload an image.")

st.markdown("""
    <div class="footer">
        Developed by Darshanikanta | Powered by Gemini-2.0-flash-exp
    </div>
""", unsafe_allow_html=True)
