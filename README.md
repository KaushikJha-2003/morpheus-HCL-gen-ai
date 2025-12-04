# Intellicite - AI Document Assistant

A multi-modal RAG (Retrieval Augmented Generation) system built with Streamlit, Groq LLM, and ChromaDB. This application allows you to upload documents (PDF, websites, YouTube videos) and interact with them using an AI assistant.

## Features

- **PDF Document Processing**: Upload and query PDF documents
- **Website Content Processing**: Extract and query content from websites
- **YouTube Video Processing**: Process YouTube video transcripts
- **Multiple AI Personas**: Choose from different AI personas (Helpful Assistant, Technical Expert, Business Analyst, ELI5)
- **Vector Search**: Powered by ChromaDB for efficient document retrieval
- **Fast Inference**: Uses Groq for high-speed LLM inference

## Project Structure

```
.
├── app.py                      # Main Streamlit application
├── config/                     # Configuration settings
│   ├── __init__.py
│   └── settings.py            # Application settings and constants
├── src/                        # Source code modules
│   ├── models/                # Model loading utilities
│   │   ├── __init__.py
│   │   └── loader.py          # LLM and embeddings loader
│   ├── document_processing/   # Document loading and processing
│   │   ├── __init__.py
│   │   ├── loaders.py         # Document loaders (PDF, Web, YouTube)
│   │   └── processor.py       # Text splitting and processing
│   ├── vectorstore/           # Vector database management
│   │   ├── __init__.py
│   │   └── chroma_manager.py  # ChromaDB operations
│   ├── rag/                   # RAG chain creation
│   │   ├── __init__.py
│   │   ├── prompts.py         # Prompt templates
│   │   └── chain.py           # RAG chain construction
│   ├── ui/                    # UI components
│   │   ├── __init__.py
│   │   ├── sidebar.py         # Sidebar UI
│   │   └── chat.py            # Chat interface
│   └── utils/                 # Utility functions
│       ├── __init__.py
│       └── session.py         # Session state management
├── data/                      # Uploaded documents (created automatically)
├── chroma_store/              # ChromaDB storage (created automatically)
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## Installation

1. **Clone the repository** (if applicable) or navigate to the project directory.

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**:
   - Copy `.env.example` to `.env`
   - Add your Groq API key:
     ```
     GROQ_API_KEY=your_actual_api_key_here
     ```
   - Get your API key from [Groq Console](https://console.groq.com/)

6. **Install Playwright browsers** (required for web scraping):
   ```bash
   playwright install
   ```

## Usage

1. **Run the Streamlit application**:
   ```bash
   streamlit run app.py
   ```

2. **Upload or link a document**:
   - Use the sidebar to upload a PDF, provide a website URL, or link a YouTube video
   - Click "Process" to load the document into the vector database

3. **Start chatting**:
   - Select an AI persona from the sidebar
   - Ask questions about your document in the chat interface
   - The AI will use the document context to answer your questions

## Configuration

You can modify settings in `config/settings.py`:
- Model configurations (LLM model name, temperature, etc.)
- Text splitting parameters (chunk size, overlap)
- RAG parameters (number of retrieved documents)
- AI personas

## Technologies Used

- **Streamlit**: Web application framework
- **Groq**: Fast LLM inference
- **ChromaDB**: Vector database for embeddings
- **LangChain**: LLM application framework
- **HuggingFace**: Sentence transformers for embeddings
- **PyPDF**: PDF processing
- **Playwright**: Web scraping for website content
- **youtube-transcript-api**: YouTube transcript extraction

## Notes

- The first run will download the embedding model, which may take some time
- Large documents may take longer to process
- ChromaDB data is stored locally in the `chroma_store/` directory
- Uploaded files are temporarily stored in the `data/` directory

## License

[Add your license here]

