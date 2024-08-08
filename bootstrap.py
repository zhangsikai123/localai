import os
import socket
from backend.configs.server_config import API_SERVER

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Connect to a known external server
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except socket.error:
        raise Exception("Unable to get local IP address")
    
ip_address = get_local_ip()

port = API_SERVER["port"]
api_key = input("Enter API_KEY: ")
os.environ["OPENAI_API_KEY"] = api_key
os.environ["VITE_BASE_URL"] = f"http://{ip_address}:{port}"

# Output the set environment variable values
print("Environment variables set:")
print(f"API_KEYOPENAI_API_KEY: {os.getenv('API_KEY')}")
print(f"VITE_BASE_URL: {os.getenv('VITE_BASE_URL')}")
os.system("make backend && make frontend")
