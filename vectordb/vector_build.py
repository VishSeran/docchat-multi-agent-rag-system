
from langchain_huggingface import HuggingFaceEmbeddings
from configuration.logger import get_logger
from configuration.config import COLLECTION_NAME, CHROMA_DB_PATH,HYBRID_RETRIEVER_WEIGHTS
from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever



logger = get_logger("vector-build")

class VectorBuild:
     
    def __init__(self, docs,embedding_model, collection_name:str = COLLECTION_NAME):
        
        
        try:
            
            self.embedding_model = embedding_model
            
            logger.info("Embedding model initialized")
            
            self.vector_store = Chroma.from_documents(
                documents=docs,
                embedding=self.embedding_model,
                collection_name=collection_name,
                persist_directory=CHROMA_DB_PATH
            )
            
            logger.info("Vector store initialized")
            
            self.bm25_retriever = BM25Retriever.from_documents(docs)
            logger.info("BM25 retriever initialized")
            
            self.vector_store_retriever = self.vector_store.as_retriever(
                search_type = "similarity_score_threshold",
                search_kwargs = {
                    "score_threshold": 0.6,
                    "k": 5
                }
            )
            
            logger.info("Vector retriever initialized")
            
            self.hybrid_retriever = EnsembleRetriever(
                retrievers=[self.bm25_retriever, self.vector_store_retriever],
                weights=HYBRID_RETRIEVER_WEIGHTS
            )
            
            logger.info("Hybrid retriever initialized")
            
        
        
        except ValueError as e:
            logger.error(f"Value error: {e}")
            raise
        
        except Exception as e:
            logger.error(f"Error in vector build initialization: {e}")
            raise
        