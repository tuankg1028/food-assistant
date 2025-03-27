import os
import streamlit as st
from openai import OpenAI
from tavily import TavilyClient

# Set page configuration
st.set_page_config(page_title="Food Search Assistant", page_icon="🍔", layout="wide")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Set API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Initialize clients with better error handling
tavily_client = None
openai_client = None

try:
    if TAVILY_API_KEY:
        tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
    if OPENAI_API_KEY:
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
except Exception as e:
    st.error(f"Error initializing API clients: {e}")

# Allowed domains for search
ALLOWED_DOMAINS = [
    "https://cooponline.vn",
    "https://bachhoaxanh.com",
    "https://winmart.vn"
]

def generate_enhanced_query(user_query):
    """Use GPT to generate a more effective search query based on the user's question."""
    try:
        if not openai_client:
            return user_query
            
        system_prompt = """You are a search query optimizer for food shopping in Vietnam.
Your task is to convert user questions into effective search queries that will yield optimal results from Vietnamese grocery websites.
Focus on extracting key product names, specifications, and other relevant search terms.
Return ONLY the optimized search query without any explanations or additional text."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Convert this question into an effective search query: {user_query}"}
        ]
        
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",  # Using a smaller model for efficiency
            messages=messages,
            temperature=0.3,
            max_tokens=100,
        )
        
        enhanced_query = response.choices[0].message.content.strip()
        return enhanced_query
        
    except Exception as e:
        st.warning(f"Could not enhance search query: {e}")
        return user_query  # Fall back to original query if there's an error

def search_web(query):
    """Search the web using Tavily API with domain restrictions.
    Searches each domain separately and combines results."""
    all_results = {"results": []}
    
    try:
        # Generate enhanced search query
        enhanced_query = generate_enhanced_query(query)
        st.info(f"🔎 Searching with query: '{enhanced_query}'")
        
        for domain in ALLOWED_DOMAINS:
            try:
                domain_results = tavily_client.search(
                    # query=enhanced_query + f" site:{domain}",
                    query=enhanced_query + f" site:{domain}",
                    search_depth="advanced",
                    max_results=5
                )
                
                # Add domain results if they don't already exist in all_results
                for result in domain_results.get("results", []):
                    if not any(r.get("url") == result.get("url") for r in all_results["results"]):
                        all_results["results"].append(result)
                
            except Exception as e:
                continue  # Skip this domain if there's an error
                
        # Limit the total number of results to 8
        # all_results["results"] = all_results["results"][:8]
        
        return all_results
        
    except Exception as e:
        st.error(f"Error during web search: {e}")
        return {"results": []}

def get_gpt4o_response(user_query, search_results):
    """Get response from GPT-4o based on user query and search results."""
    try:
        context = "\n\n".join([
            f"Source: {result.get('url', 'No URL')}\nTitle: {result.get('title', 'No Title')}\nContent: {result.get('content', 'No Content')}"
            for result in search_results.get("results", [])
        ])
        
        # Track which retailers have data
        has_cooponline = any("cooponline.vn" in result.get('url', '') for result in search_results.get("results", []))
        has_bachhoaxanh = any("bachhoaxanh.com" in result.get('url', '') for result in search_results.get("results", []))
        has_winmart = any("winmart.vn" in result.get('url', '') for result in search_results.get("results", []))
        
        system_prompt = f"""You are a helpful food shopping assistant. Use the provided search results to answer user questions about food products and groceries from Vietnamese retailers.
Allowed domains: {', '.join(ALLOWED_DOMAINS)}
Always provide detailed information about products, including:
1. Price information (current price, discounted price, etc.)
2. Product specifications (weight, volume, quantity)
3. Brand information when available
4. Promotions or special offers
5. Availability status

When comparing products, include price differences and value comparisons.
If the information isn't available in the search results, admit that you don't know.
Only provide information available from these retailers' websites.
Respond in the same language as the user's query.

IMPORTANT: At the beginning of your response, clearly mention which retailers have data for this query:
- Mention "Coop Online" if there's data from cooponline.vn
- Mention "Bách Hóa Xanh" if there's data from bachhoaxanh.com
- Mention "Winmart" if there's data from winmart.vn
"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Search results:\n{context}\n\nUser question: {user_query}\n\nRetailers with data: {'Coop Online' if has_cooponline else ''}{', Bách Hóa Xanh' if has_bachhoaxanh else ''}{', Winmart' if has_winmart else ''}"}
        ]
        
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7,
            max_tokens=800,
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        st.error(f"Error getting GPT-4o response: {e}")
        return "Sorry, I encountered an error while processing your request."

# App header
st.title("🍔 Food Shopping Assistant")
st.markdown("""
Ask questions about products from these Vietnamese retailers:
- Coop Online
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
            search_results = search_web(prompt)
            print(search_results)

            # Get GPT-4o response
            response = get_gpt4o_response(prompt, search_results)
            
            # Display response
            st.markdown(response)
            
            # Optionally show search sources (collapsible)
            with st.expander("View Sources"):
                for i, result in enumerate(search_results.get("results", [])):
                    st.markdown(f"**Source {i+1}:** [{result.get('title')}]({result.get('url')})")
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Add sidebar with info
with st.sidebar:
    st.header("About")
    st.info("""
    This assistant searches for food products across major Vietnamese retailers.
    It uses Tavily to search the web and GPT-4o to process the information.
    """)
    
    # Add API key inputs for easier testing
    st.subheader("API Keys (for testing)")
    new_openai_key = st.text_input("OpenAI API Key", type="password")
    new_tavily_key = st.text_input("Tavily API Key", type="password")
    
    if st.button("Update API Keys"):
        try:
            if new_openai_key:
                os.environ["OPENAI_API_KEY"] = new_openai_key
                OpenAI(api_key=new_openai_key)  # Test the key
                st.success("OpenAI API key updated!")
            if new_tavily_key:
                os.environ["TAVILY_API_KEY"] = new_tavily_key
                TavilyClient(api_key=new_tavily_key)  # Test the key
                st.success("Tavily API key updated!")
            st.rerun()
        except Exception as e:
            st.error(f"Invalid API key: {e}")
