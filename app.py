import streamlit as st
from streamlit_chat import message  # For chat bubbles
from chatbot import Chatbot

# Page Configuration
st.set_page_config(page_title="AI Chatbot", layout="wide")

# Title & Bot Status
st.title("🤖 SmartSupport Bot")

# Initialize Chatbot
bot = Chatbot()

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    is_user = msg["role"] == "user"
    message(msg["content"], is_user=is_user)

# User Input
user_input = st.text_input("Ask me anything:", key="input", placeholder="Type your message here...")

if user_input:
    # Store user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get AI Response
    response = bot.get_response(user_input)

    # Store bot response
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Display bot response
    message(response, is_user=False)




