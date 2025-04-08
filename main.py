import os
import streamlit as st
from dotenv import load_dotenv

# Import modules
from utils.api_clients import initialize_clients
from utils.search import search_web
from utils.response import get_gpt4o_response

# Load environment variables from .env file
load_dotenv()

# Set page configuration
st.set_page_config(page_title="Food Search Assistant", page_icon="🍔", layout="wide")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Set API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
JINA_API_KEY = os.getenv("JINA_API_KEY")

# Initialize clients
tavily_client, openai_client = initialize_clients(TAVILY_API_KEY, OPENAI_API_KEY)

# App header
st.title("🍔 Food Shopping Assistant")
st.markdown("""
Ask questions about products from these Vietnamese retailers:
- Kingfoodmart
- Bách Hóa Xanh
- Winmart
""")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Check for API keys before allowing interaction
if "messages" in st.session_state and st.chat_input and (not TAVILY_API_KEY or not tavily_client or not OPENAI_API_KEY or not openai_client):
    st.error("Please set your API keys in the sidebar to continue.")

# Get user input
if prompt := st.chat_input("Ask about food products..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Searching for information..."):
            # Search web for information
            search_results = search_web(prompt, tavily_client, openai_client, JINA_API_KEY)
            
            # Get GPT-4o streaming response
            response_stream = get_gpt4o_response(prompt, search_results, openai_client)
            
            # Process the streaming response
            response_container = st.empty()
            full_response = ""
            
            # Display the response as it streams in
            for chunk in response_stream:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    response_container.markdown(full_response + "▌")
            
            # Update with the final response (without cursor)
            response_container.markdown(full_response)
            
            # Optionally show search sources (collapsible)
            with st.expander("View Sources"):
                for i, result in enumerate(search_results.get("results", [])):
                    st.markdown(f"**Source {i+1}:** [{result.get('title')}]({result.get('url')})")
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Add sidebar with info
with st.sidebar:
    st.header("About")
    st.info("""
    This assistant searches for food products across major Vietnamese retailers.
    It uses Tavily to search the web, Jina AI to scrape real-time product details, and GPT-4o to process the information.
    """)
    
    # Add API key inputs for easier testing
    st.subheader("API Keys (for testing)")
    new_openai_key = st.text_input("OpenAI API Key", type="password")
    new_tavily_key = st.text_input("Tavily API Key", type="password")
    new_jina_key = st.text_input("Jina AI API Key", type="password")
    
    if st.button("Update API Keys"):
        try:
            from utils.api_clients import test_api_keys
            success = test_api_keys(new_openai_key, new_tavily_key, new_jina_key)
            if success:
                st.rerun()
        except Exception as e:
            st.error(f"Invalid API key: {e}")
