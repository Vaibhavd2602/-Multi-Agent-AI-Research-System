"""
Multi-Agent AI Research System — "ResearchMind" Streamlit UI
--------------------------------------------------------------
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
    page_title="ResearchMind - AI Research Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ----------------------------------------------------------------------------
# Session state defaults
# ----------------------------------------------------------------------------
if "topic_input" not in st.session_state:
    st.session_state.topic_input = ""
if "result" not in st.session_state:
    st.session_state.result = None
if "steps_done" not in st.session_state:
    st.session_state.steps_done = 0  # 0 = none, 4 = all done

SUGGESTIONS = ["LLM agents 2025", "CRISPR gene editing", "Fusion energy progress"]

# ----------------------------------------------------------------------------
# Global CSS — dark, bold, editorial style
# ----------------------------------------------------------------------------
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Archivo:wght@700;800;900&family=Inter:wght@400;500;600&display=swap');

        html, body, [class*="css"]  {
            font-family: 'Inter', sans-serif;
        }

        #MainMenu, footer, header {visibility: hidden;}
        .block-container {
            padding-top: 2.5rem;
            padding-bottom: 3rem;
            max-width: 1200px;
        }
        .stApp {
            background: #0a0a0a;
        }

        /* Hero */
        .overline {
            text-align: center;
            color: #f5811f;
            letter-spacing: 0.35em;
            font-size: 0.78rem;
            font-weight: 600;
            margin-bottom: 0.8rem;
        }
        .hero-title {
            text-align: center;
            font-family: 'Archivo', sans-serif;
            font-weight: 900;
            font-size: 5.2rem;
            line-height: 1.02;
            letter-spacing: -0.02em;
            color: #f4efe6;
            margin: 0 0 1.3rem 0;
        }
        .hero-title .accent { color: #f5811f; }
        .subtitle {
            text-align: center;
            color: #9ca3af;
            font-size: 1.08rem;
            max-width: 640px;
            margin: 0 auto 2.6rem auto;
            line-height: 1.6;
        }
        .divider {
            border-top: 1px solid #262626;
            margin: 0 0 2.6rem 0;
        }

        /* Section labels */
        .field-label {
            color: #f5811f;
            letter-spacing: 0.2em;
            font-size: 0.75rem;
            font-weight: 700;
            margin-bottom: 0.6rem;
        }

        /* Topic input */
        div[data-testid="stTextInput"] input {
            background: #141414 !important;
            border: 1px solid #2b2b2b !important;
            border-radius: 10px !important;
            color: #f4efe6 !important;
            font-size: 1rem !important;
            padding: 0.85rem 1rem !important;
        }
        div[data-testid="stTextInput"] input:focus {
            border: 1px solid #f5811f !important;
            box-shadow: 0 0 0 1px #f5811f33 !important;
        }

        /* Run button */
        div.stButton > button[kind="primary"] {
            width: 100%;
            background: linear-gradient(90deg, #f5811f, #f2b127);
            color: #0a0a0a;
            font-weight: 700;
            font-size: 1.02rem;
            border: none;
            border-radius: 10px;
            padding: 0.85rem 1rem;
            box-shadow: 0 8px 24px rgba(245, 129, 31, 0.25);
        }
        div.stButton > button[kind="primary"]:hover {
            opacity: 0.93;
        }

        /* Suggestion pills */
        .try-label {
            color: #6b7280;
            font-size: 0.75rem;
            letter-spacing: 0.15em;
            font-weight: 600;
            margin: 1.4rem 0 0.7rem 0;
        }
        div.stButton > button[kind="secondary"] {
            background: #141414;
            border: 1px solid #2b2b2b;
            color: #d1d5db;
            border-radius: 999px;
            font-size: 0.85rem;
            padding: 0.4rem 1rem;
        }
        div.stButton > button[kind="secondary"]:hover {
            border: 1px solid #f5811f;
            color: #f5811f;
        }

        /* Pipeline heading */
        .pipeline-heading {
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700;
            font-size: 1.6rem;
            color: #f4efe6;
            margin-bottom: 1.1rem;
        }

        /* Pipeline card */
        .pipeline-card {
            background: #121212;
            border: 1px solid #262626;
            border-left: 4px solid #3a3a3a;
            border-radius: 10px;
            padding: 1.1rem 1.3rem;
            margin-bottom: 1rem;
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
        }
        .pipeline-card.done { border-left: 4px solid #22c55e; }
        .pipeline-card.active { border-left: 4px solid #f5811f; }

        .step-num {
            color: #f5811f;
            font-weight: 700;
            font-size: 0.85rem;
            margin-right: 0.5rem;
        }
        .step-title {
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700;
            font-size: 1.05rem;
            color: #f4efe6;
            display: inline;
        }
        .step-desc {
            color: #8b8b8b;
            font-size: 0.88rem;
            margin-top: 0.35rem;
        }
        .status-badge {
            font-size: 0.75rem;
            font-weight: 700;
            padding: 0.2rem 0.6rem;
            border-radius: 999px;
            white-space: nowrap;
        }
        .status-done { color: #22c55e; background: #14532d33; border: 1px solid #22c55e55; }
        .status-active { color: #f5811f; background: #7c2d1233; border: 1px solid #f5811f55; }
        .status-pending { color: #6b7280; background: #1f1f1f; border: 1px solid #2b2b2b; }

        /* Result cards */
        .result-card {
            background: #121212;
            border: 1px solid #262626;
            border-radius: 14px;
            padding: 1.6rem 1.8rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Hero
# ----------------------------------------------------------------------------
st.markdown('<div class="overline">MULTI-AGENT AI SYSTEM</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-title">Research<span class="accent">Mind</span></div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="subtitle">Four specialized AI agents collaborate — searching, scraping, '
    'writing, and critiquing — to deliver a polished research report on any topic.</div>',
    unsafe_allow_html=True,
)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# Main layout: left = input, right = pipeline
# ----------------------------------------------------------------------------
left, right = st.columns([1.05, 0.95], gap="large")

with left:
    st.markdown('<div class="field-label">RESEARCH TOPIC</div>', unsafe_allow_html=True)
    topic = st.text_input(
        "Research topic",
        value=st.session_state.topic_input,
        placeholder="Quantum computing breakthroughs in 2025",
        label_visibility="collapsed",
        key="topic_box",
    )

    run_clicked = st.button("⚡  Run Research Pipeline", type="primary", use_container_width=True)

    st.markdown('<div class="try-label">TRY →</div>', unsafe_allow_html=True)
    pill_cols = st.columns(len(SUGGESTIONS))
    for i, sug in enumerate(SUGGESTIONS):
        with pill_cols[i]:
            if st.button(sug, key=f"sug_{i}", type="secondary", use_container_width=True):
                st.session_state.topic_input = sug
                st.rerun()

with right:
    st.markdown('<div class="pipeline-heading">Pipeline</div>', unsafe_allow_html=True)

    steps = [
        ("01", "Search Agent", "Gathers recent web information"),
        ("02", "Reader Agent", "Scrapes & extracts deep content"),
        ("03", "Writer Chain", "Drafts the full research report"),
        ("04", "Critic Chain", "Reviews and refines the final report"),
    ]

    for idx, (num, title, desc) in enumerate(steps):
        step_number = idx + 1
        if st.session_state.steps_done >= step_number:
            card_class, badge_class, badge_text = "done", "status-done", "✓ DONE"
        elif st.session_state.steps_done == step_number - 1 and st.session_state.get("running", False):
            card_class, badge_class, badge_text = "active", "status-active", "RUNNING"
        else:
            card_class, badge_class, badge_text = "", "status-pending", "PENDING"

        st.markdown(
            f"""
            <div class="pipeline-card {card_class}">
                <div>
                    <span class="step-num">{num}</span><span class="step-title">{title}</span>
                    <div class="step-desc">{desc}</div>
                </div>
                <div class="status-badge {badge_class}">{badge_text}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ----------------------------------------------------------------------------
# Run pipeline
# ----------------------------------------------------------------------------
if run_clicked:
    final_topic = topic.strip()
    if not final_topic:
        st.warning("Please enter a topic before running the pipeline.")
    else:
        st.session_state.running = True
        st.session_state.steps_done = 0
        placeholder = st.empty()

        with st.spinner("Agents are working..."):
            try:
                st.session_state.steps_done = 1
                time.sleep(0.2)
                result = run_research_pipeline(final_topic)
                st.session_state.steps_done = 4
                st.session_state.result = result
                st.session_state.topic_input = final_topic
            except Exception as e:
                st.session_state.running = False
                st.error(f"⚠️ Pipeline failed: {e}")
                result = None

        st.session_state.running = False
        if st.session_state.result:
            st.rerun()

# ----------------------------------------------------------------------------
# Results
# ----------------------------------------------------------------------------
if st.session_state.result:
    result = st.session_state.result
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="pipeline-heading">📄 Results</div>', unsafe_allow_html=True)

    tab_report, tab_critic, tab_search, tab_scraped = st.tabs(
        ["Final Report", "Critic Feedback", "Search Results", "Scraped Content"]
    )

    with tab_report:
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown(result.get("report", "_No report generated._"))
        st.markdown("</div>", unsafe_allow_html=True)
        st.download_button(
            "⬇️ Download report (.md)",
            data=result.get("report", ""),
            file_name="research_report.md",
            mime="text/markdown",
        )

    with tab_critic:
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown(result.get("feedback", "_No feedback generated._"))
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_search:
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown(result.get("search_results", "_No search results._"))
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_scraped:
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown(result.get("scraped_content", "_No scraped content._"))
        st.markdown("</div>", unsafe_allow_html=True)