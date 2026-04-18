import os
from google import genai
from src.utils.config import Config

class GeminiEmbedder:
    def __init__(self):
        # Uses the Gemini API key from your configuration [cite: 59, 92]
        self.client = genai.Client(api_key=Config.GEMINI_API_KEY)

    def get_embedding(self, text: str):
        """Generates a numerical vector for a single string of text[cite: 44, 116]."""
        result = self.client.models.embed_content(
            model=Config.EMBED_MODEL,
            contents=text,
            config={"task_type": "retrieval_document"}
        )
        return result.embeddings[0].values

    def get_embeddings_batch(self, text_chunks: list[str]):
        """Generates vectors for a list of text chunks for bulk storage[cite: 116]."""
        embeddings = []
        for chunk in text_chunks:
            embeddings.append(self.get_embedding(chunk))
        return embeddings