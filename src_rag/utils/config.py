import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    PUBMED_API_KEY = os.getenv("PUBMED_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    EMAIL = os.getenv("EMAIL")
    CHROMA_DATABASE = os.getenv("CHROMA_DATABASE")
    CHROMA_TENANT = os.getenv("CHROMA_TENANT")
    CHROMA_API_KEY = os.getenv("CHROMA_API_KEY")

    # Model Settings
    EMBED_MODEL = "gemini-embedding-001"
    LLM_MODEL = "gemma-3-1b-it" # Updated to the latest Gemini model [cite: 150]
    
    # RAG Settings
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 100
    TOP_ARTICLES = 3  # As per your requirement [cite: 132]