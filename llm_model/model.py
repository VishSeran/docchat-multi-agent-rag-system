
from langchain_groq import ChatGroq
from configuration.logger import get_logger
from dotenv import load_dotenv
import os


logger = get_logger("model")

class LLMModel:
    
    def __int__(self, model_id):
        
        try:
            
        
            load_dotenv()
            GROQ_API = os.getenv("GROQ_API")
            
            self.llm_grader =  ChatGroq(
                model=model_id,
                temperature=0,
                api_key=GROQ_API
            )
            
            self.llm_generator = ChatGroq(
                model=model_id,
                temperature=0.5,
                api_key=GROQ_API
            )
        
        except ValueError as e:
            logger.error(f"Value error: {e}")
            raise
        
        except Exception as e:
            logger.error(f"Error in llm model initialization : {e}")
            raise