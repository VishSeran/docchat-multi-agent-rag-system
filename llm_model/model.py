from langchain_groq import ChatGroq
from configuration.logger import get_logger
from dotenv import load_dotenv
from configuration.config import EVALUATOR_MODEL, LLM_MODEL, relevance_checker_prompt
from langchain_core.prompts import PromptTemplate
import os


logger = get_logger("model")

class LLMModel:
    
    def __init__(self, evaluator_model = EVALUATOR_MODEL, llm_model_id = LLM_MODEL):
        
        try:
            
            load_dotenv()
            GROQ_API = os.getenv("GROQ_API")
            
            if not GROQ_API:
                raise ValueError("groq api key is missing")
            
            
            self.llm_grader =  ChatGroq(
                model=evaluator_model,
                temperature=0,
                max_tokens=10,
                api_key=GROQ_API
            )
            
            self.llm_generator = ChatGroq(
                model=llm_model_id,
                temperature=0.5,
                max_tokens=200,
                api_key=GROQ_API
            )
            
            prompt_template = PromptTemplate(
                template=relevance_checker_prompt,
                input_variables=["question","document_content"],
                
            )
            
            self.relevance_chain = prompt_template | self.llm_grader
            
        
        except ValueError as e:
            logger.error(f"Value error: {e}")
            raise
        
        except Exception as e:
            logger.error(f"Error in llm model initialization : {e}")
            raise
        
        
    def get_evaluate_response(self,relevence_chain, question, document_content):
        
        """
        1. Retrieve the top-k document chunks from the global retriever.
        2. Combine them into a single text string.
        3. Pass that text + question to the LLM for classification.        
        
        Returns: "CAN_ANSWER", "PARTIAL", or "NO_MATCH".
        """
        
        try:
            response = self.relevence_chain.invoke({
                "question": question,
                "document_content": document_content
            })
            
            return response.content.strip()
            
            
            
        except ValueError as e:
            logger.error(f"Value error: {e}")
            raise
        
        except Exception as e:
            logger.error(f"Error in get evaluate response initialization : {e}")
            raise