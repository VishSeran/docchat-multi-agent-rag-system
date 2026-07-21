

from typing import TypedDict,Annotated
from pydantic import Field
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langchain_core.documents import Document
from configuration.logger import get_logger
from langchain_classic.retrievers import EnsembleRetriever


logger = get_logger("agent-state")

class AgentState(TypedDict):
    
    messages: Annotated[BaseMessage,add_messages]
    question: BaseMessage
    documents: list[Document]
    draft_answer: BaseMessage
    verification_report: BaseMessage
    is_relavent: bool
    retriever: EnsembleRetriever
    