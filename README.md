# 🚀 SpaceX Nova Assistant

SpaceX Nova Assistant is an AI chatbot that answers questions about **SpaceX**, **Starlink**, and modern space technology.

This project contains **two main files**:

1. `nova_chat.py` – Run this file to launch the interactive chat in your browser using **Streamlit**.
2. `NovaChat.ipynb` – A Jupyter notebook for **building the knowledge database** (scraping SpaceX websites, fetching API data, creating embeddings).

---

## How to Use

### 1️⃣ Set Up

* Install Python 3.10+
* Install dependencies:

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install streamlit chromadb sentence-transformers beautifulsoup4 requests groq python-dotenv
```

### 2️⃣ Provide Your Groq API Key

* Create a `.env` file in the project folder:

```
GROQ_API_KEY=your_api_key_here
```

> Keep this key private. Do not share it publicly.

### 3️⃣ Run Nova

* Launch the chat with Streamlit:

```bash
streamlit run nova_chat.py
```

* Ask Nova anything about SpaceX, Starlink, rockets, or missions.
* Type `exit` or `quit` to stop the terminal chat.
