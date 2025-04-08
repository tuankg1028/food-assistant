"""Web search functionality using Tavily API."""

from asyncio import sleep
import streamlit as st
from config import ALLOWED_DOMAINS
from utils.query_enhancement import generate_enhanced_query
from utils.scraper import scrape_url_with_jina

def search_web(query, tavily_client, openai_client, jina_api_key):
    """Search the web using Tavily API with domain restrictions.
    Searches each domain separately and combines results, then scrapes detailed content."""
    all_results = {"results": []}
    
    try:
        # Generate enhanced search query
        enhanced_query = generate_enhanced_query(query, openai_client)
        st.info(f"🔎 Searching with query: '{enhanced_query}'")
        
        for domain in ALLOWED_DOMAINS:
            try:
                domain_results = tavily_client.search(
                    query=enhanced_query + f" site:{domain}",
                    max_results=3
                )
                
                # Add domain results if they don't already exist in all_results
                for result in domain_results.get("results", []):
                    if not any(r.get("url") == result.get("url") for r in all_results["results"]):
                        all_results["results"].append(result)
                
            except Exception as e:
                st.warning(f"Error searching {domain}: {e}")
                continue  # Skip this domain if there's an error
                
        # Scrape detailed content for each result using Jina AI
        with st.status("Scraping product details...", expanded=False) as status:
            for i, result in enumerate(all_results["results"]):
                status.update(label=f"Scraping details from {result.get('url', 'URL')}... ({i+1}/{len(all_results['results'])})")
                sleep(3)
                scraped_data = scrape_url_with_jina(result.get("url", ""), jina_api_key)
                
                if scraped_data.get("status") == "success" and scraped_data.get("content"):
                    # Add the scraped content to the result
                    result["scraped_content"] = scraped_data.get("content")
                else:
                    result["scraped_content"] = ""
            
            status.update(label="Finished scraping product details", state="complete")
                
        return all_results
        
    except Exception as e:
        st.error(f"Error during web search: {e}")
        return {"results": []}
