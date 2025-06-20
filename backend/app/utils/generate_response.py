import requests
from services.ollama_service import OLLAMA_URL
from utils.ollama_errors import check_ollama_health


def generate_response(query, markdown_content: str):
    try:
        check_ollama_health()

        # Ensure context is not empty
        if not markdown_content.strip():
            return "No relevant information available in the uploaded documents."

        # Explicitly instruct the LLM to answer only based on the provided context
        prompt = f"""Based on the following document content, please answer the question.
        Do not use external sources or internet-based information. Your response must be strictly derived from the provided context.
        Context:
        {markdown_content}
        Question: {query}
        Answer:"""

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "llama3.2-vision",
                "prompt": prompt,
                "stream": False
            }
        )
        response.raise_for_status()
        return response.json().get("response", "")
    except Exception as e:
        error_msg = str(e)
        if "Connection refused" in error_msg:
            error_msg = "Could not connect to Ollama server. Please ensure Ollama is installed and running."
        elif "model not found" in error_msg.lower():
            error_msg = "Model not found. Please run: ollama pull llama3.2-vision"
        return f"Error: {error_msg}"