import os
from openai import AzureOpenAI
from dotenv import load_dotenv
# Charger les variables depuis le fichier .env
load_dotenv()

# Initialiser le client AzureOpenAI
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-10-21",
    azure_endpoint=os.getenv("AZURE_OPENAI_API_BASE")
)
completion = client.chat.completions.create(
  model="gpt-4o", # Replace with your model dpeloyment name.
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "When was Microsoft founded?"}
  ]
)

#print(completion.choices[0].message)
print(completion.model_dump_json(indent=2))