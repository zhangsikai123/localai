import os

api_key = input("Enter API_KEY: ")
ip_address = input("Enter the IP address to expose: ")
os.environ["OPENAI_API_KEY"] = api_key
os.environ["VITE_BASE_URL"] = f"http://{ip_address}:7861"

# Output the set environment variable values
print("Environment variables set:")
print(f"API_KEYOPENAI_API_KEY: {os.getenv('API_KEY')}")
print(f"VITE_BASE_URL: {os.getenv('VITE_BASE_URL')}")
os.system("make backend && make frontend")
