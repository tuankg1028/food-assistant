"""Response generation using OpenAI API."""

import streamlit as st
from config import GPT_RESPONSE_PROMPT, ALLOWED_DOMAINS

def get_gpt4o_response(user_query, search_results, openai_client):
    """Get response from GPT-4o based on user query and search results."""
    try:
        context = "\n\n".join([
            f"Source: {result.get('url', 'No URL')}\nTitle: {result.get('title', 'No Title')}\nDetailed Scraped Content: {result.get('scraped_content', 'No scraped content')}"
            for result in search_results.get("results", [])
        ])
        
        # Track which retailers have data
        has_kingfoodmart = any("kingfoodmart.com" in result.get('url', '') for result in search_results.get("results", []))
        has_bachhoaxanh = any("bachhoaxanh.com" in result.get('url', '') for result in search_results.get("results", []))
        has_winmart = any("winmart.vn" in result.get('url', '') for result in search_results.get("results", []))
        
        system_prompt = GPT_RESPONSE_PROMPT.format(allowed_domains=", ".join(ALLOWED_DOMAINS))

        messages = [
            {"role": "system", "content": system_prompt},
        ]
        
        # Add conversation history (previous messages)
        if "messages" in st.session_state:
            # Only include the last 4 message pairs to avoid context length issues
            history_messages = st.session_state.messages[-8:] if len(st.session_state.messages) > 8 else st.session_state.messages
            for msg in history_messages:
                # Skip the current user message as it will be added separately
                if msg["role"] == "user" and msg["content"] == user_query:
                    continue
                messages.append({"role": msg["role"], "content": msg["content"]})

        content = f"Search results:\n{context}\n\nUser question: {user_query}\n\nRetailers with data: {'Kingfoodmart' if has_kingfoodmart else ''}{', Bách Hóa Xanh' if has_bachhoaxanh else ''}{', Winmart' if has_winmart else ''}"
        print("Content for GPT-4o:", content)  # Debugging line
        # Add current search context and user query
        messages.append({"role": "user", "content": content})
        
        # Return the streaming response directly
        return openai_client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7,
            max_tokens=800,
            stream=True,
        )
    
    except Exception as e:
        st.error(f"Error getting GPT-4o response: {e}")
        return "Sorry, I encountered an error while processing your request."
