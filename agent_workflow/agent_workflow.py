from agents.relavence_evaluator_agent import RelevanceEvaluatorAgent
from agents.research_agent import ResearchAgent
from agents.verifier_evaluator_agent import VerifierEvaluatorAgent
from agent_state import AgentState
from langgraph.graph import StateGraph, END
from configuration.logger import get_logger
from langchain_core.messages import AIMessage, HumanMessage


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
            workflow.add_node("check_relavence",self._check_relevance)
            workflow.add_node("research",self._research_process)
            workflow.add_node("verifier",self._verifier_process)
            
            workflow.add_conditional_edges("check_relevance", self._relevance_condition)
            workflow.add_conditional_edges("verifier",)
        
        
        except ValueError as e:
            logger.error(f"Value error: {e}")
            raise
        
        except Exception as e:
            logger.error(f"Error in build workflow: {e}")
            raise    
    
    def _check_relevance(self,state:AgentState):
        
        try:
            
            retriever = state['retriever']
            
            relevance_response, top_docs = self.relevance_agent.evaluate_relevance(
                state['question'],
                retriever,
                k=20
            )
            
            logger.info("relevance response is fetched by _checker relevance")
            if relevance_response == "CAN_ANSWER" or relevance_response == "PARTIAL":
                return{
                    "messages": [AIMessage(content=relevance_response)],
                    "documents":[top_docs],
                    "relevance_result":relevance_response,
                    "is_relevant": True
                }
                
            else:
                return {
                    "messages": [AIMessage(content=relevance_response)],
                    "documents":[top_docs],
                    "is_relevant": False
                }
                
        except ValueError as e:
            logger.error(f"Value error: {e}")
            raise
        
        except Exception as e:
            logger.error(f"Error in check relevance: {e}")
            raise
        
        
    def _research_process(self, state:AgentState):
        
        try:
            
            research_response = self.research_agent.get_research_response(
                question=state["question"],
                documents=state['documents']
                
            )
            
            logger.info("research response fetched from agent workflow")
            
            return {
                "messages": [AIMessage(content=research_response)],
                "research_result": research_response
            }
            
        except ValueError as e:
            logger.error(f"Value error: {e}")
            raise
        
        except Exception as e:
            logger.error(f"Error in research process: {e}")
            raise
        
    
    def _verifier_process(self, state: AgentState):
        
        try:
            context = "\n\n".join(doc.page_content for doc in state['documents'])
            verifier_response = self.verifier_agent.verifier_response(
                answer=state['research_result'],
                context=context
            )
            
            if  "Supported: NO"  in verifier_response or "Relevant: NO":
            
                return{
                    
                    "verifier_result":verifier_response,
                    "is_verified":False
                }
                
            else:
                
                return{
                    "verifier_result":verifier_response,
                    "is_verified":True
                }
            
            
            
        except ValueError as e:
            logger.error(f"Value error: {e}")
            raise
        
        except Exception as e:
            logger.error(f"Error in verifier process: {e}")
            raise
        
        
    def _relevance_condition(self, state:AgentState):
        
        
        try:
            decision = "relevant" if state["is_relevant"] else "irrelevant"
            
            logger.info(f"[DEBUG] _relevance_condition -> {decision}")
            
            if state['is_relevant']:
                return "research"
            
            else:
                return END
        
        except ValueError as e:
            logger.error(f"Value error: {e}")
            raise
        
        except Exception as e:
            logger.error(f"Error in _relevance_condition: {e}")
            raise  
        
    
    def _verifier_condition(self,state:AgentState):
        
        try:
            
            decision = "end" if state['is_verified'] else "re-research"
            logger.info(f"[DEBUG] _relevance_condition -> {decision}")
            
            if state['is_verified']:
                return END
            
            else:
                return "research"
            
        except ValueError as e:
            logger.error(f"Value error: {e}")
            raise
        
        except Exception as e:
            logger.error(f"Error in _verifier_condition: {e}")
            raise
        
        
        
        
        
    
    
