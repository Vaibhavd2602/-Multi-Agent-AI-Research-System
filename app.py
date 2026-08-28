"""
streamlit_app.py
-----------------
Modern, professional Streamlit front-end for the multi-agent research
pipeline defined in `pipeline.py`.

This file does NOT modify pipeline.py, agents.py, or tools.py in any way.
It simply imports `run_research_pipeline` and renders a polished UI around
it, including a live log stream (captured from the existing print()
statements) so the user can watch the Search -> Read -> Write -> Critique
stages happen in real time.

Run with:
    streamlit run streamlit_app.py
"""

import io
import sys
import contextlib
import datetime as dt

import streamlit as st

from pipeline import run_research_pipeline


# ----------------------------------------------------------------------
# Page config (must be the first Streamlit call)
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ----------------------------------------------------------------------
# Custom CSS — modern / professional theme
# ----------------------------------------------------------------------
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* Hide default Streamlit chrome for a cleaner look */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1100px;
        }

        /* Hero header */
        .hero {
            background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #db2777 100%);
            padding: 2.4rem 2.2rem;
            border-radius: 18px;
            margin-bottom: 1.6rem;
            box-shadow: 0 10px 30px rgba(79, 70, 229, 0.25);
        }
        .hero h1 {
            color: #ffffff;
            font-size: 2.1rem;
            font-weight: 800;
            margin: 0;
        }
        .hero p {
            color: rgba(255,255,255,0.9);
            font-size: 1.02rem;
            margin-top: 0.5rem;
            margin-bottom: 0;
        }

        /* Agent pipeline chips */
        .pipeline-row {
            display: flex;
            gap: 0.6rem;
            flex-wrap: wrap;
            margin-top: 1rem;
        }
        .pipeline-chip {
            background: rgba(255,255,255,0.18);
            color: #fff;
            padding: 0.35rem 0.85rem;
            border-radius: 999px;
            font-size: 0.82rem;
            font-weight: 600;
            border: 1px solid rgba(255,255,255,0.35);
        }

        /* Section cards */
        .card {
            background: #ffffff;
            border: 1px solid #ececf3;
            border-radius: 16px;
            padding: 1.6rem 1.8rem;
            box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04);
            margin-bottom: 1.2rem;
        }
        .card h3 {
            margin-top: 0;
            font-weight: 700;
        }

        .stButton>button {
            background: linear-gradient(135deg, #4f46e5, #7c3aed);
            color: white;
            font-weight: 600;
            border: none;
            border-radius: 10px;
            padding: 0.6rem 1.4rem;
            transition: all 0.15s ease;
            width: 100%;
        }
        .stButton>button:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 16px rgba(124, 58, 237, 0.35);
        }

        .log-box {
            background: #0f172a;
            color: #a7f3d0;
            font-family: 'SFMono-Regular', Consolas, monospace;
            font-size: 0.82rem;
            padding: 1rem 1.1rem;
            border-radius: 12px;
            height: 260px;
            overflow-y: auto;
            white-space: pre-wrap;
            line-height: 1.5;
        }

        .badge-done {
            background: #dcfce7;
            color: #15803d;
            padding: 0.15rem 0.6rem;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 700;
        }

        section[data-testid="stSidebar"] {
            background: #0f172a;
        }
        section[data-testid="stSidebar"] * {
            color: #e2e8f0 !important;
        }
        section[data-testid="stSidebar"] .stTextInput input,
        section[data-testid="stSidebar"] textarea {
            color: #0f172a !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ----------------------------------------------------------------------
# Session state
# ----------------------------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []   # list of {topic, timestamp, state}
if "result" not in st.session_state:
    st.session_state.result = None
if "running" not in st.session_state:
    st.session_state.running = False


# ----------------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🧠 Research Console")
    st.caption("Multi-Agent AI Research System")
    st.divider()

    topic_input = st.text_area(
        "Research topic",
        placeholder="e.g. Impact of quantum computing on cybersecurity",
        height=100,
    )

    example_topics = [
        "Latest advances in solid-state batteries",
        "How AI agents are changing software engineering",
        "Global trends in renewable energy investment",
    ]
    st.caption("Quick examples")
    for ex in example_topics:
        if st.button(ex, key=f"ex_{ex}", use_container_width=True):
            topic_input = ex
            st.session_state["_prefill"] = ex

    if st.session_state.get("_prefill"):
        topic_input = st.session_state["_prefill"]

    st.divider()
    run_clicked = st.button("🚀 Run Research", use_container_width=True, disabled=st.session_state.running)

    st.divider()
    st.caption("Pipeline stages")
    st.markdown(
        "1. 🔎 **Search Agent**\n"
        "2. 📖 **Reader Agent**\n"
        "3. ✍️ **Writer Chain**\n"
        "4. 🧐 **Critic Chain**"
    )

    if st.session_state.history:
        st.divider()
        st.caption("Recent runs")
        for item in reversed(st.session_state.history[-5:]):
            st.markdown(f"- {item['timestamp']} — {item['topic'][:40]}")


# ----------------------------------------------------------------------
# Hero header
# ----------------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <h1>Multi-Agent Research System</h1>
        <p>Search, read, write, and critique — an autonomous agent pipeline that
        turns any topic into a polished, fact-checked report.</p>
        <div class="pipeline-row">
            <span class="pipeline-chip">🔎 Search Agent</span>
            <span class="pipeline-chip">📖 Reader Agent</span>
            <span class="pipeline-chip">✍️ Writer Chain</span>
            <span class="pipeline-chip">🧐 Critic Chain</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ----------------------------------------------------------------------
# Live log capture helper
# ----------------------------------------------------------------------
class _StreamlitLogStream(io.TextIOBase):
    """Redirects print() output from pipeline.py into a live Streamlit box."""

    def __init__(self, placeholder):
        self.placeholder = placeholder
        self.buffer = ""

    def write(self, s):
        if s:
            self.buffer += s
            self.placeholder.markdown(
                f'<div class="log-box">{self.buffer[-6000:]}</div>',
                unsafe_allow_html=True,
            )
        return len(s)

    def flush(self):
        pass


# ----------------------------------------------------------------------
# Run pipeline
# ----------------------------------------------------------------------
if run_clicked:
    if not topic_input or not topic_input.strip():
        st.warning("Please enter a research topic before running the pipeline.")
    else:
        st.session_state.running = True
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### ⚙️ Pipeline in progress")
        status = st.status("Initializing agents...", expanded=True)
        log_placeholder = status.empty()
        st.markdown("</div>", unsafe_allow_html=True)

        try:
            with contextlib.redirect_stdout(_StreamlitLogStream(log_placeholder)):
                result_state = run_research_pipeline(topic_input.strip())

            status.update(label="✅ Research pipeline completed", state="complete", expanded=False)
            st.session_state.result = result_state
            st.session_state.history.append(
                {
                    "topic": topic_input.strip(),
                    "timestamp": dt.datetime.now().strftime("%H:%M:%S"),
                    "state": result_state,
                }
            )
            st.toast("Research report ready!", icon="✅")

        except Exception as e:
            status.update(label="❌ Pipeline failed", state="error", expanded=True)
            st.error(f"Something went wrong while running the pipeline:\n\n**{e}**")
        finally:
            st.session_state.running = False


# ----------------------------------------------------------------------
# Results
# ----------------------------------------------------------------------
if st.session_state.result:
    state = st.session_state.result

    st.markdown("### 📊 Results")

    col1, col2, col3, col4 = st.columns(4)
    for col, label in zip(
        (col1, col2, col3, col4),
        ("Search", "Read", "Write", "Critique"),
    ):
        with col:
            st.markdown(
                f'<div class="card" style="text-align:center;">'
                f'<span class="badge-done">✓ Done</span><br><br>'
                f'<b>{label}</b></div>',
                unsafe_allow_html=True,
            )

    tab_report, tab_critic, tab_search, tab_scrape = st.tabs(
        ["📄 Final Report", "🧐 Critic Feedback", "🔎 Search Results", "📖 Scraped Content"]
    )

    with tab_report:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        report_text = state.get("report", "")
        report_text = getattr(report_text, "content", report_text)
        st.markdown(str(report_text))
        st.markdown("</div>", unsafe_allow_html=True)
        st.download_button(
            "⬇️ Download report (.md)",
            data=str(report_text),
            file_name="research_report.md",
            mime="text/markdown",
            use_container_width=True,
        )

    with tab_critic:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        feedback_text = state.get("feedback", "")
        feedback_text = getattr(feedback_text, "content", feedback_text)
        st.markdown(str(feedback_text))
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_search:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.text(state.get("search_results", ""))
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_scrape:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.text(state.get("scraped_content", ""))
        st.markdown("</div>", unsafe_allow_html=True)

else:
    st.markdown(
        """
        <div class="card" style="text-align:center; padding:3rem 1rem;">
            <h3>👋 Enter a topic in the sidebar and click <i>Run Research</i></h3>
            <p style="color:#64748b;">Your multi-agent pipeline will search the web, read the best
            source, draft a report, and have it reviewed by a critic agent — all in one click.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
