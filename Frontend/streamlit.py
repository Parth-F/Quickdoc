import streamlit as st
import requests
import json
import os
import socket

# Get local IP address
def get_local_ip():
    return socket.gethostbyname(socket.gethostname())

# Get backend URL from environment variable with a default fallback
# In production, this should be set to the internal API URL
BACKEND_URL = os.environ.get("BACKEND_URL", f"http://{get_local_ip()}:5000")
print(f"Connecting to backend at: {BACKEND_URL}")

# st.title("Chatbot with Custom LLM")

st.title("QuickDoc AI: Medical Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Thanks for getting in touch with Astor today! 😊 We are here to help you build your wellness so that you are healthy today and tomorrow."}
    ]

# Mode selection (similar to how the React app uses localStorage)
# In React: mode === '0' or not set means Flagship/FineTune
# Here we'll use index=0 to match that default behavior
mode_options = ["Flagship (FineTune)", "Augmented (RAG)"]
mode = st.sidebar.radio(
    "Choose LLM Mode",
    mode_options,
    index=0
)

# Store selected mode in session state (mimicking localStorage behavior)
if "selected_mode" not in st.session_state:
    st.session_state.selected_mode = mode
else:
    st.session_state.selected_mode = mode

# GCP bucket explorer
st.sidebar.markdown("## GCP Bucket Explorer")
bucket_name = st.sidebar.text_input("Enter Bucket Name:")
if st.sidebar.button("List Files") and bucket_name:
    try:
        # Initialize GCP storage client
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blobs = bucket.list_blobs()
        
        # Display files in the bucket
        st.sidebar.markdown("### Files in Bucket:")
        for blob in blobs:
            st.sidebar.text(blob.name)
    except Exception as e:
        st.sidebar.error(f"Error accessing bucket: {str(e)}")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask a medical question..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response with a placeholder while waiting
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        
        try:
            # Determine which endpoint to use based on mode (matching React logic)
            useFineTuneModel = mode == mode_options[0]  # True if Flagship/FineTune
            endpoint = "queryFineTune" if useFineTuneModel else "queryRAG"
            
            # Log the request details for debugging
            request_url = f"{BACKEND_URL}/api/{endpoint}"
            st.write(f"Connecting to: {request_url}")
            
            # Make the API request to the backend (matching React payload structure)
            response = requests.post(
                request_url,
                json={"query_text": prompt},
                timeout=60
            )
            
            if response.status_code == 200:
                assistant_response = response.json().get("response", "Sorry, I couldn't generate a response.")
                
                # Remove debug info
                st.experimental_rerun()
                
                # Update the placeholder with the actual response
                message_placeholder.markdown(assistant_response)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            else:
                error_msg = f"Error: Received status code {response.status_code} from the server."
                message_placeholder.markdown(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                
        except Exception as e:
            error_msg = f"Error connecting to the server: {str(e)}"
            message_placeholder.markdown(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Add a button to clear chat history (equivalent to React's component remount behavior)
if st.sidebar.button("New Chat"):
    st.session_state.messages = [
        {"role": "assistant", "content": "Thanks for getting in touch with Astor today! 😊 We are here to help you build your wellness so that you are healthy today and tomorrow."}
    ]
    st.experimental_rerun()

# Add information about the chatbot in the sidebar
st.sidebar.markdown("## About Astor AI")
st.sidebar.markdown("Astor AI is a medical chatbot designed to provide reliable answers to health-related questions.")
st.sidebar.markdown("### Features:")
st.sidebar.markdown("- Medical Information")
st.sidebar.markdown("- Real-Time Responses")
st.sidebar.markdown("- User-Friendly Interface")

# This is needed for the app to work with Google Cloud Run
if __name__ == "__main__":
    # Get the port from the environment variable or use a default
    port = int(os.environ.get("PORT", 8080))
    # Note: We don't use this directly as Streamlit manages its own server
    # but it's good practice to acknowledge the PORT environment variable 