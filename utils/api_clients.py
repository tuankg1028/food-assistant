"""API client initialization and management."""

import os
import streamlit as st
from openai import OpenAI
from tavily import TavilyClient

def initialize_clients(tavily_api_key, openai_api_key):
    """Initialize API clients with error handling."""
    tavily_client = None
    openai_client = None

    try:
        if tavily_api_key:
            tavily_client = TavilyClient(api_key=tavily_api_key)
        if openai_api_key:
            openai_client = OpenAI(api_key=openai_api_key)
    except Exception as e:
        st.error(f"Error initializing API clients: {e}")

    return tavily_client, openai_client

def test_api_keys(openai_key=None, tavily_key=None, jina_key=None):
    """Test API keys and update environment variables if valid."""
    try:
        if openai_key:
            OpenAI(api_key=openai_key)  # Test the key
            os.environ["OPENAI_API_KEY"] = openai_key
            st.success("OpenAI API key updated!")
            
        if tavily_key:
            TavilyClient(api_key=tavily_key)  # Test the key
            os.environ["TAVILY_API_KEY"] = tavily_key
            st.success("Tavily API key updated!")
            
        if jina_key:
            os.environ["JINA_API_KEY"] = jina_key
            st.success("Jina AI API key updated!")
            
        return True
    except Exception as e:
        st.error(f"Invalid API key: {e}")
        return False
