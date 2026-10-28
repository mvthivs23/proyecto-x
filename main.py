import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

respuesta = client.chat.completions.create(
    model="recursive/flint-v1.0:free",
    messages=[
        {"role": "system", "content": "Eres un asistente técnico que responde en español."},
        {"role": "user", "content": "Explica en tres frases qué es un webhook."},
    ],
)

print(respuesta.choices[0].message.content)