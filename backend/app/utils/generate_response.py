import requests
from services.ollama_service import OLLAMA_URL
from utils.ollama_errors import check_ollama_health


def generate_response(query, markdown_content: str):
    try:
        check_ollama_health()
        prompt = f"""Based on the following context, please answer the question.
        Keep your response focused and relevant with the context and document uploaded only.
        Context: {markdown_content}
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
            error_msg = "Mistral model not found. Please run: ollama pull mistral"
        return f"Error: {error_msg}"