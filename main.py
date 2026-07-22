import hashlib
import gradio as gr
from configuration.logger import get_logger
from vectordb.file_handler import DocumentProcessor
from vectordb.embedding import EmbeddingModel
from vectordb.vector_build import VectorBuild
from agent_workflow.agent_workflow import AgentWorkflow

logger = get_logger("main")

def main():
    
    try:
        
        document_processor = DocumentProcessor()
        embedding_model = EmbeddingModel()
        vector_db = VectorBuild(embedding_model.get_model())
        workflow = AgentWorkflow()
        
        with gr.Blocks(title="DocChat - Multi Agent RAG System") as demo:
            gr.Markdown("## DocChat: powered by Docling 🐥 and LangGraph")
            gr.Markdown("# How it works ✨:")
            gr.Markdown("📤 Upload your document(s), enter your query then press Submit 📝")
            gr.Markdown("Or you can select one of the examples from the drop-down menu, select Load Example then press Submit 📝")
            gr.Markdown("⚠️ Note: DocChat only accepts documents in these formats: '.pdf', '.docx', '.txt', '.md'")  
            
            session_state = gr.State({
                "hashes": frozenset(),
                "retriever": None
            })
            
            with gr.Row():
                
                with gr.Column():
                    files = gr.File(label="📄 Upload Documents", type='filepath')
                    question = gr.Textbox(label="❓ Question", lines=3)
                    submit_btn = gr.Button("Submit")
                    
                    
                with gr.Column():
                    
                    answer = gr.Textbox(label="Answer", interactive=False)
                    verfication_result = gr.TextArea(label="✅ Verification Report")
                    
                submit_btn.click(
                    fn = question_handler,
                    inputs = [question,files],
                    outputs = [answer, verfication_result, session_state]
                )
        
        
    except ValueError as e:
            logger.error(f"Value error: {e}")   
            raise
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
        raise 
    
    
    def question_handler(question:str, docs:list, state:dict):
        
        try:
            
            if not question:
                raise ValueError("Question must not be empty")
            
            if not docs:
                raise ValueError("Documents must not be empty")
            
            if not state:
                raise ValueError("State must not be empty")
            
            logger.info("Processing new/changed documents...")
            
            current_hashes = _get_file_hash(docs)
            
            if state['retriever'] is None or current_hashes != state['hashes']:
            
                chunks = document_processor.document_process(docs)
                retriever = vector_db.get_retriever(
                    chunks=chunks
                )
                
                state.update({
                    "hashes": current_hashes,
                    "retriever": retriever
                })
            
            result = workflow.run(
                question=question,
                retriever=state['retriever']
            )
            
            return result['final_answer'], result['verifier_result'], state
   
        except ValueError as e:
                logger.error(f"Value error: {e}")   
                raise
            
        except Exception as e:
            logger.error(f"Error in question handler: {e}")
            return f"Error: {str(e)}", "", state 
        
    
    def _get_file_hash(upload_docs:list)->frozenset:
        
        hashes = set()
        
        for file in upload_docs:
            with open(file.name, "rb") as f:
                hashes.add(hashlib.sha256(f.read()).hexdigest())
                
        return frozenset(hashes)
                
        
    
    