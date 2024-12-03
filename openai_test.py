import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_type = "azure"
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION")

try:
    response = openai.Completion.create(
        engine="text-davinci-003",  # Remplacez par le nom de votre modèle déployé sur Azure, par ex. "gpt-4"
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Test de connexion."}
        ],
        max_tokens=10,
        temperature=0.5
    )
    print("Connexion réussie :", response['choices'][0]['message']['content'].strip())
except Exception as e:
    print(f"Erreur de connexion Azure OpenAI : {e}")
