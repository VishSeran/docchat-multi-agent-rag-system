import hashlib
from configuration.logger import get_logger
from vectordb.file_handler import DocumentProcessor
from vectordb.embedding import EmbeddingModel
from vectordb.vector_build import VectorBuild
from agent_workflow.agent_workflow import AgentWorkflow

logger = get_logger("main")

def main():
    
    try:
        
        document_processor = DocumentProcessor()
        embedding_model = EmbeddingModel()
        vector_db = VectorBuild(embedding_model.get_model())
        workflow = AgentWorkflow()
        
        
        
        
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
            
            current_hashes = _get_file_hash(docs)
            
            if state['retriever'] is None or current_hashes != state['hashes']:
            
                chunks = document_processor.document_process(docs)
                retriever = vector_db.get_retriever(
                    chunks=chunks
                )
                
                state.update({
                    "hashes": current_hashes,
                    "retriever": retriever
                })
            
            result = workflow.run(
                question=question,
                retriever=state['retriever']
            )
            
            return result['final_answer'], result['verifier_result'], state
            
            
            
            
            
            
            
        except ValueError as e:
                logger.error(f"Value error: {e}")   
                raise
            
        except Exception as e:
            logger.error(f"Error in question handler: {e}")
            raise
        
    
    def _get_file_hash(upload_docs:list)->frozenset:
        
        hashes = set()
        
        for file in upload_docs:
            with open(file.name, "rb") as f:
                hashes.add(hashlib.sha256(f.read()).hexdigest())
                
        return frozenset(hashes)
                
        
    
    