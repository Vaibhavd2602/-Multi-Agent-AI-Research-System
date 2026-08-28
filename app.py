"""
app.py — Streamlit UI for the Multi-Agent Research Pipeline

Drop this file in the SAME folder as pipeline.py, agents.py, tools.py, requirements.txt.
Run with:  streamlit run app.py

This file does NOT modify pipeline.py or agents.py. It reuses the exact same
agent/chain builders (build_search_agent, build_reader_agent, writer_chain,
critic_chain) so the underlying multi-agent logic is identical to what
pipeline.py does when run from the terminal — the UI just adds a polished,
step-by-step visual layer on top of it (progress per agent, live status,
tabs, downloadable report, etc.) instead of only printing to stdout.
"""

from datetime import datetime
import streamlit as st
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ──────────────────────────────────────────────────────────────────────────
# Page config
# ──────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────────
# Custom CSS — modern / clean / professional
# ──────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        html, body, [class*="css"]  {
            font-family: 'Inter', sans-serif;
        }
        .main {
            background: radial-gradient(circle at top left, #12141c 0%, #0b0c10 60%);
        }

        /* Hero header */
        .hero {
            padding: 2.2rem 2.4rem;
            border-radius: 18px;
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 45%, #ec4899 100%);
            box-shadow: 0 10px 40px rgba(99, 102, 241, 0.35);
            margin-bottom: 1.6rem;
        }
        .hero h1 {
            color: white;
            font-weight: 800;
            font-size: 2.1rem;
            margin: 0;
            letter-spacing: -0.5px;
        }
        .hero p {
            color: rgba(255,255,255,0.9);
            font-size: 1.02rem;
            margin-top: 0.4rem;
            margin-bottom: 0;
        }

        /* Agent badges */
        .agent-badge {
            display: inline-block;
            padding: 0.25rem 0.7rem;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 600;
            margin-bottom: 0.8rem;
            letter-spacing: 0.3px;
        }
        .badge-search { background: rgba(99,102,241,0.18); color: #a5b4fc; }
        .badge-reader { background: rgba(236,72,153,0.18); color: #f9a8d4; }
        .badge-writer { background: rgba(34,197,94,0.18); color: #86efac; }
        .badge-critic { background: rgba(245,158,11,0.18); color: #fcd34d; }

        div.stButton > button {
            border-radius: 10px;
            font-weight: 700;
            padding: 0.6rem 1.6rem;
            border: none;
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            color: white;
            transition: 0.2s ease;
        }
        div.stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 8px 20px rgba(139, 92, 246, 0.35);
        }

        section[data-testid="stSidebar"] {
            background: #0e0f14;
            border-right: 1px solid rgba(255,255,255,0.06);
        }

        .footer-note {
            text-align: center;
            color: rgba(255,255,255,0.35);
            font-size: 0.8rem;
            margin-top: 2rem;
        }

        .stTabs [data-baseweb="tab-list"] { gap: 6px; }
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px 8px 0 0;
            padding: 0.5rem 1.1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────────────────────────────────
# Session state
# ──────────────────────────────────────────────────────────────────────────
if "result_state" not in st.session_state:
    st.session_state.result_state = None
if "history" not in st.session_state:
    st.session_state.history = []
if "running" not in st.session_state:
    st.session_state.running = False

# ──────────────────────────────────────────────────────────────────────────
# Sidebar
# ──────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🧠 Research System")
    st.caption("Multi-agent pipeline: Search → Read → Write → Critique")
    st.markdown("---")
    st.markdown("### 🔧 Pipeline Stages")
    st.markdown(
        """
        1. **Search Agent** — finds recent, reliable sources
        2. **Reader Agent** — scrapes the best source in depth
        3. **Writer Chain** — drafts the final report
        4. **Critic Chain** — reviews & gives feedback
        """
    )
    st.markdown("---")
    st.markdown("### 🕘 Recent Topics")
    if st.session_state.history:
        for h in reversed(st.session_state.history[-8:]):
            st.markdown(f"- {h}")
    else:
        st.caption("No research run yet.")
    st.markdown("---")
    st.caption("Built on your existing `pipeline.py` — core agent logic is untouched.")

# ──────────────────────────────────────────────────────────────────────────
# Hero header
# ──────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero">
        <h1>🧠 Multi-Agent Research System</h1>
        <p>Enter a topic and let the Search, Reader, Writer & Critic agents collaborate to produce a reviewed report.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────────────────────────────────
# Input section
# ──────────────────────────────────────────────────────────────────────────
input_col, button_col = st.columns([4, 1])
with input_col:
    topic = st.text_input(
        "Research topic",
        placeholder="e.g. Impact of quantum computing on cryptography",
        label_visibility="collapsed",
    )
with button_col:
    start_clicked = st.button("🚀 Start Research", use_container_width=True, disabled=st.session_state.running)

st.markdown("<br>", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────
# Pipeline execution — same building blocks as pipeline.run_research_pipeline,
# just instrumented with live UI status per step.
# ──────────────────────────────────────────────────────────────────────────
def run_pipeline_with_ui(topic: str) -> dict:
    state = {}
    with st.status("Running multi-agent pipeline...", expanded=True) as status:
        # Step 1 — Search agent
        st.write("🔎 **Search Agent** is looking for recent, reliable sources...")
        search_agent = build_search_agent()
        search_result = search_agent.invoke(
            {"messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]}
        )
        state["search_results"] = search_result["messages"][-1].content
        st.write("✅ Search complete.")

        # Step 2 — Reader agent
        st.write("📖 **Reader Agent** is scraping the top resource for deeper content...")
        reader_agent = build_reader_agent()
        reader_result = reader_agent.invoke(
            {
                "messages": [
                    (
                        "user",
                        f"Based on the following search results about '{topic}', "
                        f"pick the most relevant URL and scrape it for deeper content.\n\n"
                        f"Search Results:\n{state['search_results'][:800]}",
                    )
                ]
            }
        )
        state["scraped_content"] = reader_result["messages"][-1].content
        st.write("✅ Scraping complete.")

        # Step 3 — Writer chain
        st.write("✍️ **Writer Chain** is drafting the report...")
        research_combined = (
            f"SEARCH RESULTS : \n {state['search_results']} \n\n"
            f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
        )
        state["report"] = writer_chain.invoke({"topic": topic, "research": research_combined})
        st.write("✅ Draft complete.")

        # Step 4 — Critic chain
        st.write("🧐 **Critic Chain** is reviewing the report...")
        state["feedback"] = critic_chain.invoke({"topic": topic, "report": state["report"]})
        st.write("✅ Review complete.")

        status.update(label="Pipeline finished successfully ✅", state="complete", expanded=False)

    return state


if start_clicked:
    if not topic or not topic.strip():
        st.warning("Please enter a research topic before starting.")
    else:
        st.session_state.running = True
        try:
            result = run_pipeline_with_ui(topic.strip())
            st.session_state.result_state = result
            st.session_state.history.append(topic.strip())
        except Exception as e:
            st.error(f"Pipeline failed: {e}")
        finally:
            st.session_state.running = False
        st.rerun()

# ──────────────────────────────────────────────────────────────────────────
# Results section
# ──────────────────────────────────────────────────────────────────────────
def as_text(x) -> str:
    """Normalize chain/agent outputs (str or objects with .content) to plain text."""
    if x is None:
        return ""
    if isinstance(x, str):
        return x
    return getattr(x, "content", str(x))


if st.session_state.result_state:
    state = st.session_state.result_state
    st.markdown("## 📊 Results")

    tab_report, tab_feedback, tab_search, tab_scraped = st.tabs(
        ["📝 Final Report", "🧐 Critic Feedback", "🔎 Search Results", "📖 Scraped Content"]
    )

    # NOTE: st.container(border=True) is used instead of manually opening/closing
    # a <div> across multiple st.markdown() calls. Each st.markdown() call gets
    # wrapped in its own isolated block by Streamlit, so a hand-written <div> that
    # opens in one call and closes in another never actually wraps the content in
    # between — it just auto-closes early, leaving the badge stuck in a tiny box
    # and the rest of the content unstyled below it. st.container(border=True)
    # avoids that entirely.
    with tab_report:
        with st.container(border=True):
            st.markdown('<span class="agent-badge badge-writer">WRITER CHAIN</span>', unsafe_allow_html=True)
            st.markdown(as_text(state.get("report", "")))
        report_text = as_text(state.get("report", ""))
        st.download_button(
            "⬇️ Download Report (.md)",
            data=report_text,
            file_name=f"research_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown",
        )

    with tab_feedback:
        with st.container(border=True):
            st.markdown('<span class="agent-badge badge-critic">CRITIC CHAIN</span>', unsafe_allow_html=True)
            st.markdown(as_text(state.get("feedback", "")))

    with tab_search:
        with st.container(border=True):
            st.markdown('<span class="agent-badge badge-search">SEARCH AGENT</span>', unsafe_allow_html=True)
            st.markdown(as_text(state.get("search_results", "")))

    with tab_scraped:
        with st.container(border=True):
            st.markdown('<span class="agent-badge badge-reader">READER AGENT</span>', unsafe_allow_html=True)
            st.markdown(as_text(state.get("scraped_content", "")))
else:
    st.info("👆 Enter a topic above and click **Start Research** to run the pipeline.")

st.markdown(
    '<div class="footer-note">Multi-Agent Research System · powered by your existing agents.py & pipeline.py</div>',
    unsafe_allow_html=True,
)
