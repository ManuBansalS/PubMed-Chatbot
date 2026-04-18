from google import genai
from src_rag.utils.config import Config
from src_rag.utils.logger import logger

class ResponseGenerator:
    def __init__(self):
        # Uses the Gemini API key from your config file [cite: 18, 59]
        self.client = genai.Client(api_key=Config.GEMINI_API_KEY)

    def generate(self, prompt: str):
        """
        Sends the structured prompt to the Gemini model and returns the text response.
        """
        logger.info("Sending prompt to Gemini for final response generation.")
        
        try:
            # Calls the specific LLM model defined in your config (e.g., gemini-1.5-pro) [cite: 18, 153]
            response = self.client.models.generate_content(
                model=Config.LLM_MODEL,
                contents=prompt
            )
            
            logger.info("Successfully received response from Gemini.")
            return response.text
            
        except Exception as e:
            logger.error(f"Error during Gemini response generation: {e}")
            return "Error: Unable to generate a response at this time."