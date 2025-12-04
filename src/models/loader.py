"""
Model loading utilities for LLM and embeddings.
"""
import streamlit as st
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

from config.settings import (
    GROQ_API_KEY,
    EMBEDDING_MODEL_NAME,
    LLM_MODEL_NAME,
    LLM_TEMPERATURE
)


@st.cache_resource
def load_all_models():
    """
    Load Groq LLM + HuggingFace embeddings.
    
    Returns:
        tuple: (embedding_model, llm_model) or (None, None) on failure
    """
    if not GROQ_API_KEY:
        st.error("Groq API Key not found. Add GROQ_API_KEY to .env file.")
        return None, None
    
    try:
        # Load embedding model
        embedding_model = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL_NAME,
            model_kwargs={"device": "cpu"}
        )
        
        # Load Groq LLM
        llm_model = ChatGroq(
            api_key=GROQ_API_KEY,
            model=LLM_MODEL_NAME,
            temperature=LLM_TEMPERATURE
        )
        
        return embedding_model, llm_model
    
    except Exception as e:
        st.error(f"Failed to load Groq LLM or embeddings: {e}")
        return None, None

