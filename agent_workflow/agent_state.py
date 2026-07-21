from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph.message import add_messages
from langchain_core.documents import Document
from configuration.logger import get_logger
from langchain_classic.retrievers import EnsembleRetriever


logger = get_logger("agent-state")

class AgentState(TypedDict):
    
    messages: Annotated[list[HumanMessage | AIMessage],add_messages]
    question: str
    retriever: EnsembleRetriever

    relevance_result: str
    is_relevant: bool

    research_result: str

    verifier_result: str
    is_verified: bool

    final_answer: str
    