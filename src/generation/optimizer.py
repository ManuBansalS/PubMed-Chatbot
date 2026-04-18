from google import genai
from utils.config import Config
from utils.logger import logger

def get_optimized_search_query(user_query: str):
    """
    Uses Gemini to transform a natural language question into 
    concise PubMed search keywords.
    """
    client = genai.Client(api_key=Config.GEMINI_API_KEY)
    
    prompt = f"""
    You are a medical research assistant. Convert the following user question 
    into a short, efficient query string for PubMed search. 
    Remove conversational filler. Return ONLY the search string.
    
    Question: "{user_query}"
    Search Query:
    """
    
    try:
        response = client.models.generate_content(
            model=Config.LLM_MODEL,
            contents=prompt
        )
        optimized_query = response.text.strip()
        logger.info(f"Optimized query: {optimized_query}")
        return optimized_query
    except Exception as e:
        logger.error(f"Optimization failed, using raw query: {e}")
        return user_query