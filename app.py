"""
Intellicite - AI Document Assistant
Main Streamlit application entry point.
"""
import streamlit as st

from config.settings import PAGE_TITLE, PAGE_LAYOUT
from src.utils.session import initialize_session_state
from src.models.loader import load_all_models
from src.ui.sidebar import render_sidebar
from src.ui.chat import render_chat_interface

# Configure Streamlit page
st.set_page_config(page_title=PAGE_TITLE, layout=PAGE_LAYOUT)

# Initialize session state
initialize_session_state()

# Load models at startup
if st.session_state.llm is None:
    with st.spinner("Loading models..."):
        st.session_state.embeddings_model, st.session_state.llm = load_all_models()
        
        if st.session_state.llm:
            st.session_state.messages = [
                {"role": "assistant", "content": "Models loaded! Upload or link a document to begin."}
            ]

# Render UI
render_sidebar()
render_chat_interface()

