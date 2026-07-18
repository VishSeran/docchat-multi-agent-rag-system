from configuration.logger import get_logger
from docling.document_converter import DocumentConverter
from configuration.config import CACHE_DIR, MAX_FILE_SIZE
from langchain_text_splitters.markdown import MarkdownHeaderTextSplitter
from pathlib import Path
import os
import pickle
from datetime import datetime

logger = get_logger("file-handler")

class DocumentProcessor:
    
    def __init__(self):
        self.headers = [("#", "Header1 "), ("##", "Header 2")]
        self.cache_dir = Path(CACHE_DIR)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("Document processor initialized")
        
    def valiate_files(self, files:list) -> None:
        
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
            logger.error(f"Error in validate files: {e}")
            raise
    
    
    def process_files (self, file):
        
        try:
            if not file:
                raise ValueError("file cannot be empty or none")
            
            if not file.name.endswith((".pdf", ".docx", ".txt", ".md")):
                raise ValueError(f"Unsupport file format: {file.name}")
             
            document_converter = DocumentConverter()
            markdown_content = document_converter.convert(file).document.export_to_markdown()
            spiltter = MarkdownHeaderTextSplitter(headers_to_split_on=self.headers)
            chunks = spiltter.split_text(markdown_content)
            
            logger.info("file splitted successful")
            
            return chunks
            
        except ValueError as e:
            logger.error(f"Value error: {e}")
            raise
        
        except Exception as e:
            logger.error(f"Error in process files: {e}")
            raise
        
    def save_to_cache(self,chunks:list, cache_path:Path):
        
        try:
            if not chunks:
                raise ValueError("Chunks are empty")
            
            if not cache_path:
                cache_path = self.cache_dir
                
            with open(cache_path, "wb") as file:
                pickle.dump({
                    "timestamp": datetime.now().timestamp(),
                    "chunks": chunks
                }, file) 
            
            logger.info("Cache saved successful")
            
        except ValueError as e:
            logger.error(f"Value error: {e}")
            raise
        
        except Exception as e:
            logger.error(f"Error in process files: {e}")
            raise
    