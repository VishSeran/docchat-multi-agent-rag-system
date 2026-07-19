CACHE_DIR = "../vectordb/document_cache"
MAX_FILE_SIZE = 50
EMBED_MODEL = "BAAI/bge-m3"
COLLECTION_NAME = "docchat_collection"
CHROMA_DB_PATH = "../vectordb/vectore_store"
HYBRID_RETRIEVER_WEIGHTS = [0.5, 0.5]

RELAVENCE_EVALUATOR_MODEL = "llama-3.1-8b-instant"
VERIFIER_EVALUATOR_MODEL = "llama-3.1-8b-instant"
LLM_MODEL = "llama-3.1-8b-instant"


relevance_checker_prompt = """

        You are an AI relevance checker between a user's question and provided document content.        
        
        Instructions:
        - Classify how well the document content addresses the user's question.
        - Respond with only one of the following labels: CAN_ANSWER, PARTIAL, NO_MATCH.
        - Do not include any additional text or explanation.        
        
        Labels:
        1) "CAN_ANSWER": The passages contain enough explicit information to fully answer the question.
        2) "PARTIAL": The passages mention or discuss the question's topic but do not provide all the details needed for a complete answer.
        3) "NO_MATCH": The passages do not discuss or mention the question's topic at all.        
        
        Important: If the passages mention or reference the topic or timeframe of the question in any way, even if incomplete, respond with "PARTIAL" instead of "NO_MATCH".        
        
        Question: {question}
        Passages: {question}        
        
        Respond ONLY with one of the following labels: CAN_ANSWER, PARTIAL, NO_MATCH
       

"""


verifier_prompt = """
        You are an AI assistant designed to verify the accuracy and relevance of answers based on the provided context.        
        
        Instructions:
        - Verify the following answer against the provided context.
        - Check for:
        
        1. Direct/indirect factual support (YES/NO)
        2. Unsupported claims (list any if present)
        3. Contradictions (list any if present)
        4. Relevance to the question (YES/NO)
        
        - Provide additional details or explanations where relevant.
        - Respond in the exact format specified below without adding any unrelated information.        
        
        Format:
        Supported: YES/NO
        Unsupported Claims: [item1, item2, ...]
        Contradictions: [item1, item2, ...]
        Relevant: YES/NO
        Additional Details: [Any extra information or explanations]        
        
        Answer: 
        {answer}
        
        Context:
        {context}       
        
        Respond ONLY with the above format.
        
        
"""
