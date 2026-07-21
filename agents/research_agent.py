from langchain_groq import ChatGroq
from configuration.logger import get_logger
from dotenv import load_dotenv
from configuration.config import LLM_MODEL, research_prompt
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
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
            logger.error(f"Error in research agent initialization : {e}")
            raise
        
    
    def get_research_response (self, question, documents:Document):
        
        final_response = None
        
        try:
            logger.info(f"ResearchAgent.generate called with question='{question}' and {len(documents)} documents.")     
            context = "\n\n".join([doc.page_content for doc in documents])
            logger.info(f"Combined context length: {len(context)} characters.") 
            
            response = self.research_chain.invoke({
                "question": question,
                "context": context
            })
            
            logger.info("LLM response is fetched")
            
            if not response.content:
                final_response = "I cannot answer this question based on the provided documents."
            
            else:
                final_response = response.content.strip()
            
            logger.info(f"Generated answer: {final_response}")
            return final_response 
            
        except ValueError as e:
            logger.error(f"Value error: {e}")
            raise
        
        except Exception as e:
            logger.error(f"Error in get research response: {e}")
            raise RuntimeError("Failed to generate answer due to a model error.") from e