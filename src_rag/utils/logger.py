import logging

# 1. Setup the standard logging format
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# 2. Configure File logging (keeps all details for debugging)
file_handler = logging.FileHandler("src_rag/logs/pipeline.log")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(log_format))

# 3. Configure Stream logging (what you see in the terminal)
# We set this to ERROR so you don't see "INFO" or "HTTP" logs in your chat
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.ERROR) 
stream_handler.setFormatter(logging.Formatter(log_format))

# 4. Apply configuration
logging.basicConfig(
    level=logging.INFO,
    handlers=[file_handler, stream_handler]
)

# 5. CRITICAL: Silence external library "noise" [cite: 167, 277, 278]
# This prevents httpx and chromadb from flooding your chat interface
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("chromadb").setLevel(logging.WARNING)
logging.getLogger("google").setLevel(logging.WARNING)

logger = logging.getLogger("PubMed_RAG")