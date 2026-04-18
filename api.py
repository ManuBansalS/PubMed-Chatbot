import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import time

from src_rag.ingestion.pubmed_client import PubMedClient
from src_rag.ingestion.parser import PubMedParser
from src_rag.database.vector_store import VectorStore
from src_rag.retrieval.search_engine import SearchEngine
from src_rag.generation.generators import ResponseGenerator
from src_rag.generation.prompt_templates import get_medical_prompt
from src_rag.utils.logger import logger
from src_rag.generation.optimizer import get_optimized_search_query

app = FastAPI(title="PubMed Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str

# Lazy-load components gracefully
components = {}

def get_components():
    if not components:
        logger.info("Initializing RAG components...")
        components['pubmed'] = PubMedClient()
        components['parser'] = PubMedParser()
        components['db'] = VectorStore()
        components['search_engine'] = SearchEngine()
        components['generator'] = ResponseGenerator()
    return components

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    query = request.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Empty query provided.")
    
    if query.lower() in ["hi", "hello", "hey"]:
        return ChatResponse(answer="Hello! I am the PubMed AI Research Assistant. How can I help you with medical research today?")
        
    try:
        c = get_components()
        logger.info(f"Received query: {query}")
        
        # Optimize
        optimized_query = get_optimized_search_query(query)
        logger.info(f"Optimized Query for PubMed: {optimized_query}")
        
        # Fetch
        raw_xml = c['pubmed'].fetch_top_articles(optimized_query)
        if not raw_xml:
            return ChatResponse(answer="No relevant articles found on PubMed. Please try adjusting your query.")
            
        # Process
        chunks = c['parser'].parse_to_chunks(raw_xml)
        
        # Unique ID generated based on hash and timestamp to prevent overwriting
        ids = [f"doc_{i}_{hash(query)}_{int(time.time())}" for i in range(len(chunks))]
        c['db'].add_documents(chunks, ids)
        
        # Retrieval and Generation
        context = c['search_engine'].find_relevant_context(query, top_k=5)
        prompt = get_medical_prompt(query, context)
        final_answer = c['generator'].generate(prompt)
        
        return ChatResponse(answer=final_answer)
        
    except Exception as e:
        logger.error(f"API Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Serve the Vite Frontend Build Static Files gracefully
ui_dist_path = os.path.join(os.path.dirname(__file__), 'src_ui', 'dist')
if os.path.exists(ui_dist_path):
    app.mount("/", StaticFiles(directory=ui_dist_path, html=True), name="static")
else:
    logger.warning(f"UI build directory not found at {ui_dist_path}. Run 'npm run build' inside src_ui.")
