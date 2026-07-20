from langchain_groq import ChatGroq
from configuration.logger import get_logger
from dotenv import load_dotenv
from configuration.config import LLM_MODEL, research_prompt
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import os


logger = get_logger("model")

class ResearchAgent:
    
    def __init__(self, llm_model_id = LLM_MODEL):
        
        try:
            
            load_dotenv()
            GROQ_API = os.getenv("GROQ_API")
            
            if not GROQ_API:
                raise ValueError("groq api key is missing")
            
            
            self.llm_generator = ChatGroq(
                model=llm_model_id,
                temperature=0.5,
                max_tokens=500,
                api_key=GROQ_API
            )
            
            logger.info("LLM model loaded")
            
            research_prompt_template = ChatPromptTemplate.from_messages([
                (
                    "system",
                    research_prompt
                ),
                
                (
                    "human",
                    """
                    Question: 
                    {question}
                    
                    Context:
                    {context}   
                    """
                )
            ])
            
            logger.info("LLM reseach agent Created")
            
            self.research_chain = research_prompt_template | self.llm_generator
            
            
            
        
        except ValueError as e:
            logger.error(f"Value error: {e}")
            raise
        
        except Exception as e:
            logger.error(f"Error in llm model initialization : {e}")
            raise
        
    
    def evaluate_verification (self, answer, context):
        
        try:
            
            response = self.verifier_chain.invoke({
                "answer": answer,
                "context": context
            })
            
            
            
        except ValueError as e:
            logger.error(f"Value error: {e}")
            raise
        
        except Exception as e:
            logger.error(f"Error in get evaluate verification: {e}")
            raise    