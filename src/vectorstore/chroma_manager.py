"""
ChromaDB vector store management utilities.
"""
import os
import shutil
import time
import streamlit as st
import chromadb
from langchain_community.vectorstores import Chroma

from config.settings import CHROMA_DIR


def create_vectorstore_from_documents(document_chunks, embedding_model):
    """
    Create a ChromaDB vector store from document chunks.
    
    Args:
        document_chunks: List of document chunks
        embedding_model: Embedding model for vectorization
        
    Returns:
        Chroma vector store or None on failure
    """
    try:
        vector_store = Chroma.from_documents(
            documents=document_chunks,
            embedding=embedding_model,
            collection_name=f"docs_{int(time.time())}"
        )
        return vector_store
    
    except Exception as chroma_error:
        st.error(f"ChromaDB error: {chroma_error}")
        cleanup_chroma_db()
        
        try:
            # Fallback: try with explicit client
            client = chromadb.PersistentClient(path=CHROMA_DIR)
            vector_store = Chroma.from_documents(
                documents=document_chunks,
                embedding=embedding_model,
                client=client,
                collection_name=f"fallback_{int(time.time())}"
            )
            return vector_store
        
        except Exception as fallback_error:
            st.error(f"Fallback failure: {fallback_error}")
            return None


def cleanup_chroma_db():
    """
    Safely cleanup ChromaDB directory.
    
    Returns:
        bool: True if cleanup successful, False otherwise
    """
    try:
        if os.path.exists(CHROMA_DIR):
            import gc
            gc.collect()
            
            for attempt in range(3):
                try:
                    shutil.rmtree(CHROMA_DIR)
                    break
                except PermissionError:
                    time.sleep(1)
                    continue
                except Exception:
                    break
        
        os.makedirs(CHROMA_DIR, exist_ok=True)
        return True
    
    except Exception as e:
        st.warning(f"Could not fully cleanup database: {e}")
        return False

