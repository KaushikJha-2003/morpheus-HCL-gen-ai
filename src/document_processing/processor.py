"""
Document processing utilities for text splitting and vectorization.
"""
import streamlit as st
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config.settings import CHUNK_SIZE, CHUNK_OVERLAP, CHROMA_DIR
from src.vectorstore.chroma_manager import create_vectorstore_from_documents


def process_documents(docs, embedding_model):
    """
    Process documents by splitting and creating vector store.
    
    Args:
        docs: List of Document objects
        embedding_model: Embedding model for vectorization
        
    Returns:
        Chroma vector store or None on failure
    """
    if not docs:
        st.error("No documents provided.")
        return None
    
    if not embedding_model:
        st.error("Embedding model unavailable.")
        return None
    
    try:
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )
        document_chunks = text_splitter.split_documents(docs)
        
        if not document_chunks:
            st.error("Text splitting failed.")
            return None
        
        # Create vector store
        vector_store = create_vectorstore_from_documents(
            document_chunks,
            embedding_model
        )
        
        if vector_store:
            st.success(f"Vector DB created with {len(document_chunks)} chunks.")
            # Store documents in session for BM25 retrieval
            st.session_state.document_chunks = document_chunks
        
        return vector_store
    
    except Exception as e:
        st.error(f"Document processing error: {e}")
        return None

