# 🔬 ResearchMind — Multi-Agent AI Research System

**ResearchMind** is a multi-agent AI system built with **LangChain** and **LangGraph** that automates the entire research workflow — from web search to a polished, reviewed report — powered by four specialized AI agents working in sequence.

🔗 **Live Demo:** [agentic-research-ai.streamlit.app](https://agentic-research-ai.streamlit.app)

---

## ✨ Features

- 🔍 **Search Agent** — Finds recent, reliable sources on the web using the Tavily Search API.
- 📖 **Reader Agent** — Scrapes and extracts deep content from the most relevant source.
- ✍️ **Writer Chain** — Drafts a structured, professional research report (Introduction, Key Findings, Conclusion, Sources).
- 🧐 **Critic Chain** — Reviews the report for accuracy, clarity, and completeness, and provides constructive feedback.
- 🎨 **Modern Streamlit UI** — Clean, dark-themed interface with a live pipeline status tracker (`WAITING → RUNNING → DONE`).
- ⚡ **Fast & Free LLM inference** via [Groq](https://groq.com).

---

## 🧠 How It Works

```
User Topic
    │
    ▼
🔍 Search Agent  →  gathers recent web results (Tavily)
    │
    ▼
📖 Reader Agent  →  scrapes the most relevant URL for deeper content
    │
    ▼
✍️ Writer Chain  →  drafts a structured research report
    │
    ▼
🧐 Critic Chain  →  reviews the report and gives feedback
    │
    ▼
📄 Final Report + Critic Feedback
```

---

## 🛠️ Tech Stack

| Layer            | Technology                              |
|-------------------|------------------------------------------|
| LLM Orchestration | LangChain, LangGraph                    |
| LLM Provider      | Groq (`qwen/qwen3.6-27b`)                |
| Web Search        | Tavily API                              |
| Web Scraping      | BeautifulSoup4, Requests, lxml           |
| UI                | Streamlit                               |
| Environment       | Python 3.14, python-dotenv               |

---

## 📁 Project Structure

```
├── agents.py          # Agent definitions (search, reader) + writer & critic chains
├── tools.py            # Custom tools: web_search, scrape_url
├── pipeline.py          # Core orchestration logic (CLI entry point)
├── app.py               # Streamlit UI, wired to the pipeline
├── requirements.txt     # Python dependencies
├── .gitignore            # Excludes .venv, .env, __pycache__
└── README.md
```

---

## 🚀 Getting Started (Local Setup)

### 1. Clone the repository
```bash
git clone https://github.com/Vaibhavd2602/-Multi-Agent-AI-Research-System.git
cd -Multi-Agent-AI-Research-System
```

### 2. Create and activate a virtual environment
```bash
python -m venv .venv
# Windows
.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

### 5. Run it

**As a CLI:**
```bash
python pipeline.py
```

**As a web app:**
```bash
streamlit run app.py
```

---

## ☁️ Deployment

This app is deployed on **Streamlit Community Cloud**. API keys are stored securely using Streamlit's built-in **Secrets** manager (never committed to GitHub).

To deploy your own copy:
1. Push this repo to your GitHub account (make sure `.env` is in `.gitignore`).
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**.
3. Select your repo, branch `main`, and main file `app.py`.
4. Add your API keys under **Advanced settings → Secrets**:
   ```toml
   GROQ_API_KEY = "your_key"
   TAVILY_API_KEY = "your_key"
   ```
5. Click **Deploy**.

---

## 📌 Notes

- Groq's free tier has daily token limits per model — if you hit a rate limit, the app will show an error asking you to retry after a short wait.
- The system prints intermediate step outputs (search results, scraped content) for transparency and debugging.

---

## 📄 License

This project is open-source and available under the MIT License.
