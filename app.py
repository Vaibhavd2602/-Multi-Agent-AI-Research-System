"""
app.py — Streamlit UI for the Multi-Agent Research Pipeline ("ResearchMind" theme)

Drop this file in the SAME folder as pipeline.py, agents.py, tools.py, requirements.txt.
Run with:  streamlit run app.py

Does NOT modify pipeline.py or agents.py — it reuses the exact same
agent/chain builders (build_search_agent, build_reader_agent, writer_chain,
critic_chain), just wrapped with a polished visual layer and live per-agent
status instead of terminal prints.
"""

from datetime import datetime

import streamlit as st

from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ──────────────────────────────────────────────────────────────────────────
# Page config
# ──────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind · AI Research Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ──────────────────────────────────────────────────────────────────────────
# Theme — near-black background + amber/orange accent, matching the mock
# ──────────────────────────────────────────────────────────────────────────
ACCENT = "#f7a53b"
ACCENT_SOFT = "#ffb454"
BG = "#08090c"
CARD = "#12141c"
CARD_BORDER = "rgba(255,255,255,0.08)"
MUTED = "#9aa3b2"

st.markdown(
    f"""
    <style>
        .stApp {{ background: {BG}; }}
        #MainMenu, footer, header {{ visibility: hidden; }}
        .block-container {{ padding-top: 2.2rem; max-width: 1180px; }}

        .eyebrow {{ color: {ACCENT}; font-size: 0.8rem; letter-spacing: 3px; margin-bottom: 0.5rem; }}
        .hero-title {{ font-size: 4.2rem; font-weight: 900; line-height: 1; margin: 0; }}
        .hero-title .accent {{ color: {ACCENT}; }}
        .hero-sub {{ color: #dbe1ea; font-size: 1.15rem; max-width: 780px; margin-top: 1rem; }}
        .hero-divider {{ border: none; border-top: 1px solid {CARD_BORDER}; margin: 2rem 0; }}

        .section-label {{ color: {ACCENT}; font-size: 0.78rem; letter-spacing: 2px; font-weight: 600; margin-bottom: 0.6rem; }}
        .pipeline-heading {{ font-size: 1.5rem; font-weight: 800; color: white; margin-bottom: 1rem; }}

        div[data-testid="stTextInput"] input {{
            background: {CARD} !important; border: 1px solid {CARD_BORDER} !important;
            border-radius: 12px !important; color: white !important; padding: 0.9rem 1.1rem !important;
        }}
        div[data-testid="stTextInput"] input:focus {{ border-color: {ACCENT} !important; }}

        div.stButton > button {{
            width: 100%; border-radius: 12px; font-weight: 700; border: none;
            background: {ACCENT}; color: #1a1206; padding: 0.85rem 1.3rem;
        }}
        div.stButton > button:disabled {{ opacity: 0.5; }}

        .pill-row div.stButton > button {{
            background: {CARD}; color: #d1d5db; font-weight: 500; font-size: 0.85rem;
            padding: 0.4rem 0.9rem; border: 1px solid {CARD_BORDER}; width: auto;
        }}

        .pcard {{ background: {CARD}; border: 1px solid {CARD_BORDER}; border-radius: 14px; padding: 1.1rem 1.3rem; margin-bottom: 0.9rem; }}
        .pcard.active {{ border-color: {ACCENT}; }}
        .pcard.done {{ border-color: rgba(34,197,94,0.4); }}
        .pcard-top {{ display: flex; justify-content: space-between; align-items: center; }}
        .pcard-num {{ color: {ACCENT}; font-weight: 700; font-size: 0.85rem; margin-right: 0.5rem; }}
        .pcard-title {{ font-weight: 700; color: white; }}
        .pcard-desc {{ color: {MUTED}; font-size: 0.87rem; margin-top: 0.3rem; }}
        .status-badge {{ font-size: 0.7rem; font-weight: 700; letter-spacing: 1px; padding: 0.25rem 0.6rem; border-radius: 999px; }}
        .status-waiting {{ background: rgba(255,255,255,0.06); color: {MUTED}; }}
        .status-running {{ background: rgba(247,165,59,0.16); color: {ACCENT}; }}
        .status-done {{ background: rgba(34,197,94,0.15); color: #4ade80; }}

        .rcard {{ background: {CARD}; border: 1px solid {CARD_BORDER}; border-radius: 16px; padding: 1.4rem 1.6rem; }}
        .agent-badge {{ display: inline-block; padding: 0.25rem 0.7rem; border-radius: 999px; font-size: 0.75rem; font-weight: 700; margin-bottom: 0.8rem; }}
        .badge-search {{ background: rgba(99,102,241,0.16); color: #a5b4fc; }}
        .badge-reader {{ background: rgba(236,72,153,0.16); color: #f9a8d4; }}
        .badge-writer {{ background: rgba(247,165,59,0.16); color: {ACCENT}; }}
        .badge-critic {{ background: rgba(34,197,94,0.16); color: #86efac; }}

        .stTabs [aria-selected="true"] {{ color: {ACCENT} !important; }}
        .footer-note {{ text-align: center; color: rgba(255,255,255,0.25); font-size: 0.78rem; margin-top: 3rem; }}
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
if "topic_input" not in st.session_state:
    st.session_state.topic_input = ""

SUGGESTIONS = ["LLM agents 2025", "Quantum computing breakthroughs", "Future of solid-state batteries"]

PIPELINE_STEPS = [
    ("01", "Search Agent", "Gathers recent web information"),
    ("02", "Reader Agent", "Scrapes & extracts deep content"),
    ("03", "Writer Chain", "Drafts the polished report"),
    ("04", "Critic Chain", "Reviews and gives feedback"),
]

# ──────────────────────────────────────────────────────────────────────────
# Hero
# ──────────────────────────────────────────────────────────────────────────
st.markdown('<div class="eyebrow">MULTI-AGENT AI SYSTEM</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-title">Research<span class="accent">Mind</span></div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="hero-sub">Four specialized AI agents collaborate — searching, scraping, writing, '
    'and critiquing — to deliver a polished research report on any topic.</div>',
    unsafe_allow_html=True,
)
st.markdown('<hr class="hero-divider">', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────
# Main layout — left: input / right: pipeline preview
# ──────────────────────────────────────────────────────────────────────────
left, right = st.columns([1.15, 1], gap="large")

with left:
    st.markdown('<div class="section-label">RESEARCH TOPIC</div>', unsafe_allow_html=True)

    topic = st.text_input(
        "Research topic",
        value=st.session_state.topic_input,
        placeholder="e.g. Quantum computing breakthroughs in 2025",
        label_visibility="collapsed",
        key="topic_box",
    )

    start_clicked = st.button(
        "⚡ Run Research Pipeline",
        use_container_width=True,
        disabled=st.session_state.running,
    )

    st.markdown('<div class="section-label" style="margin-top:1.4rem;">TRY →</div>', unsafe_allow_html=True)
    st.markdown('<div class="pill-row">', unsafe_allow_html=True)
    pcols = st.columns(len(SUGGESTIONS))
    for i, s in enumerate(SUGGESTIONS):
        with pcols[i]:
            if st.button(s, key=f"sugg_{i}", disabled=st.session_state.running):
                st.session_state.topic_input = s
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.history:
        st.markdown('<div class="section-label" style="margin-top:1.6rem;">RECENT</div>', unsafe_allow_html=True)
        st.caption(" · ".join(reversed(st.session_state.history[-5:])))

with right:
    st.markdown('<div class="pipeline-heading">Pipeline</div>', unsafe_allow_html=True)
    pipeline_placeholder = st.container()

    def render_pipeline(active_index=None, done_indices=()):
        """active_index: index currently RUNNING, done_indices: set of finished indices."""
        html = ""
        for i, (num, title, desc) in enumerate(PIPELINE_STEPS):
            if i in done_indices:
                cls, badge_cls, badge_txt = "done", "status-done", "DONE"
            elif i == active_index:
                cls, badge_cls, badge_txt = "active", "status-running", "RUNNING"
            else:
                cls, badge_cls, badge_txt = "", "status-waiting", "WAITING"
            html += f"""
            <div class="pcard {cls}">
                <div class="pcard-top">
                    <div><span class="pcard-num">{num}</span><span class="pcard-title">{title}</span></div>
                    <span class="status-badge {badge_cls}">{badge_txt}</span>
                </div>
                <div class="pcard-desc">{desc}</div>
            </div>
            """
        pipeline_placeholder.markdown(html, unsafe_allow_html=True)

    render_pipeline()

# ──────────────────────────────────────────────────────────────────────────
# Pipeline execution — same building blocks as pipeline.run_research_pipeline,
# instrumented with live pipeline-card status updates.
# ──────────────────────────────────────────────────────────────────────────
def run_pipeline_with_ui(topic: str) -> dict:
    state = {}

    render_pipeline(active_index=0)
    search_agent = build_search_agent()
    search_result = search_agent.invoke(
        {"messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]}
    )
    state["search_results"] = search_result["messages"][-1].content
    render_pipeline(active_index=1, done_indices={0})

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
    render_pipeline(active_index=2, done_indices={0, 1})

    research_combined = (
        f"SEARCH RESULTS : \n {state['search_results']} \n\n"
        f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
    )
    state["report"] = writer_chain.invoke({"topic": topic, "research": research_combined})
    render_pipeline(active_index=3, done_indices={0, 1, 2})

    state["feedback"] = critic_chain.invoke({"topic": topic, "report": state["report"]})
    render_pipeline(done_indices={0, 1, 2, 3})

    return state


if start_clicked:
    if not topic or not topic.strip():
        st.warning("Please enter a research topic before starting.")
    else:
        st.session_state.running = True
        try:
            with st.spinner(""):
                result = run_pipeline_with_ui(topic.strip())
            st.session_state.result_state = result
            st.session_state.history.append(topic.strip())
        except Exception as e:
            st.error(f"Pipeline failed: {e}")
        finally:
            st.session_state.running = False

# ──────────────────────────────────────────────────────────────────────────
# Results section
# ──────────────────────────────────────────────────────────────────────────
def as_text(x) -> str:
    if x is None:
        return ""
    if isinstance(x, str):
        return x
    return getattr(x, "content", str(x))


if st.session_state.result_state:
    state = st.session_state.result_state

    st.markdown('<div class="section-label" style="margin-top:2.6rem;">RESULTS</div>', unsafe_allow_html=True)

    tab_report, tab_feedback, tab_search, tab_scraped = st.tabs(
        ["📝 Final Report", "🧐 Critic Feedback", "🔎 Search Results", "📖 Scraped Content"]
    )

    with tab_report:
        st.markdown('<div class="rcard"><span class="agent-badge badge-writer">WRITER CHAIN</span>', unsafe_allow_html=True)
        st.markdown(as_text(state.get("report", "")))
        st.markdown("</div>", unsafe_allow_html=True)
        st.download_button(
            "⬇️ Download Report (.md)",
            data=as_text(state.get("report", "")),
            file_name=f"research_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown",
        )

    with tab_feedback:
        st.markdown('<div class="rcard"><span class="agent-badge badge-critic">CRITIC CHAIN</span>', unsafe_allow_html=True)
        st.markdown(as_text(state.get("feedback", "")))
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_search:
        st.markdown('<div class="rcard"><span class="agent-badge badge-search">SEARCH AGENT</span>', unsafe_allow_html=True)
        st.markdown(as_text(state.get("search_results", "")))
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_scraped:
        st.markdown('<div class="rcard"><span class="agent-badge badge-reader">READER AGENT</span>', unsafe_allow_html=True)
        st.markdown(as_text(state.get("scraped_content", "")))
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="footer-note">RESEARCHMIND · POWERED BY YOUR AGENTS.PY & PIPELINE.PY</div>', unsafe_allow_html=True)
