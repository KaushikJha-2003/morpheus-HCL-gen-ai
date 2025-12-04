"""Document processing package."""
from src.document_processing.loaders import (
    load_pdf_document,
    load_web_document,
    load_youtube_document
)
from src.document_processing.processor import process_documents

__all__ = [
    "load_pdf_document",
    "load_web_document",
    "load_youtube_document",
    "process_documents"
]

