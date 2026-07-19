
from configuration.logger import get_logger
from configuration.config import EMBED_MODEL
from langchain_huggingface import HuggingFaceEmbeddings
import torch

logger = get_logger("embedding")

class EmbeddingModel:
    
    def __init__(self, embedding_model_id = EMBED_MODEL):
        
        
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Device is initialted: {device}")
        
        self.embed_model = HuggingFaceEmbeddings(
            model_name = embedding_model_id,
            model_kwargs = {
                "device": device
            },
            encode_kwargs = {
                "normalize_embeddings": True
            }
        )
        logger.info("Embedding model is initiated")
        
    