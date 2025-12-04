"""
Configuration settings for the Intellicite application.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).parent.parent

# Data directories
DATA_DIR = BASE_DIR / "data"
CHROMA_DIR = BASE_DIR / "chroma_store"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
CHROMA_DIR.mkdir(exist_ok=True)

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Model configurations
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL_NAME = "llama-3.3-70b-versatile"
LLM_TEMPERATURE = 0.2

# Text splitter configurations
CHUNK_SIZE = 1500
CHUNK_OVERLAP = 200

# RAG configurations
RETRIEVER_K = 5 
BM25_WEIGHT = 0.5  
SEMANTIC_WEIGHT = 0.5  

# Personas
PERSONAS = {
    "Helpful Assistant": "You are a helpful assistant.",
    "Technical Expert": "You are a technical engineering expert.",
    "Business Analyst": "You are a strategic business analyst.",
    "ELI5 (Explain Like I'm 5)": "Explain concepts in very simple terms like I'm 5 years old.",
}

# Streamlit page config
PAGE_TITLE = "Intellicite"
PAGE_LAYOUT = "wide"

