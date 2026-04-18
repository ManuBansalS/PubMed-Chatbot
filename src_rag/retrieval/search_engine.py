from src_rag.database.vector_store import VectorStore
from src_rag.utils.logger import logger

class SearchEngine:
    def __init__(self):
        # Connects to your existing Chroma Cloud collection
        self.db = VectorStore() # [cite: 164]

    def find_relevant_context(self, user_query: str, top_k: int = 5):
        """
        Takes the user's question, searches the cloud vector store, 
        and returns the best matching text snippets for the LLM.
        """
        logger.info(f"Searching for context related to: {user_query}")  # [cite: 163, 165]
        
        try:
            # Query the cloud collection for the top K most similar chunks
            results = self.db.query_context(user_query, n_results=top_k) # [cite: 165]
            
            # Combine retrieved documents into a single formatted context string
            # This is what will be fed into your prompt template later.
            context_list = results.get('documents', [[]])[0]
            context_text = "\n\n---\n\n".join(context_list)
            
            logger.info(f"Successfully retrieved {len(context_list)} relevant chunks.") # [cite: 163]
            return context_text
            
        except Exception as e:
            logger.error(f"Error during semantic search: {e}") # [cite: 163]
            return ""