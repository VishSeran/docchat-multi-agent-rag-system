
from dotenv import load_dotenv
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from configuration.config import RELAVENCE_EVALUATOR_MODEL,relevance_checker_prompt
from configuration.logger import get_logger
from langchain_classic.retrievers import EnsembleRetriever

logger = get_logger("relavence-evaluator")

class RelevanceEvaluatorAgent:
    
    def __init__(self, relavence_model=RELAVENCE_EVALUATOR_MODEL):
        
        try:
            
            load_dotenv()
            GROQ_API = os.getenv("GROQ_API")
            
            if not GROQ_API:
                raise ValueError("groq api key is missing")
            
            
            self.llm_grader =  ChatGroq(
                model=relavence_model,
                temperature=0,
                max_tokens=10,
                api_key=GROQ_API
            )
            
            logger.info("LLM relevance evaluator is created")
            
            relevance_prompt_template = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        relevance_checker_prompt
                    ),
                    
                    (
                        "human",
                        """
                        question: 
                        {question}
                        
                        document_content:
                        {document_content}
                         
                        """
                    )
                ]
            )
            
            logger.info("LLM relavence evaluator prompt is created")
            
            self.relevance_chain = relevance_prompt_template | self.llm_grader
            
            logger.info("LLM relavence evaluator chain is created")
            
        except ValueError as e:
            logger.error(f"Value error: {e}")
            raise
        
        except Exception as e:
            logger.error(f"Error in llm model initialization : {e}")
            raise
        
    
    def evaluate_relevance(self, question, retriever:EnsembleRetriever, k=5):
        
        """
        1. Retrieve the top-k document chunks from the global retriever.
        2. Combine them into a single text string.
        3. Pass that text + question to the LLM for classification.        
        
        Returns: "CAN_ANSWER", "PARTIAL", or "NO_MATCH".
        """
        
        try:
            top_docs = retriever.invoke(question)
            document_content = "\n\n".join(document.content for document in top_docs[:k])
            
            response = self.relevance_chain.invoke({
                "question": question,
                "document_content": document_content
            })
            
            logger.info("Relavence response is fetched")
            
            return response.content.strip()
            
            
            
        except ValueError as e:
            logger.error(f"Value error: {e}")
            raise
        
        except Exception as e:
            logger.error(f"Error in get evaluate relevance: {e}")
            raise