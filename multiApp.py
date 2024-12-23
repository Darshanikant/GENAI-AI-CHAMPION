import os
import base64
import streamlit as st
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Set up Gemini API key from environment variable
api_key = os.getenv("AIzaSyA8KpggPAGA9VRHIMebBEvsZOD5pgMDguk")

# Function to encode the local image as base64
def get_base64_of_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Encode your local image
background_image_path = "background.jpg"
base64_image = get_base64_of_image(background_image_path)

# Add custom CSS to make the UI visually appealing and add background image
st.markdown(f"""
    <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{base64_image}");
            background-size: cover;
            
            background-position: center center;
            background-attachment: fixed;
        }}
        .stButton button {{
            background-color: green;
            color: white;
            font-size: 16px;
            border-radius: 8px;
            padding: 10px 20px;
            transition: background-color 0.3s ease;
        }}
        
        .stTextInput input {{
            border-radius: 8px;
            padding: 12px;
            border: 1px solid #ddd;
        }}
        .stTextInput input:focus {{
            border-color: #FF5733;
        }}
        .header {{
            text-align: center;
            color: white;
            font-size: 36px;
            margin-bottom: 20px;
            font-weight: bold;
        }}
        .subheader {{
            font-size: 24px;
            color: white;
            text-align: center;
            margin-bottom: 40px;
        }}
        .image-container {{
            margin-bottom: 20px;
            border-radius: 8px;
        }}
        .footer {{
            text-align: center;
            font-size: 14px;
            color: white;
            padding: 20px;
            margin-top: 40px;
        }}
    </style>
""", unsafe_allow_html=True)

# Sidebar for choosing the model with emojis
option = st.sidebar.radio("Choose Mode", ("🏠 Home", "💬 Text-2-Text Chat", "🖼️ Image-2-Text Chat"))

# Add Application Details in Sidebar with emojis
st.sidebar.markdown("""
    ## Gemini AI Chat App 🤖
    This app leverages Google's Gemini API to provide an interactive experience 
    for both **Text-based** and **Image-based** queries. You can:
    - Ask questions and chat with the AI 💬.
    - Upload images and get detailed descriptions 🖼️.
    - Enjoy a seamless experience with an intuitive design ✨.
    
    Choose one of the modes from the options and interact with the AI! 🚀
    
""")

# Function to generate response using Gemini API for Text-2-Text
def handle_text_input():
    user_input = st.session_state.user_input
    if user_input:
        # Generate model response
        response = model.generate_content(user_input)
        model_output = response.text
        st.session_state.chat_history.append({"user": user_input, "model": model_output})
        st.session_state.user_input = ""

# Function to generate response using Gemini API for Image-2-Text
def handle_image_input(input_text, image):
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    model.set_api_key(api_key)
    
    # Handle image and input text
    if input_text and image:
        response = model.generate_content([input_text, image])
    elif input_text:
        response = model.generate_content(input_text)
    elif image:
        response = model.generate_content(image)
    else:
        response = "No input or image provided."
    
    return response.text

# Default page - Home
if option == "🏠 Home":
    
    st.markdown('<div class="header">Gemini AI. Your AI Companion App 🚀</div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="subheader">
            Welcome to the Gemini Your AI Companion – Your gateway to intelligent conversations and insightful interactions with AI 🤖.
        </div>
        <div class="subheader">
            Experience the future of AI, where your queries meet innovative solutions 💡.
        </div>
    """, unsafe_allow_html=True)

# Text-2-Text Chat Mode
elif option == "💬 Text-2-Text Chat":
    
    st.markdown('<div class="header">Text💬 Chat with Gemini🤖 </div>', unsafe_allow_html=True)
    
    # Session state for storing conversation history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Initialize the model
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    model.set_api_key(api_key)

    # Display chat history (above the input box)
    for chat in st.session_state.chat_history:
        with st.container():
            col1, col2 = st.columns([1, 1])

            # User's input on the right
            with col2:
                st.markdown(f"**You:** {chat['user']}")

            # Model's response on the left
            with col1:
                if "model" in chat:
                    st.markdown(f"**Model:** {chat['model']}")

    # Input box for user text
    st.text_input("Enter your message 💬:", key="user_input", placeholder="Type your message here...", on_change=handle_text_input)
    st.write("The output may not be accurate.. recheck by your. Thank you ")
# Image-2-Text Chat Mode
elif option == "🖼️ Image-2-Text Chat":
    st.markdown('<div class="header">Visual Insights with Gemini 🖼️</div>', unsafe_allow_html=True)
    
    # File uploader for image input
    uploaded_file = st.file_uploader("Choose an image 📸...", type=["jpg", "jpeg", "png"])

    # Display uploaded image (if any)
    image = None
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image 🖼️", use_container_width =True)

    # Text input for additional context
    input_text = st.text_input("Input Prompt ✍️:", key="input")
    
    # Button to submit the input
    if st.button("Tell me about the image 🧐"):
        if input_text or image:
            response = handle_image_input(input_text, image)
            st.subheader("The Response is 📜:")
            st.write(response)
        else:
            st.warning("Please provide either a prompt or an image. 📢")

# Footer
st.markdown("""
    <div class="footer">
        Developed by Darshanikant | Powered by Gemini-2.0-flash-exp
    </div>
""", unsafe_allow_html=True)
