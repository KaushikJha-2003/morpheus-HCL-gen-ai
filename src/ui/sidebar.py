"""
Sidebar UI components.
"""
import streamlit as st
from config.settings import PERSONAS
from src.models.loader import load_all_models
from src.vectorstore.chroma_manager import cleanup_chroma_db
from src.document_processing.loaders import (
    load_pdf_document,
    load_web_document,
    load_youtube_document,
    save_uploaded_file
)
from src.document_processing.processor import process_documents


def render_sidebar():
    """Render the sidebar with document upload and configuration options."""
    with st.sidebar:
        st.header("Setup")
        
        # Reset Database button
        if st.button("Reset Database"):
            st.session_state.vectorstore = None
            if cleanup_chroma_db():
                st.success("Database reset.")
            else:
                st.warning("Partial reset. Restart app if issues occur.")
        
        # Model status
        if st.session_state.llm:
            st.success("LLM Loaded ✔")
            
            # Persona selection
            st.header("AI Persona")
            persona_list = list(PERSONAS.keys())
            default_index = 0
            if "persona_select" in st.session_state and st.session_state.persona_select in persona_list:
                default_index = persona_list.index(st.session_state.persona_select)
            
            st.session_state.persona_select = st.selectbox(
                "Choose persona",
                persona_list,
                index=default_index
            )
            
            # Document source selection
            st.header("Document Source")
            source_option = st.radio(
                "Select type",
                ["PDF Upload", "Website", "YouTube"]
            )
            
            # PDF Upload
            if source_option == "PDF Upload":
                render_pdf_upload()
            
            # Website
            elif source_option == "Website":
                render_website_upload()
            
            # YouTube
            elif source_option == "YouTube":
                render_youtube_upload()
        
        else:
            st.error("LLM not loaded. Check your GROQ_API_KEY.")


def render_pdf_upload():
    """Render PDF upload UI."""
    pdf = st.file_uploader("Upload PDF", type="pdf")
    
    if st.button("Process PDF") and pdf:
        with st.spinner("Reading PDF..."):
            try:
                file_path = save_uploaded_file(pdf)
                docs = load_pdf_document(file_path)
                
                st.session_state.vectorstore = process_documents(
                    docs,
                    st.session_state.embeddings_model
                )
                
                if st.session_state.vectorstore:
                    st.success("PDF processed!")
                    st.session_state.messages = [
                        {"role": "assistant", "content": "PDF ready! Ask anything about it."}
                    ]
                    st.rerun()
            
            except Exception as e:
                st.error(f"PDF error: {e}")


def render_website_upload():
    """Render website URL input UI."""
    url = st.text_input("Website URL")
    
    if st.button("Process Website") and url:
        with st.spinner("Reading website..."):
            try:
                docs = load_web_document(url)
                st.session_state.vectorstore = process_documents(
                    docs,
                    st.session_state.embeddings_model
                )
                
                if st.session_state.vectorstore:
                    st.success("Website processed!")
                    st.session_state.messages = [
                        {"role": "assistant", "content": "Website processed! Ask away."}
                    ]
                    st.rerun()
            
            except Exception as e:
                st.error(f"Website error: {e}")


def render_youtube_upload():
    """Render YouTube URL input UI."""
    url = st.text_input("YouTube URL")
    
    if st.button("Process YouTube") and url:
        with st.spinner("Reading transcript..."):
            try:
                docs = load_youtube_document(url)
                st.session_state.vectorstore = process_documents(
                    docs,
                    st.session_state.embeddings_model
                )
                
                if st.session_state.vectorstore:
                    st.success("Video processed!")
                    st.session_state.messages = [
                        {"role": "assistant", "content": "YouTube video ready! Ask about it."}
                    ]
                    st.rerun()
            
            except Exception as e:
                st.error(f"YouTube error: {e}")

