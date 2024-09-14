import streamlit as st
import openai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_response(prompt, model):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return str(e)

def render_latex(text):
    # This function would handle LaTeX rendering if needed
    st.markdown(text)

def chat_page():
    st.set_page_config(layout="wide")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("AI Assistant와의 대화")
    with col2:
        st.image("https://via.placeholder.com/100", width=100)  # Placeholder for profile image
    
    st.write("AI Assistant와 대화를 나누어보세요.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({"role": "assistant", "type": "text", "content": "안녕하세요! 어떤 도움이 필요하신가요?"})

    model = st.selectbox("모델 선택", ["gpt-3.5-turbo", "gpt-4"])
    
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                if message["type"] == "text":
                    render_latex(message["content"])
    
    if prompt := st.chat_input("메시지를 입력하세요"):
        st.session_state.messages.append({"role": "user", "type": "text", "content": prompt})
        with st.chat_message("user"):
            render_latex(prompt)
        
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = generate_response(prompt, model)
            message_placeholder.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "type": "text", "content": full_response})
        
        st.experimental_rerun()

if __name__ == "__main__":
    chat_page()
