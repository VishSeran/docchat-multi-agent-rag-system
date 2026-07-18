from configuration.logger import get_logger
from docling.document_converter import DocumentConverter
from configuration.config import CACHE_DIR, MAX_FILE_SIZE
from pathlib import Path
import os

logger = get_logger("file-handler")

class DocumentProcessor:
    
    def __init__(self):
        self.headers = [("#", "Header1 "), ("##", "Header 2")]
        self.cache_dir = Path(CACHE_DIR)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("Document processor initialized")
        
    def valiate_file(self, files:list) -> None:
        
        try:
            
            if not files:
                raise ValueError("Files cannot be empty")
            
            file_size = sum(os.path.getsize(file.name) for file in files)
            
            if file_size > MAX_FILE_SIZE:
                raise ValueError(f"Total file size cannot exceed {MAX_FILE_SIZE} MB")
            
            logger.info("Files validate successful")
            
        except ValueError as e:
            logger.error(f"Value error: {e}")
            raise
        
        except Exception as e:
            logger.error(f"Error in document processor: {e}")
            raise
        
    