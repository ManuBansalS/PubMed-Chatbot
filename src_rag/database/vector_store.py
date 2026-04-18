import chromadb
import os
from utils.config import Config

class VectorStore:
    def __init__(self):
        # 1. Connect to Chroma Cloud using credentials from your configuration
        self.client = chromadb.CloudClient(
            api_key=Config.CHROMA_API_KEY,
            tenant=Config.CHROMA_TENANT,
            database=Config.CHROMA_DATABASE
        )
        
        # 2. Automatically create the collection if it's missing
        # This acts as the "table" for your research articles
        self.collection = self.client.get_or_create_collection(
            name="pubmed_research_collection"
        )

    def add_documents(self, chunks: list, ids: list):
        """Uploads text chunks to your cloud collection."""
        self.collection.add(
            documents=chunks, 
            ids=ids
        )

    def query_context(self, query_text: str, n_results: int = 5):
        """Searches the cloud collection for relevant text."""
        return self.collection.query(
            query_texts=[query_text], 
            n_results=n_results
        )