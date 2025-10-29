import streamlit as st
from groq import Groq
import chromadb

# === SETUP ===
GROQ_API_KEY = "API_key"
client = Groq(api_key=GROQ_API_KEY)
chroma_client = chromadb.PersistentClient(path="./nova_db")
collection = chroma_client.get_or_create_collection("spacex_data")

# === SYSTEM PROMPT ===
SYSTEM_PROMPT = """
You are Nova, an expert AI assistant for SpaceX, Starlink, and modern space technology.
- Answer only the question; no reasoning, no explanations.
- Be concise, clear, friendly, and professional.
- Use retrieved context if available.
- Include sources if relevant.
"""

# === STREAMLIT CONFIG ===
st.set_page_config(
    page_title="🚀 Nova – SpaceX Mission Control",
    page_icon="🛰️",
    layout="wide",
)

# === CUSTOM CSS WITH BACKGROUND, STARS, SATELLITE, AND TITLE COLORS ===
st.markdown(
    """
    <style>
    body {
        background: radial-gradient(circle at 20% 30%, #0f0c29, #302b63, #1a1a2e);
        background-attachment: fixed;
        color: #ffffff;
        font-family: 'Segoe UI', sans-serif;
        overflow-x: hidden;
    }

    /* Twinkling stars */
    .star {
        position: absolute;
        background: white;
        border-radius: 50%;
        animation: twinkle 2s infinite alternate;
        opacity: 0.8;
    }
    @keyframes twinkle {
        0% { opacity: 0.3; }
        100% { opacity: 1; }
    }

    /* Moving satellite in curved orbit */
    .satellite {
        position: absolute;
        width: 80px;
        height: 40px;
        background: url('https://i.imgur.com/jT0VXkJ.png') no-repeat center/contain;
        animation: orbit 25s linear infinite;
        z-index: -1; /* behind chat */
    }
    @keyframes orbit {
        0% { transform: translate(0vw, 5vh) rotate(0deg); }
        25% { transform: translate(30vw, 15vh) rotate(90deg); }
        50% { transform: translate(60vw, 10vh) rotate(180deg); }
        75% { transform: translate(30vw, 5vh) rotate(270deg); }
        100% { transform: translate(0vw, 5vh) rotate(360deg); }
    }

    /* Titles and footer */
    .title, .subtitle, .footer {
        text-align: center;
        background: linear-gradient(90deg, #4b0082, #9b59b6, #d6b3ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    .title { font-size: 48px; margin-bottom: 5px; }
    .subtitle { font-size: 20px; margin-bottom: 30px; }
    .footer { font-size: 12px; margin-top: 30px; }

    /* Chat boxes */
    .chat-box {
        border-radius: 15px;
        padding: 12px 18px;
        margin: 8px;
        max-width: 65%;
        font-size: 16px;
        word-wrap: break-word;
    }

    .user-msg {
        background: linear-gradient(135deg, #00aaff, #0055ff);
        color: #fff;
        float: right;
        text-align: right;
        clear: both;
        font-weight: bold;
        box-shadow: 0px 0px 15px rgba(0,170,255,0.5);
        animation: floatUser 2s infinite alternate;
    }
    @keyframes floatUser {
        0% { transform: translateY(0px); }
        100% { transform: translateY(-3px); }
    }

    .nova-msg {
        background: linear-gradient(135deg, #b991ff, #8f6fff);
        color: #fff;
        float: left;
        text-align: left;
        clear: both;
        font-weight: bold;
        box-shadow: 0px 0px 15px rgba(155,93,229,0.6);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# === ADD STARS AND SATELLITE TO BODY ===
stars_html = "\n".join([
    f'<div class="star" style="top:{i*4}%; left:{i*6}%; width:{2+i%3}px; height:{2+i%3}px;"></div>'
    for i in range(50)
])
st.markdown('<div class="satellite"></div>' + stars_html, unsafe_allow_html=True)

# === TITLE & SUBTITLE ===
st.markdown('<div class="title">NOVA MISSION CONTROL</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">SpaceX & Starlink AI Assistant — Powered by Groq & ChromaDB</div>', unsafe_allow_html=True)

# === SESSION MEMORY ===
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# === ASK FUNCTION ===
def ask_nova(query):
    results = collection.query(query_texts=[query], n_results=3, include=["documents"])
    context = "\n".join(doc for doc in results["documents"][0])
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"""
Context:
{context}

Question:
{query}

Instructions:
- You can reason internally if you want.
- BUT only provide the final answer in your output.
- Do NOT include internal reasoning or <think> blocks.
"""}
    ]
    response = client.chat.completions.create(
        model="qwen/qwen3-32b",
        messages=messages
    )
    raw_answer = response.choices[0].message.content.strip()
    clean_answer = raw_answer.replace("<think>", "").replace("</think>", "").strip()
    final_answer = clean_answer.split("\n")[-1].strip()
    return final_answer

# === CHAT INPUT ===
user_input = st.chat_input("Type your question for Nova... 🚀")

if user_input:
    with st.spinner("🛰️ Nova is calculating trajectory..."):
        answer = ask_nova(user_input)
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Nova", answer))

# === DISPLAY CHAT HISTORY ===
for role, text in st.session_state.chat_history:
    if role == "You":
        st.markdown(f'<div class="chat-box user-msg">🧑‍🚀 You: {text}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-box nova-msg">🤖 Nova: {text}</div>', unsafe_allow_html=True)

# === FOOTER ===
st.markdown(
    '<div class="footer">🛰️ Nova – Developed by Nada Emad • Powered by Groq & ChromaDB • Inspired by SpaceX Mission Control</div>',
    unsafe_allow_html=True
)
