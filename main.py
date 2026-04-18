import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src_rag'))

from src_rag.ingestion.pubmed_client import PubMedClient
from src_rag.ingestion.parser import PubMedParser
from src_rag.database.vector_store import VectorStore
from src_rag.retrieval.search_engine import SearchEngine
from src_rag.generation.generators import ResponseGenerator
from src_rag.generation.prompt_templates import get_medical_prompt
from src_rag.utils.logger import logger
from src_rag.generation.optimizer import get_optimized_search_query # Import the optimizer

def run_chatbot():
    # Initialize components
    pubmed = PubMedClient()
    parser = PubMedParser()
    db = VectorStore()
    search_engine = SearchEngine()
    generator = ResponseGenerator()

    print("Welcome to the PubMed AI Research Assistant!")
    print("Type 'exit' or 'quit' to end the session.")

    while True:
        original_query = input("\n[User]: ").strip()
        if original_query.lower() in ['exit', 'quit']: break
        if not original_query: continue

        # 1. Handle Greetings
        if original_query.lower() in ["hi", "hello", "hey"]:
            print("\n[System]: Hello! I am here to help with medical research.")
            continue

        # 2. Optimize Query for PubMed
        print(f"[System]: Analyzing request...")
        optimized_query = get_optimized_search_query(original_query)
        print(f"[System]: Searching PubMed for: '{original_query}' (optimized to '{optimized_query}')'")
        
        try:
            # 3. Fetch top articles using OPTIMIZED query
            raw_xml = pubmed.fetch_top_articles(optimized_query)
            
            if not raw_xml:
                print("[System]: No relevant articles found. Please try a different query.")
                continue

            # 4. Process and Store
            chunks = parser.parse_to_chunks(raw_xml)
            ids = [f"doc_{i}_{hash(original_query)}" for i in range(len(chunks))]
            db.add_documents(chunks, ids)
            
            # 5. Retrieve Context (using original query for better semantic match)
            context = search_engine.find_relevant_context(original_query, top_k=5)

            # 6. Generate Response (using original query)
            prompt = get_medical_prompt(original_query, context)
            final_answer = generator.generate(prompt)

            print("[System]: Here's what I found based on the latest research:\n", final_answer)

        except Exception as e:
            logger.error(f"Chatbot error: {e}")
            print(f"[System Error]: Something went wrong. Check logs for details.")

if __name__ == "__main__":
    run_chatbot()