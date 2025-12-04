"""
Session state management utilities.
"""
import streamlit as st


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! Models are loading..."}
        ]
    
    if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = None
    
    if "llm" not in st.session_state:
        st.session_state.llm = None
    
    if "embeddings_model" not in st.session_state:
        st.session_state.embeddings_model = None
    
    if "persona_select" not in st.session_state:
        st.session_state.persona_select = "Helpful Assistant"

