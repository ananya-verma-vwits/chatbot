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
