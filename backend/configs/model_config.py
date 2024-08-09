import os


API_KEY = os.getenv("API_KEY")
# Llama or OpenAI
LLM_MODEL = "OpenAI"
# history session count window
HISTORY_LEN = 3
# LLM temperature
TEMPERATURE = 0.7
MAX_TOKEN = 1000
