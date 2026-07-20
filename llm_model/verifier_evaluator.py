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
        
        logger.info("LLM verifier is created")
        
        verifier_prompt_template = ChatPromptTemplate.from_messages([
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
        
        logger.info("LLM verifier prompt is created")
        self.verifier_chain = verifier_prompt_template | self.llm_verifier
        logger.info("LLM verifier chain is created successful")