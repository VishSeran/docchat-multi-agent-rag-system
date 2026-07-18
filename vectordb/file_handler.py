from configuration.logger import get_logger
from docling.document_converter import DocumentConverter
from configuration.config import CACHE_DIR
from pathlib import Path

logger = get_logger("file-handler")

class DocumentProcessor:
    
    def __init__(self):
        self.headers = [("#", "Header1 "), ("##", "Header 2")]
        self.cache_dir = Path(CACHE_DIR)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        
    