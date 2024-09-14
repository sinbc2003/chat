import streamlit as st
import openai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return str(e)

# Custom CSS to push content to the top and input to the bottom
st.markdown("""
    <style>
        .reportview-container {
            flex-direction: column-reverse;
        }
        .main .block-container {
            padding-top: 1rem;
            padding-bottom: 10rem;
            max-width: 46rem;
        }
        .stTextInput {
            position: fixed;
            bottom: 3rem;
            left: 0;
            right: 0;
            background-color: white;
            padding: 1rem;
            z-index: 1000;
        }
        .stButton {
            position: fixed;
            bottom: 0.5rem;
            right: 1rem;
            z-index: 1001;
        }
    </style>
""", unsafe_allow_html=True)

st.title("GPT-3.5 Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a container for the chat history
chat_container = st.container()

# Create a container for the input field and button
input_container = st.container()

# Use the input container for the text input and button
with input_container:
    prompt = st.text_input("What is your question?", key="user_input")
    send_button = st.button("Send")

# React to user input
if send_button and prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Generate response
    response = generate_response(prompt)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Clear the input box after sending
    st.session_state.user_input = ""

# Display updated chat history
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Force a rerun to update the chat history display
st.experimental_rerun()
