from configuration.config import VERIFIER_EVALUATOR_MODEL, verifier_prompt
from configuration.logger import get_logger
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import dotenv
import os


logger = get_logger("verifier-evalutor")

class VerifierEvaluator:
    
    def __init__(self, verifier_model=VERIFIER_EVALUATOR_MODEL):
        
        try:
            
            if not verifier_model:
                raise ValueError("Verifier model is required to futher process!!!")
        
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
        
        except ValueError as e:
            logger.error(f"Value error: {e}")
            raise
        
        except Exception as e:
            logger.error(f"Error in verifier evaluator initialization: {e}")
            raise
        
    
    def verifier_response (self, answer, context):
        
        try:
            
            if not answer:
                raise ValueError("Model answer is missing")
            
            if not context:
                raise ValueError("Retrieved contexts are missing")
            
            response = self.verifier_chain.invoke({
                "answer": answer,
                "context": context
            })
        
        except ValueError as e:
            logger.error(f"Value error: {e}")
            raise
        
        except Exception as e:
            logger.error(f"Error in verifier response: {e}")
            raise   
        
        
    def extracted_info_from_response(self, response):
        
        try:
            
        except ValueError as e:
            logger.error(f"Value error: {e}")
            raise
        
        except Exception as e:
            logger.error(f"Error in extracted info from response: {e}")
            raise
    
    def fomrate_response(self, response):
        
        try:
            
        except ValueError as e:
            logger.error(f"Value error: {e}")
            raise
        
        except Exception as e:
            logger.error(f"Error in format verifier response: {e}")
            raise