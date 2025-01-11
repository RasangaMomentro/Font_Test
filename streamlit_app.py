import streamlit as st
import requests
import json

# Set page configuration
st.set_page_config(page_title="RAG Chatbot", layout="wide")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

def extract_chat_response(response_data):
    """Extract the actual chat message from the nested response structure"""
    try:
        # Navigate through the nested structure
        outputs = response_data.get('outputs', [{}])[0]
        outputs_nested = outputs.get('outputs', [{}])[0]
        results = outputs_nested.get('results', {})
        message = results.get('message', {})
        text = message.get('data', {}).get('text', '')
        
        return text if text else "No response text found"
    except Exception as e:
        return f"Error parsing response: {str(e)}"

def query_langflow(prompt):
    """Send query to Langflow API"""
    try:
        # Constants from your API
        base_url = "https://api.langflow.astra.datastax.com"
        langflow_id = "34d17c26-a986-4b87-a228-81e15a1ecc86"
        flow_id = "3774f27b-92cd-4e44-99b7-c197b469357f"
        
        # Construct API URL exactly as shown in template
        api_url = f"{base_url}/lf/{langflow_id}/api/v1/run/{flow_id}"
        
        # Headers
        headers = {
            "Authorization": f"Bearer {st.secrets['LANGFLOW_AUTH']}",
            "Content-Type": "application/json"
        }
        
        # Payload structure matching the template
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
        
        # Make the request
        response = requests.post(api_url, json=payload, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            # Extract just the chat message text
            return extract_chat_response(result)
        else:
            error_detail = f"Status code: {response.status_code}"
            try:
                error_detail += f"\nResponse: {response.json()}"
            except:
                error_detail += f"\nResponse: {response.text}"
            return f"Error: {error_detail}"
            
    except Exception as e:
        return f"Error: {str(e)}"

# Create the main application
st.title("RAG Chatbot")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])  # Using markdown for better formatting

# Chat input
if prompt := st.chat_input("What would you like to know?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get response from Langflow
    response = query_langflow(prompt)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response)
