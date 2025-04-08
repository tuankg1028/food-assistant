"""Query enhancement utilities."""

import streamlit as st
from config import QUERY_OPTIMIZER_PROMPT

def generate_enhanced_query(user_query, openai_client):
    """Use GPT to generate a more effective search query based on the user's question and conversation history."""
    try:
        if not openai_client:
            return user_query
            
        # Extract previous user questions from chat history (up to 3 most recent)
        previous_queries = []
        if "messages" in st.session_state:
            for msg in reversed(st.session_state.messages):
                if msg["role"] == "user" and msg["content"] != user_query:
                    previous_queries.append(msg["content"])
                    if len(previous_queries) >= 3:
                        break
            
        # Reverse to get chronological order
        previous_queries.reverse()
        
        # Create context from previous queries if they exist
        context = ""
        if previous_queries:
            context = "Previous questions:\n" + "\n".join([f"- {q}" for q in previous_queries]) + "\n\n"
            
        messages = [
            {"role": "system", "content": QUERY_OPTIMIZER_PROMPT},
            {"role": "user", "content": f"{context}Current question: {user_query}\n\nGenerate an optimized search query combining relevant context from previous questions with the current question:"}
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
