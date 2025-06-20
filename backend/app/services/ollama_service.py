import requests
import subprocess
from utils.ollama_errors import check_ollama_health
import signal


OLLAMA_URL = "http://localhost:11434/api/generate"
ollama_process = None  # Global variable to track the Ollama process

def start_ollama_server():
    """Start the Ollama server."""
    global ollama_process
    try:
        ollama_process = subprocess.Popen(["ollama", "serve"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Ollama server started.")
    except Exception as e:
        raise RuntimeError(f"Failed to start Ollama server: {str(e)}")
    
def stop_ollama_server():
    """Stop the Ollama server."""
    global ollama_process
    if ollama_process:
        try:
            ollama_process.send_signal(signal.SIGTERM)  # Gracefully terminate the process
            ollama_process.wait()  # Wait for the process to terminate
            print("Ollama server stopped.")
        except Exception as e:
            raise RuntimeError(f"Failed to stop Ollama server: {str(e)}")



def generate_response(query, context=""):
    
    try:
        check_ollama_health()
        prompt = f"""Based on the following context, please answer the question. Keep your response focused and relevant.
                            Context: {context}
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