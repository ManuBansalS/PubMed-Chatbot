import io
from Bio import Entrez
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from utils.config import Config

class PubMedParser:
    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP
        )

    def parse_to_chunks(self, xml_data: str):
        # Cleans XML and splits text into manageable chunks[cite: 42, 43]
        records = Entrez.read(io.BytesIO(xml_data.encode('utf-8')))
        chunks = []
        
        for article in records['PubmedArticle']:
            title = article['MedlineCitation']['Article']['ArticleTitle']
            abstract = article['MedlineCitation']['Article'].get('Abstract', {}).get('AbstractText', [""])[0]
            pmid = article['MedlineCitation']['PMID']
            
            text = f"Title: {title}\nAbstract: {abstract}\nSource: https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
            chunks.extend(self.splitter.split_text(text))
            
        return chunks