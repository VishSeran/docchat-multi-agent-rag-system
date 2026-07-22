
from configuration.logger import get_logger
from vectordb.file_handler import DocumentProcessor
from vectordb.embedding import EmbeddingModel
from vectordb.vector_build import VectorBuild

logger = get_logger("main")

def main():
    
    try:
        
        document_processor = DocumentProcessor()
        embedding_model = EmbeddingModel()
        vector_db = VectorBuild()
        
        
        
        
    except ValueError as e:
            logger.error(f"Value error: {e}")   
            raise
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
        raise 
    
    
    def question_handler(question:str, docs:list, state:dict):
        
        try:
            
            if not question:
                raise ValueError("Question must not be empty")
            
            if not docs:
                raise ValueError("Documents must not be empty")
            
            if not state:
                raise ValueError("State must not be empty")
            
            logger.info("Processing new/changed documents...")
            
            chunks = document_processor.document_process(docs)
            
        except ValueError as e:
                logger.error(f"Value error: {e}")   
                raise
            
        except Exception as e:
            logger.error(f"Error in question handler: {e}")
            raise
    
    