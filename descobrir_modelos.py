import os
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega o .env
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Configura a chave (lembre de usar o nome exato que está no seu .env)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("Modelos disponíveis para a sua chave:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)