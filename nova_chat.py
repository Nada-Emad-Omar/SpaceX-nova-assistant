import streamlit as st
from groq import Groq
import chromadb

# === SETUP ===
GROQ_API_KEY = "API_key"  # Replace with your key safely
client = Groq(api_key=GROQ_API_KEY)
chroma_client = chromadb.PersistentClient(path="./nova_db")
collection = chroma_client.get_or_create_collection("spacex_data")

# === SYSTEM PROMPT ===
SYSTEM_PROMPT = """
You are **Nova**, an expert AI assistant for SpaceX, Starlink, and modern space tech.
- Always answer concisely and clearly.
- Use retrieved context first.
- Never show your reasoning (<think>), just the final answer.
- Friendly, professional, and approachable tone.
- Include sources if available.
"""

# === STREAMLIT PAGE ===
st.set_page_config(page_title="🚀 Nova – SpaceX Mission Control", page_icon="🛰️")
st.title("🛰️ NOVA MISSION CONTROL")
st.subheader("SpaceX & Starlink AI Assistant — Powered by Groq & ChromaDB")

# === SESSION MEMORY ===
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# === ASK FUNCTION ===
def ask_nova(query):
    results = collection.query(query_texts=[query], n_results=3, include=["documents"])
    context = "\n".join(doc for doc in results["documents"][0])

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
    ]

    response = client.chat.completions.create(
        model="qwen/qwen3-32b",
        messages=messages
    )

    return response.choices[0].message.content

# === CHAT UI ===
user_input = st.chat_input("Type your question for Nova... 🚀")

if user_input:
    with st.spinner("🛰️ Nova is calculating trajectory..."):
        answer = ask_nova(user_input)
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Nova", answer))

# Display chat history
for role, text in st.session_state.chat_history:
    if role == "You":
        st.markdown(f"**🧑‍🚀 You:** {text}")
    else:
        st.markdown(f"**🤖 Nova:** {text}")

# === FOOTER ===
st.markdown(
    """
🛰️ Nova – Developed by Nada Emad • Powered by Groq & ChromaDB • Inspired by SpaceX Mission Control
"""
)
