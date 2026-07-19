from langchain_groq import ChatGroq
from configuration.logger import get_logger
from dotenv import load_dotenv
from configuration.config import EVALUATOR_MODEL, LLM_MODEL 
import os


logger = get_logger("model")

class LLMModel:
    
    def __int__(self, evaluator_model = EVALUATOR_MODEL, llm_model_id = LLM_MODEL):
        
        try:
            
            load_dotenv()
            GROQ_API = os.getenv("GROQ_API")
            
            if not GROQ_API:
                raise ValueError("groq api key is missing")
            
            
            self.llm_grader =  ChatGroq(
                model=evaluator_model,
                temperature=0,
                api_key=GROQ_API
            )
            
            self.llm_generator = ChatGroq(
                model=llm_model_id,
                temperature=0.5,
                api_key=GROQ_API
            )
        
        except ValueError as e:
            logger.error(f"Value error: {e}")
            raise
        
        except Exception as e:
            logger.error(f"Error in llm model initialization : {e}")
            raise
        
    
    def get_evaluator_chain (self):
        
        