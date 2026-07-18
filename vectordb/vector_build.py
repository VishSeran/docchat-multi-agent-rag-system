
from langchain_huggingface import HuggingFaceEmbeddings
from configuration.logger import get_logger


logger = get_logger("vector-build")

class VectorBuild:
    
    def __init__(self):
        
        self.embedding_model = HuggingFaceEmbeddings(
            model_name = "BAAI/bge-m3",
            model_kwargs = {
                "device": "cuda"
            },
            encode_kwargs = {
                "normalize_embeddings": True
            }
        )
        
        