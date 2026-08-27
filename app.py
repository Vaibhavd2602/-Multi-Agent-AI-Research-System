"""
Multi-Agent AI Research System — Streamlit UI
------------------------------------------------
Drop this file in the same folder as pipeline.py, agents.py, tools.py, and .env,
then run:  streamlit run app.py
"""

import time
import streamlit as st
from pipeline import run_research_pipeline

# ----------------------------------------------------------------------------
# Page config
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Multi-Agent AI Research System",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------------
# Custom CSS — modern, clean, professional
# ----------------------------------------------------------------------------
st.markdown(
    """
    <style>
        /* Overall page */
        .main {
            background-color: #0e1117;
        }

        /* Hero header — simple, clean, no big gradient box */
        .hero {
            padding: 0.5rem 0 1.6rem 0;
            border-bottom: 1px solid #262c36;
            margin-bottom: 1.8rem;
        }
        .hero h1 {
            color: #f5f1ea;
            font-size: 2rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
        }
        .hero p {
            color: #9ca3af;
            font-size: 0.95rem;
            margin: 0;
        }
        .hero p .arrow {
            color: #f97316;
            font-weight: 700;
        }

        /* Step pill badges */
        .step-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.35rem 0.9rem;
            border-radius: 999px;
            font-size: 0.85rem;
            font-weight: 600;
            margin-right: 0.5rem;
            margin-bottom: 0.4rem;
        }
        .badge-search   { background: #1e3a8a33; color: #93c5fd; border: 1px solid #3b82f680; }
        .badge-reader    { background: #78350f33; color: #fcd34d; border: 1px solid #f59e0b80; }
        .badge-writer    { background: #14532d33; color: #86efac; border: 1px solid #22c55e80; }
        .badge-critic    { background: #7f1d1d33; color: #fca5a5; border: 1px solid #ef444480; }

        /* Card container */
        .card {
            background: #161b22;
            border: 1px solid #262c36;
            border-radius: 16px;
            padding: 1.4rem 1.6rem;
            margin-bottom: 1.2rem;
        }
        .card h3 {
            margin-top: 0;
        }

        /* Report card */
        .report-card {
            background: linear-gradient(145deg, #161b22 0%, #1a1f2b 100%);
            border: 1px solid #2f3542;
            border-radius: 18px;
            padding: 1.8rem;
        }

        /* Footer */
        .footer {
            text-align: center;
            color: #6b7280;
            font-size: 0.85rem;
            margin-top: 2.5rem;
            padding-top: 1rem;
            border-top: 1px solid #262c36;
        }

        /* Buttons */
        div.stButton > button {
            border-radius: 10px;
            font-weight: 600;
            padding: 0.55rem 1.4rem;
            background: linear-gradient(90deg, #10b981, #0ea5e9);
            color: white;
            border: none;
        }
        div.stButton > button:hover {
            opacity: 0.92;
            border: none;
        }

        /* Field label */
        .field-label {
            color: #d1d5db;
            font-size: 0.9rem;
            font-weight: 600;
            margin-bottom: 0.4rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ How it works")
    st.markdown(
        """
        This system runs **4 AI agents** in sequence:

        <div class="step-badge badge-search">🔍 Search Agent</div>
        Finds recent, reliable sources on the web.

        <div class="step-badge badge-reader">📖 Reader Agent</div>
        Scrapes the most relevant page for deep content.

        <div class="step-badge badge-writer">✍️ Writer Chain</div>
        Drafts a structured research report.

        <div class="step-badge badge-critic">🧐 Critic Chain</div>
        Reviews the report for accuracy & clarity.
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.markdown("### 📌 Notes")
    st.caption(
        "Make sure your `.env` file (with GROQ_API_KEY / TAVILY_API_KEY) "
        "is in the same folder as this app before running."
    )
    st.markdown("---")
    st.caption("Built with LangChain · LangGraph · Streamlit")

# ----------------------------------------------------------------------------
# Hero header
# ----------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <h1>🔍 Multi-Agent AI Research System</h1>
        <p>Powered by LangChain — Search Agent <span class="arrow">→</span> Reader Agent <span class="arrow">→</span> Writer Chain <span class="arrow">→</span> Critic Chain</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Input section
# ----------------------------------------------------------------------------
st.markdown('<div class="field-label">Enter a research topic</div>', unsafe_allow_html=True)
topic = st.text_input(
    "Research topic",
    placeholder="e.g. Latest developments in AI regulation 2026",
    label_visibility="collapsed",
)
run_clicked = st.button("🚀 Run Research Pipeline")

# ----------------------------------------------------------------------------
# Run pipeline
# ----------------------------------------------------------------------------
if run_clicked:
    if not topic.strip():
        st.warning("Please enter a topic before running the pipeline.")
    else:
        status_box = st.status("Starting the research pipeline...", expanded=True)
        try:
            status_box.write("🔍 **Search agent** is gathering recent sources...")
            time.sleep(0.3)

            result = run_research_pipeline(topic)

            status_box.write("📖 Reader agent scraped the top resource.")
            status_box.write("✍️ Writer chain drafted the report.")
            status_box.write("🧐 Critic chain reviewed the report.")
            status_box.update(label="Research complete!", state="complete", expanded=False)

            st.session_state["result"] = result
            st.session_state["topic"] = topic

        except Exception as e:
            status_box.update(label="Something went wrong", state="error", expanded=True)
            st.error(f"⚠️ Pipeline failed: {e}")

# ----------------------------------------------------------------------------
# Results
# ----------------------------------------------------------------------------
if "result" in st.session_state:
    result = st.session_state["result"]
    topic_used = st.session_state.get("topic", "")

    st.markdown("## 📄 Results")
    st.caption(f"Topic: **{topic_used}**")

    tab_report, tab_critic, tab_search, tab_scraped = st.tabs(
        ["📝 Final Report", "🧐 Critic Feedback", "🔍 Search Results", "📖 Scraped Content"]
    )

    with tab_report:
        st.markdown('<div class="report-card">', unsafe_allow_html=True)
        st.markdown(result.get("report", "_No report generated._"))
        st.markdown("</div>", unsafe_allow_html=True)

        st.download_button(
            "⬇️ Download report (.md)",
            data=result.get("report", ""),
            file_name=f"{topic_used.replace(' ', '_')}_report.md",
            mime="text/markdown",
        )

    with tab_critic:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(result.get("feedback", "_No feedback generated._"))
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_search:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(result.get("search_results", "_No search results._"))
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_scraped:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(result.get("scraped_content", "_No scraped content._"))
        st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# Footer
# ----------------------------------------------------------------------------
st.markdown(
    """
    <div class="footer">
        Multi-Agent AI Research System · Search → Read → Write → Critique
    </div>
    """,
    unsafe_allow_html=True,
)