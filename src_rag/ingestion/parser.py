import io
import os
import json
from Bio import Entrez
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.config import Config

class PubMedParser:
    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP
        )

    def parse_to_chunks(self, xml_data: str):
        """
        Parses XML, chunks text, and saves a copy to data/processed for auditability.
        """
        records = Entrez.read(io.BytesIO(xml_data.encode('utf-8')))
        chunks = []
        
        for article in records.get('PubmedArticle', []):
            try:
                citation = article.get('MedlineCitation', {})
                article_data = citation.get('Article', {})
                
                title = article_data.get('ArticleTitle', 'No Title')
                pmid = citation.get('PMID', 'Unknown')
                
                # Safely extract and join abstract text fragments
                abstract_text = article_data.get('Abstract', {}).get('AbstractText', [])
                abstract = " ".join([str(text) for text in abstract_text]) if abstract_text else "No abstract."
                
                # Create the clean text format
                text = f"Title: {title}\nAbstract: {abstract}\nSource: https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
                
                # Split into chunks
                chunks.extend(self.splitter.split_text(text))
                
            except Exception as e:
                print(f"Skipping article due to parsing error: {e}")
                continue
        
        # AUDIT LOG: Save processed text to disk 
        # This allows you to verify what is actually being sent to the Vector Store
        os.makedirs("src_rag/data/processed", exist_ok=True)
        with open("src_rag/data/processed/latest_chunks.json", "w", encoding="utf-8") as f:
            json.dump(chunks, f, indent=4)
            
        return chunks