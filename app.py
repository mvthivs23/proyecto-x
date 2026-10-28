import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MODEL = "recursive/flint-v1.0:free"
SYSTEM = "Eres un asistente técnico que responde en español, con claridad y sin relleno."

st.set_page_config(page_title="Chat", page_icon="💬")
st.title("Chat")
st.caption(f"Modelo gratis de OpenRouter: `{MODEL}`")

api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    st.error("Falta OPENROUTER_API_KEY en el archivo .env")
    st.stop()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM}]

if st.button("Nueva conversación"):
    st.session_state.messages = [{"role": "system", "content": SYSTEM}]
    st.rerun()

for message in st.session_state.messages:
    if message["role"] == "system":
        continue
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Escribe un mensaje")
if not prompt:
    st.stop()

st.session_state.messages.append({"role": "user", "content": prompt})
with st.chat_message("user"):
    st.markdown(prompt)

with st.chat_message("assistant"):
    try:
        with st.spinner("Pensando..."):
            respuesta = client.chat.completions.create(
                model=MODEL,
                messages=st.session_state.messages,
            )
        texto = respuesta.choices[0].message.content or ""
    except Exception as exc:
        st.session_state.messages.pop()
        st.error(f"No pude consultar el modelo: {exc}")
        st.stop()
    st.markdown(texto)

st.session_state.messages.append({"role": "assistant", "content": texto})
