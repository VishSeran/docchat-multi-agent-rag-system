from configuration.config import VERIFIER_EVALUATOR_MODEL, verifier_prompt
from configuration.logger import get_logger
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import dotenv
import os


logger = get_logger("verifier-evalutor")

class VerifierEvaluator:
    
    def __init__(self, verifier_model=VERIFIER_EVALUATOR_MODEL):
        
        dotenv.load_dotenv()
        groq_api = os.getenv("GROQ_API")
        
        
        self.llm_verifier = ChatGroq(
            model=verifier_model,
            temperature=0,
            max_tokens=10,
            api_key=groq_api
        )
        
        verifier_prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                verifier_prompt
            ),
            
            (
                "human",
                """
                answer: 
                {answer}
                
                context:
                {context}
                         
                """
            )
            
        ])