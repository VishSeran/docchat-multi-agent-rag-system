from agents.relavence_evaluator_agent import RelavenceEvaluatorAgent
from agents.research_agent import ResearchAgent
from agents.verifier_evaluator_agent import VerifierEvaluatorAgent
from configuration.logger import get_logger


logger = get_logger("agent-workflow")

class AgentWorkflow:
    
    def __init__(self):
        self.relavence_agent = RelavenceEvaluatorAgent()
        self.research_agent = ResearchAgent()
        self.verifier_agent = VerifierEvaluatorAgent()
        logger.info("Agents are initialized")
        
        
    
    
