import streamlit as st
import requests
import json

# Set page configuration
st.set_page_config(page_title="RAG Chatbot", layout="wide")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Get secrets
LANGFLOW_URL = st.secrets["LANGFLOW_URL"]
LANGFLOW_AUTH = st.secrets["LANGFLOW_AUTH"]

def query_langflow(prompt):
    """Send query to Langflow API"""
    try:
        headers = {
            "Authorization": f"Bearer {LANGFLOW_AUTH}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "input_value": prompt,
            "output_type": "chat",
            "input_type": "chat",
            "tweaks": {
                "ChatInput-GttX2": {},
                "ParseData-pfCjl": {},
                "Prompt-oucXx": {},
                "SplitText-NN9ME": {},
                "OpenAIModel-dTpgs": {},
                "ChatOutput-ZJqT4": {},
                "AstraDB-By7mp": {},
                "OpenAIEmbeddings-CHR7f": {},
                "AstraDB-qMCWK": {},
                "OpenAIEmbeddings-1b1YB": {},
                "File-ziFHP": {}
            }
        }
        
        response = requests.post(
            f"{LANGFLOW_URL}/run/3774f27b-92cd-4e44-99b7-c197b469357f",  # Using your FLOW_ID
            json=payload,
            headers=headers
        )
        
        if response.status_code == 200:
            result = response.json()
            # Handle the response based on the actual structure
            if isinstance(result, dict):
                return result.get('response', result.get('output', str(result)))
            return str(result)
        else:
            return f"Error: API returned status code {response.status_code}"
            
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
    
