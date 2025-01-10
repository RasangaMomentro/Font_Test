import streamlit as st
import requests

# Set page configuration
st.set_page_config(page_title="RAG Chatbot", layout="wide")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Get secrets
LANGFLOW_URL = st.secrets["LANGFLOW_URL"]  # Base URL from Python API section
LANGFLOW_AUTH = st.secrets["LANGFLOW_AUTH"]  # Your authentication token

def query_langflow(prompt):
    """Send query to Langflow API"""
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {LANGFLOW_AUTH}"
        }
        
        response = requests.post(
            f"{LANGFLOW_URL}/chat/invoke",  # Adding /chat/invoke endpoint
            json={"message": prompt},
            headers=headers
        )
        return response.json()["response"]
    except Exception as e:
        return f"Error: {str(e)}"

# Create the main application
st.title("RAG Chatbot")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to know?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get response from Langflow
    response = query_langflow(prompt)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Display assistant response
    with st.chat_message("assistant"):
        st.write(response)
