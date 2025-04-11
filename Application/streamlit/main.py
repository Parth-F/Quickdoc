import streamlit as st
import requests
import json
import os

# Get backend URL from environment variable with a default fallback
BACKEND_URL = os.environ.get("BACKEND_URL", "http://backend:5000")

# st.title("Chatbot with Custom LLM")

st.title("QuickDoc AI: Medical Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Thanks for getting in touch with Astor today! 😊 We are here to help you build your wellness so that you are healthy today and tomorrow."}
    ]

# Mode selection (similar to the mode stored in localStorage in the React app)
mode = st.sidebar.radio(
    "Choose LLM Mode",
    ["Flagship (FineTune)", "Augmented (RAG)"],
    index=0
)

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
    #     stream = client.chat.completions.create(
    #         model=st.session_state["openai_model"],
    #         messages=[
    #             {"role": m["role"], "content": m["content"]}
    #             for m in st.session_state.messages
    #         ],
    #         stream=True,
    #     )
    #     response = st.write_stream(stream)
    # st.session_state.messages.append({"role": "assistant", "content": response})
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        
        try:
            # Determine which endpoint to use based on mode
            endpoint = "queryFineTune" if mode == "Flagship (FineTune)" else "queryRAG"
            
            # Make the API request to the backend using the environment variable
            response = requests.post(
                f"{BACKEND_URL}/{endpoint}",
                json={"query_text": prompt},
                timeout=60
            )
            
            if response.status_code == 200:
                assistant_response = response.json().get("response", "Sorry, I couldn't generate a response.")
                
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

# Add a button to clear chat history
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
