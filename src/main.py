import sys
from ingestion.pubmed_client import PubMedClient
from ingestion.parser import PubMedParser
from database.vector_store import VectorStore
from retrieval.search_engine import SearchEngine
from generation.generators import ResponseGenerator
from generation.prompt_templates import get_medical_prompt
from utils.logger import logger

def run_chatbot():
    # Main loop for the PubMed RAG Terminal Chatbot
    
    # Initialize components once outside the loop for efficiency
    pubmed = PubMedClient()
    parser = PubMedParser()
    db = VectorStore()
    search_engine = SearchEngine()
    generator = ResponseGenerator()

    print("Welcome to the PubMed AI Research Assistant!")
    print("Type 'exit' or 'quit' to end the session.")

    while True:
        query = input("\n[User]: ").strip()
        if query.lower() in ['exit', 'quit']: break
        if not query: continue

        # 1. Check for Greetings (Keep these short and direct)
        greetings = ["hi", "hello", "hey", "hola"]
        if query.lower() in greetings:
            print("\n[System]: Hello! I am your PubMed Research Assistant. You can enter medical terms (e.g., 'heart attack') or full questions.")
            continue

        print(f"\n[System]: Searching PubMed for research related to '{query}'...")
        
        try:
            # Proceed with the full RAG pipeline
            raw_xml = pubmed.fetch_top_articles(query)

            # 2. Fetch top 2-3 articles [cite: 132, 147]
            raw_xml = pubmed.fetch_top_articles(query)
            
            if not raw_xml:
                print("[System]: No relevant articles found. Please try a different query.")
                continue

            # 3. Process and Store [cite: 148]
            chunks = parser.parse_to_chunks(raw_xml)
            ids = [f"doc_{i}_{hash(query)}" for i in range(len(chunks))]
            db.add_documents(chunks, ids)
            
            # 4. Retrieve Context [cite: 149, 237]
            context = search_engine.find_relevant_context(query, top_k=5)

            # 5. Generate and Display Response [cite: 150, 239]
            prompt = get_medical_prompt(query, context)
            final_answer = generator.generate(prompt)

            print("[System]: Here's what I found based on the latest research:",final_answer)

        except Exception as e:
            logger.error(f"Chatbot error: {e}") # [cite: 163, 208]
            print(f"[System Error]: Something went wrong. Check logs for details.")

if __name__ == "__main__":
    run_chatbot()