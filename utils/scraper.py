"""Web scraping utilities."""

import requests
import streamlit as st

def scrape_url_with_jina(url, jina_api_key):
    """Scrape content from a URL using Jina AI API"""
    try:
        if not jina_api_key:
            return {"error": "Jina API key not set", "content": ""}
            
        headers = {
            'Authorization': f'Bearer {jina_api_key}',
            'X-Retain-Images': 'none',
            'X-Return-Format': 'text',
        }
        
        response = requests.get(f"https://r.jina.ai/{url}", headers=headers, timeout=20)

        if response.status_code == 200:
            return {
                "status": "success",
                "content": response.text
            }
        else:
            return {
                "status": "error",
                "error": f"HTTP error {response.status_code}",
                "content": ""
            }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "content": ""
        }
