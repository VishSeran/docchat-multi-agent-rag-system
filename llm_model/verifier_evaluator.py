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
        
        
    def extracted_info_from_response(self, response:str):
        
        try:
            
            if not response:
                raise ValueError("Response is required to process")
            
            verifications = {}
            lines = response.split("\n")
            
            logger.info("response is splitted by lines")
            
            for line in lines:
                if ":" in line:
                    key, value = line.split(":", 1)
                    key = key.strip().capitalize()
                    value = value.strip()
                    
                    if key in {"Supported", "Unsupported claims", "Contradictions", "Relevant", "Additional details"}:
                        
                        if key in {"Unsupported claims", "Contradictions"}:
                            if value.startswith("[") and value.endswith("]"):
                                items = value[1:-1].split(",")
                                items = [item.strip('"').strip("'") for item in items if item.strip()]
                                
                                verifications[key] = items
                                
                            else:
                                verifications[key] = []
                                
                        elif key == "Additional details":
                            verifications[key] = value
                            
                        else:
                            verifications[key] = value.upper()
            
            logger.info("Verifications are fetched")
                            
            return verifications
            
            
            
        except ValueError as e:
            logger.error(f"Value error: {e}")
            raise
        
        except Exception as e:
            logger.error(f"Error in extracted info from response: {e}")
            raise
    
    def fomrate_response(self, verification:dict):
        
        try:
            
            supported = verification.get("Supported", "NO")
            unspported_claims = verification.get("Unsupported claims", [])
            contradictions = verification.get("Contradictions", [])
            relevant = verification.get("Relevant", "NO")
            additional_details = verification.get("Additional details", "")
            
            result = f"**Supported**: {supported}\n"
            
            if unspported_claims:
                result += f"**Unsupported Claims**: {", ".join(unspported_claims)}\n"
            
            else:
                result += "**Unsupported Claims:** None\n"

            if contradictions:
                result += f"**Contradictions:** {', '.join(contradictions)}\n"
            else:
                result += "**Contradictions:** None\n"

            result += f"**Relevant:** {relevant}\n"

            if additional_details:
                result += f"**Additional Details:** {additional_details}\n"
            else:
                result += "**Additional Details:** None\n"
                
            logger.info("Result is fetched")
                
            return result
            
        except ValueError as e:
            logger.error(f"Value error: {e}")
            raise
        
        except Exception as e:
            logger.error(f"Error in format verifier response: {e}")
            raise