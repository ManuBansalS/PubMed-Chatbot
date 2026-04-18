import os
import ssl
from Bio import Entrez
from src_rag.utils.config import Config

class PubMedClient:
    def __init__(self):
        # Bypass SSL verification to prevent connection crashes
        ssl._create_default_https_context = ssl._create_unverified_context
        Entrez.email = Config.EMAIL
        Entrez.api_key = Config.PUBMED_API_KEY

    def fetch_top_articles(self, query: str):
        """Search PubMed and return raw XML string."""
        try:
            # 1. Search for IDs
            search_handle = Entrez.esearch(db="pubmed", term=query, retmax=Config.TOP_ARTICLES)
            search_results = Entrez.read(search_handle)
            search_handle.close()
            id_list = search_results.get("IdList", [])

            if not id_list:
                print("No articles found.")
                return None

            # 2. Fetch full details (XML format)
            fetch_handle = Entrez.efetch(db="pubmed", id=",".join(id_list), rettype="xml", retmode="text")
            raw_xml = fetch_handle.read()
            fetch_handle.close()

            # 3. Save to data/raw in binary mode
            os.makedirs("src_rag/data/raw", exist_ok=True)
            with open("src_rag/data/raw/latest_fetch.xml", "wb") as f:
                if isinstance(raw_xml, str):
                    f.write(raw_xml.encode("utf-8"))
                else:
                    f.write(raw_xml)
            
            # Return the XML content as string for the parser
            return raw_xml if isinstance(raw_xml, str) else raw_xml.decode("utf-8")
            
        except Exception as e:
            print(f"Error fetching from PubMed: {e}")
            return None