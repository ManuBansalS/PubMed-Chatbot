import os
import ssl
from Bio import Entrez
from utils.config import Config


class PubMedClient:
    def __init__(self):
        # Bypass SSL verification for environments with strict SSL issues (e.g., some corporate networks)
        ssl._create_default_https_context = ssl._create_unverified_context
        # Always set an email for Entrez API compliance
        Entrez.email = Config.EMAIL
        Entrez.api_key = Config.PUBMED_API_KEY

    def fetch_top_articles(self, query: str):
        """Search PubMed and save raw XML to data/raw."""
        try:
            # Step 1: Search for IDs
            search_handle = Entrez.esearch(db="pubmed", term=query, retmax=Config.TOP_ARTICLES)
            search_results = Entrez.read(search_handle)
            search_handle.close()
            id_list = search_results.get("IdList", [])

            if not id_list:
                print("No articles found.")
                return []

            # Step 2: Fetch full details (XML format)
            fetch_handle = Entrez.efetch(db="pubmed", id=",".join(id_list), rettype="xml", retmode="text")
            raw_xml = fetch_handle.read()
            fetch_handle.close()

            # Save to data/raw
            os.makedirs("data/raw", exist_ok=True)
            with open("data/raw/latest_fetch.xml", "w", encoding="utf-8") as f:
                f.write(raw_xml)
            
            return id_list
        except Exception as e:
            print(f"Error fetching from PubMed: {e}")
            return []