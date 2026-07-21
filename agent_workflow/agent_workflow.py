from agents.relavence_evaluator_agent import RelevanceEvaluatorAgent
from agents.research_agent import ResearchAgent
from agents.verifier_evaluator_agent import VerifierEvaluatorAgent
from agent_state import AgentState
from langgraph.graph import StateGraph
from configuration.logger import get_logger


logger = get_logger("agent-workflow")

class AgentWorkflow:
    
    def __init__(self):
        
        try:
            
            self.relevance_agent = RelevanceEvaluatorAgent()
            self.research_agent = ResearchAgent()
            self.verifier_agent = VerifierEvaluatorAgent()
            logger.info("Agents are initialized")
        
        except ValueError as e:
            logger.error(f"Value error: {e}")
            raise
        
        except Exception as e:
            logger.error(f"Error in Agent workflow initialization: {e}")
            raise
        
    def build_workflow(self):
        
        try:
        
            workflow = StateGraph(AgentState)
            workflow.add_node("check_relavence",)
            workflow.add_node("research",)
            workflow.add_node("verifier",)
        
        
        except ValueError as e:
            logger.error(f"Value error: {e}")
            raise
        
        except Exception as e:
            logger.error(f"Error in build workflow: {e}")
            raise    
    
    def _check_relavence(self,state:AgentState):
        
        try:
            
            retriever = state['retriever']
            
            relevance_response = self.relevance_agent.evaluate_relevance(
                state['question'],
                retriever,
                k=20
            )
            
            if relevance_response == "CAN_ANSWER" or relevance_response == "PARTIAL":
                return{
                    "is_relevant": True
                }
                
            else:
                return {
                    "is_relevant": False
                }
                
        except ValueError as e:
            logger.error(f"Value error: {e}")
            raise
        
        except Exception as e:
            logger.error(f"Error in check relevance: {e}")
            raise
        
        
        
        
        
        
        
        
    
    
