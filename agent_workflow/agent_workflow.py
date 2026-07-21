from agents.relavence_evaluator_agent import RelevanceEvaluatorAgent
from agents.research_agent import ResearchAgent
from agents.verifier_evaluator_agent import VerifierEvaluatorAgent
from agent_state import AgentState
from langgraph.graph import StateGraph
from configuration.logger import get_logger


logger = get_logger("agent-workflow")

class AgentWorkflow:
    
    def __init__(self):
        self.relevance_agent = RelevanceEvaluatorAgent()
        self.research_agent = ResearchAgent()
        self.verifier_agent = VerifierEvaluatorAgent()
        logger.info("Agents are initialized")
        
        
    def build_workflow(self):
        
        workflow = StateGraph(AgentState)
        workflow.add_node("check_relavence",)
        workflow.add_node("research",)
        workflow.add_node("verifier",)
        
    
    def _check_relavence(self,state:AgentState):
        
        retriever = state['retriever']
        
        relavence_response = self.relevance_agent.evaluate_relevance(
            state['question'],
            retriever,
            k=20
        )
        
        if relavence_response == "CAN_ANSWER":
            return{
                "is_relavent"
            }
        
        
        
        
        
        
    
    
