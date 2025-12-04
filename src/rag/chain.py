"""
RAG chain creation utilities with hybrid BM25 + semantic retrieval.
"""
import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.retrievers import BaseRetriever
from langchain_community.retrievers import BM25Retriever

from config.settings import RETRIEVER_K, BM25_WEIGHT, SEMANTIC_WEIGHT
from src.rag.prompts import create_prompt_template


class HybridRetriever(BaseRetriever):
    """
    Hybrid retriever combining BM25 and semantic search results.
    """
    semantic_retriever: object
    bm25_retriever: object
    semantic_weight: float = 0.5
    bm25_weight: float = 0.5
    
    class Config:
        arbitrary_types_allowed = True
    
    def __init__(self, semantic_retriever, bm25_retriever, weights):
        super().__init__()
        self.semantic_retriever = semantic_retriever
        self.bm25_retriever = bm25_retriever
        self.semantic_weight = weights[0]
        self.bm25_weight = weights[1]
    
    def _get_relevant_documents(self, query: str):
        """
        Retrieve documents using both methods and combine results.
        """
        try:
            # Get results from both retrievers
            semantic_docs = self.semantic_retriever.invoke(query)
            bm25_docs = self.bm25_retriever.invoke(query)
            
            # Combine and deduplicate by content
            combined_docs = []
            seen_content = set()
            
            # Add semantic results (weighted higher if semantic_weight > bm25_weight)
            for doc in semantic_docs:
                if doc.page_content not in seen_content:
                    combined_docs.append(doc)
                    seen_content.add(doc.page_content)
            
            # Add BM25 results
            for doc in bm25_docs:
                if doc.page_content not in seen_content:
                    combined_docs.append(doc)
                    seen_content.add(doc.page_content)
            
            # Return top K documents
            return combined_docs[:RETRIEVER_K]
        except Exception as e:
            # Fallback to semantic search only on error
            return self.semantic_retriever.invoke(query)


def format_docs(docs):
    """
    Format retrieved documents into a single string.
    
    Args:
        docs: List of Document objects
        
    Returns:
        Formatted string of document contents
    """
    return "\n\n".join(doc.page_content for doc in docs)


def create_hybrid_retriever(vector_store, documents):
    """
    Create a hybrid retriever combining BM25 and semantic search.
    
    Args:
        vector_store: Chroma vector store for semantic search
        documents: List of documents for BM25 indexing
        
    Returns:
        HybridRetriever combining both methods
    """
    # Semantic retriever from vector store
    semantic_retriever = vector_store.as_retriever(
        search_kwargs={"k": RETRIEVER_K}
    )
    
    # BM25 retriever
    bm25_retriever = BM25Retriever.from_documents(documents)
    bm25_retriever.k = RETRIEVER_K
    
    # Hybrid retriever - combines both with configurable weights
    hybrid_retriever = HybridRetriever(
        semantic_retriever=semantic_retriever,
        bm25_retriever=bm25_retriever,
        weights=[SEMANTIC_WEIGHT, BM25_WEIGHT]
    )
    
    return hybrid_retriever


def create_rag_chain(vector_store, llm_model, persona: str, documents=None):
    """
    Create a RAG chain with hybrid BM25 + semantic retrieval.
    
    Args:
        vector_store: Chroma vector store
        llm_model: Language model
        persona: Selected persona name
        documents: List of documents for BM25 (optional, will extract from vector store if not provided)
        
    Returns:
        RAG chain or None on failure
    """
    if not vector_store:
        st.error("Vector store missing.")
        return None
    
    if not llm_model:
        st.error("LLM missing.")
        return None
    
    try:
        # Try to get documents from session state or parameter
        retriever = None
        
        if documents is None:
            documents = st.session_state.get('document_chunks')
        
        if documents:
            try:
                retriever = create_hybrid_retriever(vector_store, documents)
            except Exception as e:
                # Fallback to semantic search on hybrid creation failure
                retriever = None
        
        # Fallback to semantic-only retriever
        if retriever is None:
            retriever = vector_store.as_retriever(
                search_kwargs={"k": RETRIEVER_K}
            )
        
        # Create prompt template
        prompt = create_prompt_template(persona)
        
        # Create RAG chain
        chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm_model
            | StrOutputParser()
        )
        
        return chain
    
    except Exception as e:
        st.error(f"RAG chain creation failed: {e}")
        return None


