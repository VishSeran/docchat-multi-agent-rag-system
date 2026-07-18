from configuration.logger import get_logger
from docling.document_converter import DocumentConverter
from configuration.config import CACHE_DIR
from pathlib import Path
import os

logger = get_logger("file-handler")

class DocumentProcessor:
    
    def __init__(self):
        self.headers = [("#", "Header1 "), ("##", "Header 2")]
        self.cache_dir = Path(CACHE_DIR)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
    def valiate_file(self, files:list):
        
        try:
            
            if not files:
                raise ValueError("Files cannot be empty")
            
            file_size = sum(os.path.getsize(file.name) for file in files)
            
            if file_size > 
            
        except ValueError as e:
            logger.error(f"Value error: {e}")
            raise
        
        except Exception as e:
            logger.error(f"Error in document processor: {e}")
            raise
        
    