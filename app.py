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
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif;
        }}

        .stApp {{
            background: radial-gradient(ellipse 900px 500px at 15% 0%, rgba(247,165,59,0.08), transparent),
                        {BG};
        }}

        #MainMenu, footer, header {{ visibility: hidden; }}

        .block-container {{
            padding-top: 2.4rem;
            max-width: 1180px;
        }}

        /* ── Hero ─────────────────────────────────────────── */
        .eyebrow {{
            color: {ACCENT};
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.82rem;
            letter-spacing: 4px;
            font-weight: 500;
            margin-bottom: 0.6rem;
        }}
        .hero-title {{
            font-size: 4.6rem;
            font-weight: 900;
            line-height: 1;
            letter-spacing: -2px;
            margin: 0;
        }}
        .hero-title .accent {{ color: {ACCENT}; }}
        .hero-sub {{
            color: #dbe1ea;
            font-size: 1.25rem;
            font-weight: 400;
            max-width: 780px;
            margin-top: 1.1rem;
            line-height: 1.5;
        }}
        .hero-divider {{
            border: none;
            border-top: 1px solid rgba(255,255,255,0.1);
            margin: 2.2rem 0 2.4rem 0;
        }}

        /* ── Section labels ───────────────────────────────── */
        .section-label {{
            color: {ACCENT};
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.78rem;
            letter-spacing: 2.5px;
            font-weight: 600;
            margin-bottom: 0.7rem;
        }}
        .pipeline-heading {{
            font-size: 1.6rem;
            font-weight: 800;
            color: white;
            margin-bottom: 1rem;
        }}

        /* ── Input ─────────────────────────────────────────── */
        div[data-testid="stTextInput"] input {{
            background: {CARD} !important;
            border: 1px solid {CARD_BORDER} !important;
            border-radius: 12px !important;
            color: white !important;
            padding: 0.95rem 1.1rem !important;
            font-size: 1rem !important;
        }}
        div[data-testid="stTextInput"] input:focus {{
            border-color: {ACCENT} !important;
            box-shadow: 0 0 0 1px {ACCENT} !important;
        }}
        div[data-testid="stTextInput"] input::placeholder {{
            color: #6b7280 !important;
        }}

        /* ── Run button ────────────────────────────────────── */
        div.stButton > button[kind="primary"], div.stButton > button {{
            width: 100%;
            border-radius: 12px;
            font-weight: 800;
            font-size: 1.02rem;
            padding: 0.9rem 1.4rem;
            border: none;
            background: linear-gradient(135deg, {ACCENT} 0%, {ACCENT_SOFT} 100%);
            color: #1a1206;
            box-shadow: 0 8px 24px rgba(247,165,59,0.28);
            transition: 0.15s ease;
        }}
        div.stButton > button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 10px 28px rgba(247,165,59,0.4);
        }}
        div.stButton > button:disabled {{
            opacity: 0.55;
            box-shadow: none;
        }}

        /* pill / try buttons */
        .pill-row div.stButton > button {{
            background: {CARD};
            color: #d1d5db;
            font-weight: 500;
            font-size: 0.85rem;
            padding: 0.4rem 0.9rem;
            border: 1px solid {CARD_BORDER};
            box-shadow: none;
            width: auto;
        }}
        .pill-row div.stButton > button:hover {{
            border-color: {ACCENT};
            color: {ACCENT};
        }}

        /* ── Pipeline cards ────────────────────────────────── */
        .pcard {{
            background: {CARD};
            border: 1px solid {CARD_BORDER};
            border-radius: 14px;
            padding: 1.1rem 1.3rem;
            margin-bottom: 0.9rem;
            transition: 0.2s ease;
        }}
        .pcard.active {{
            border-color: {ACCENT};
            box-shadow: 0 0 0 1px {ACCENT}, 0 8px 24px rgba(247,165,59,0.12);
        }}
        .pcard.done {{
            border-color: rgba(34,197,94,0.4);
        }}
        .pcard-top {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .pcard-num {{
            color: {ACCENT};
            font-family: 'JetBrains Mono', monospace;
            font-weight: 700;
            font-size: 0.85rem;
            margin-right: 0.5rem;
        }}
        .pcard-title {{
            font-weight: 700;
            font-size: 1.02rem;
            color: white;
        }}
        .pcard-desc {{
            color: {MUTED};
            font-size: 0.87rem;
            margin-top: 0.35rem;
        }}
        .status-badge {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.7rem;
            font-weight: 700;
            letter-spacing: 1px;
            padding: 0.25rem 0.6rem;
            border-radius: 999px;
        }}
        .status-waiting {{ background: rgba(255,255,255,0.06); color: {MUTED}; }}
        .status-running {{ background: rgba(247,165,59,0.16); color: {ACCENT}; }}
        .status-done {{ background: rgba(34,197,94,0.15); color: #4ade80; }}

        /* ── Result cards ──────────────────────────────────── */
        .rcard {{
            background: {CARD};
            border: 1px solid {CARD_BORDER};
            border-radius: 16px;
            padding: 1.5rem 1.7rem;
        }}
        .agent-badge {{
            display: inline-block;
            padding: 0.25rem 0.7rem;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 700;
            font-family: 'JetBrains Mono', monospace;
            margin-bottom: 0.9rem;
            letter-spacing: 0.5px;
        }}
        .badge-search {{ background: rgba(99,102,241,0.16); color: #a5b4fc; }}
        .badge-reader {{ background: rgba(236,72,153,0.16); color: #f9a8d4; }}
        .badge-writer {{ background: rgba(247,165,59,0.16); color: {ACCENT}; }}
        .badge-critic {{ background: rgba(34,197,94,0.16); color: #86efac; }}

        .stTabs [data-baseweb="tab-list"] {{ gap: 4px; }}
        .stTabs [data-baseweb="tab"] {{
            border-radius: 8px 8px 0 0;
            padding: 0.5rem 1.1rem;
            color: {MUTED};
        }}
        .stTabs [aria-selected="true"] {{ color: {ACCENT} !important; }}

        .footer-note {{
            text-align: center;
            color: rgba(255,255,255,0.25);
            font-size: 0.78rem;
            margin-top: 3rem;
            font-family: 'JetBrains Mono', monospace;
        }}
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