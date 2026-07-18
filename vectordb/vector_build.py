
from langchain_huggingface import HuggingFaceEmbeddings
from configuration.logger import get_logger
from configuration.config import COLLECTION_NAME
from langchain_community.vectorstores import Chroma



logger = get_logger("vector-build")

class VectorBuild:
     
    def __init__(self, docs, collection_name:str = COLLECTION_NAME):
        
        self.embedding_model = HuggingFaceEmbeddings(
            model_name = "BAAI/bge-m3",
            model_kwargs = {
                "device": "cuda"
            },
            encode_kwargs = {
                "normalize_embeddings": True
            }
        )
        
        self.vector_store = Chroma.from_documents(
            documents=docs,
            embedding=self.embedding_model,
            collection_name=collection_name,
            pers
        )
        
        