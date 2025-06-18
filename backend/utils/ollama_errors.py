class OllamaConnectionError(Exception):
    pass

def check_ollama_health():
    import requests
    import psutil
    import socket
    
    def is_port_in_use(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('127.0.0.1', port)) == 0
    
    try:
        if is_port_in_use(11434):
            # Check if Ollama is actually running
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] == 'ollama':
                    return True  # Ollama is running and using the port
            raise OllamaConnectionError(
                "Port 11434 is in use by another application. Please:\n"
                "1. Stop any other applications using port 11434\n"
                "2. Restart Ollama with: ollama serve"
            )
        
        response = requests.get("http://localhost:11434/api/health")
        return response.status_code == 200
    except requests.ConnectionError:
        raise OllamaConnectionError(
            "Could not connect to Ollama server. Please ensure Ollama is installed and running."
        )