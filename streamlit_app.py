import streamlit as st
import requests
import json

# Set page configuration
st.set_page_config(page_title="RAG Chatbot", layout="wide")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Debug mode to see full API response
DEBUG_MODE = True

def query_langflow(prompt):
    """Send query to Langflow API"""
    try:
        # Get the base URL and auth token from secrets
        base_url = st.secrets["LANGFLOW_URL"]
        auth_token = st.secrets["LANGFLOW_AUTH"]
        
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "input_value": prompt,
            "output_type": "chat",
            "input_type": "chat"
        }
        
        # Construct the full API URL
        api_url = f"{base_url}/run/3774f27b-92cd-4e44-99b7-c197b469357f"
        
        if DEBUG_MODE:
            st.write("Debug - API URL:", api_url)
            st.write("Debug - Headers:", {k: v for k, v in headers.items() if k != "Authorization"})
            st.write("Debug - Payload:", payload)
        
        response = requests.post(
            api_url,
            json=payload,
            headers=headers
        )
        
        if DEBUG_MODE:
            st.write("Debug - Status Code:", response.status_code)
            try:
                st.write("Debug - Response:", response.json())
            except:
                st.write("Debug - Raw Response:", response.text)
        
        if response.status_code == 200:
            result = response.json()
            return result.get('response', result.get('output', str(result)))
        else:
            return f"Error: API returned status code {response.status_code}. Response: {response.text}"
            
    except Exception as e:
        return f"Error: {str(e)}"

# Create the main application
st.title("RAG Chatbot")

# Optional: Add a debug toggle
DEBUG_MODE = st.sidebar.checkbox("Debug Mode", value=False)

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
