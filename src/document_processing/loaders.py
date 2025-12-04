"""
Document loaders for different sources (PDF, Web, YouTube).
"""
import os
import requests
try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False
from langchain_core.documents import Document
from langchain_community.document_loaders import (
    WebBaseLoader,
    YoutubeLoader,
    PyPDFLoader
)
from config.settings import DATA_DIR


def load_pdf_document(file_path: str):
    """
    Load a PDF document.
    
    Args:
        file_path: Path to the PDF file
        
    Returns:
        List of Document objects
    """
    try:
        loader = PyPDFLoader(file_path)
        return loader.load()
    except Exception as e:
        raise Exception(f"Error loading PDF: {e}")


def load_web_document(url: str):
    """
    Load a document from a website URL using requests + BeautifulSoup.
    
    Args:
        url: Website URL
        
    Returns:
        List of Document objects
    """
    try:
        # Use requests + BeautifulSoup directly for more reliable parsing
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        if HAS_BS4:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
        else:
            # Fallback: simple regex-based HTML removal
            import re
            text = response.text
            # Remove HTML tags
            text = re.sub('<[^<]+?>', '', text)
            # Clean up whitespace
            text = re.sub(r'\s+', ' ', text).strip()
        
        if not text or len(text.strip()) == 0:
            raise Exception("No content extracted from webpage")
        
        return [Document(page_content=text, metadata={"source": url})]
    except Exception as e:
        raise Exception(f"Error loading website: {e}. Try: pip install beautifulsoup4 requests")


def load_youtube_document(url: str):
    """
    Load a document from a YouTube video transcript.
    
    Args:
        url: YouTube video URL (supports youtube.com, youtu.be, youtube-nocookie.com, live streams)
        
    Returns:
        List of Document objects
    """
    try:
        # Normalize YouTube URL
        import re
        
        # Extract video ID from various YouTube URL formats
        video_id = None
        
        # Format: https://www.youtube.com/watch?v=VIDEO_ID
        match = re.search(r'youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})', url)
        if match:
            video_id = match.group(1)
        
        # Format: https://www.youtube.com/live/VIDEO_ID (live streams)
        if not video_id:
            match = re.search(r'youtube\.com/live/([a-zA-Z0-9_-]{11})', url)
            if match:
                video_id = match.group(1)
        
        # Format: https://youtu.be/VIDEO_ID
        if not video_id:
            match = re.search(r'youtu\.be/([a-zA-Z0-9_-]{11})', url)
            if match:
                video_id = match.group(1)
        
        # Format: https://www.youtube-nocookie.com/embed/VIDEO_ID
        if not video_id:
            match = re.search(r'youtube-nocookie\.com/embed/([a-zA-Z0-9_-]{11})', url)
            if match:
                video_id = match.group(1)
        
        if not video_id:
            raise Exception(f"Could not extract video ID from URL: {url}. Supported formats: https://www.youtube.com/watch?v=VIDEO_ID, https://youtu.be/VIDEO_ID, https://www.youtube.com/live/VIDEO_ID")
        
        # Construct proper YouTube URL for loader (use watch format for compatibility)
        youtube_url = f"https://www.youtube.com/watch?v={video_id}"
        
        try:
            loader = YoutubeLoader.from_youtube_url(youtube_url, add_video_info=True)
            docs = loader.load()
            
            if not docs or len(docs) == 0:
                raise Exception(f"No transcript found for video ID: {video_id}. The video may not have captions available.")
            
            return docs
        except Exception as loader_error:
            # If it's a live stream, it might not have a transcript yet
            if "live" in url.lower():
                raise Exception(f"Live streams may not have transcripts available yet. Try: 1) Wait for the stream to end, 2) Try a different video with captions enabled")
            raise loader_error
    
    except Exception as e:
        error_msg = str(e)
        if "400" in error_msg or "Bad Request" in error_msg:
            raise Exception(f"YouTube Error: The video may not be accessible or may not have a transcript. Try a different video. Original error: {e}")
        elif "Transcript" in error_msg or "transcript" in error_msg.lower():
            raise Exception(f"YouTube Error: This video doesn't have captions/transcript available. Try a different video.")
        else:
            raise Exception(f"Error loading YouTube video: {e}. Make sure you provided a valid YouTube URL.")


def save_uploaded_file(uploaded_file, destination_dir=DATA_DIR):
    """
    Save an uploaded file to the destination directory.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        destination_dir: Directory to save the file
        
    Returns:
        Path to the saved file
    """
    file_path = os.path.join(destination_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getvalue())
    return file_path

