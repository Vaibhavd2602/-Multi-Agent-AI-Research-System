"""
streamlit_app_v2.py
--------------------
Alternative UI for the multi-agent research pipeline (pipeline.py).
Dark "dashboard" theme with a step-by-step timeline instead of a hero-card
layout. pipeline.py / agents.py are untouched.

Run:
    streamlit run streamlit_app_v2.py
"""

import io
import contextlib
import datetime as dt

import streamlit as st

from pipeline import run_research_pipeline


st.set_page_config(
    page_title="Research Agent Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------
# Dark dashboard theme
# ----------------------------------------------------------------------
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

        html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }
        #MainMenu {visibility: hidden;} footer {visibility: hidden;}

        .stApp {
            background: #0b0e14;
            color: #e6e9ef;
        }
        .block-container { padding-top: 1.6rem; max-width: 1200px; }

        section[data-testid="stSidebar"] {
            background: #0f131b;
            border-right: 1px solid #1e2430;
        }
        section[data-testid="stSidebar"] * { color: #cdd3e0 !important; }

        /* Top bar */
        .topbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 1.2rem;
            border-bottom: 1px solid #1e2430;
            margin-bottom: 1.5rem;
        }
        .topbar h1 {
            font-size: 1.4rem;
            font-weight: 700;
            margin: 0;
            color: #f4f6fb;
        }
        .topbar .tag {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            color: #22d3ee;
            background: rgba(34,211,238,0.1);
            border: 1px solid rgba(34,211,238,0.3);
            padding: 0.25rem 0.7rem;
            border-radius: 6px;
        }

        /* Timeline */
        .timeline { display: flex; gap: 0; margin-bottom: 1.5rem; }
        .tl-step {
            flex: 1;
            background: #12161f;
            border: 1px solid #1e2430;
            padding: 0.9rem 1rem;
            position: relative;
        }
        .tl-step:first-child { border-radius: 10px 0 0 10px; }
        .tl-step:last-child { border-radius: 0 10px 10px 0; }
        .tl-step .num {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.7rem;
            color: #6b7280;
        }
        .tl-step .name { font-weight: 600; font-size: 0.92rem; color: #e6e9ef; }
        .tl-step.active { background: #16202b; border-color: #22d3ee; }
        .tl-step.active .num { color: #22d3ee; }
        .tl-step.done .num::before { content: "✓ "; color: #34d399; }

        /* Panel */
        .panel {
            background: #12161f;
            border: 1px solid #1e2430;
            border-radius: 12px;
            padding: 1.4rem 1.6rem;
            margin-bottom: 1.1rem;
        }
        .panel h4 {
            font-size: 0.95rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: #9aa4b8;
            margin-top: 0;
            margin-bottom: 0.8rem;
        }

        .metric {
            background: #12161f;
            border: 1px solid #1e2430;
            border-radius: 10px;
            padding: 1rem;
            text-align: center;
        }
        .metric .v { font-size: 1.4rem; font-weight: 700; color: #22d3ee; }
        .metric .l { font-size: 0.75rem; color: #8892a6; text-transform: uppercase; }

        .stButton>button {
            background: #22d3ee;
            color: #0b0e14;
            font-weight: 700;
            border: none;
            border-radius: 8px;
            padding: 0.55rem 1.2rem;
            width: 100%;
        }
        .stButton>button:hover { background: #67e8f9; }

        .console {
            background: #05070b;
            border: 1px solid #1e2430;
            border-radius: 10px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.78rem;
            color: #34d399;
            padding: 1rem;
            height: 240px;
            overflow-y: auto;
            white-space: pre-wrap;
        }

        [data-testid="stTabs"] button { color: #9aa4b8; }
    </style>
    """,
    unsafe_allow_html=True,
)

STAGES = ["Search", "Read", "Write", "Critique"]

if "result" not in st.session_state:
    st.session_state.result = None
if "history" not in st.session_state:
    st.session_state.history = []
if "running" not in st.session_state:
    st.session_state.running = False

# ----------------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚡ Agent Dashboard")
    st.caption("LangChain multi-agent research pipeline")
    st.divider()

    topic = st.text_input("Topic", placeholder="Type a research topic...")
    run_clicked = st.button("Run Pipeline", disabled=st.session_state.running)

    st.divider()
    st.markdown("**Agents in this pipeline**")
    st.markdown(
        "- `search_agent` — web search\n"
        "- `reader_agent` — scrapes top source\n"
        "- `writer_chain` — drafts report\n"
        "- `critic_chain` — reviews report"
    )

    if st.session_state.history:
        st.divider()
        st.markdown("**History**")
        for h in reversed(st.session_state.history[-6:]):
            st.caption(f"`{h['timestamp']}` {h['topic'][:32]}")

# ----------------------------------------------------------------------
# Top bar
# ----------------------------------------------------------------------
st.markdown(
    """
    <div class="topbar">
        <h1>Multi-Agent Research Pipeline</h1>
        <span class="tag">● 4 agents online</span>
    </div>
    """,
    unsafe_allow_html=True,
)


def render_timeline(active_idx=-1, done_upto=-1):
    html = '<div class="timeline">'
    for i, s in enumerate(STAGES):
        cls = "tl-step"
        if i <= done_upto:
            cls += " done"
        elif i == active_idx:
            cls += " active"
        html += f'<div class="{cls}"><div class="num">STEP {i+1:02d}</div><div class="name">{s}</div></div>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


class _ConsoleStream(io.TextIOBase):
    def __init__(self, placeholder):
        self.placeholder = placeholder
        self.buf = ""

    def write(self, s):
        if s:
            self.buf += s
            self.placeholder.markdown(f'<div class="console">{self.buf[-6000:]}</div>', unsafe_allow_html=True)
        return len(s)

    def flush(self):
        pass


# ----------------------------------------------------------------------
# Run
# ----------------------------------------------------------------------
if run_clicked:
    if not topic or not topic.strip():
        st.warning("Enter a topic first.")
    else:
        st.session_state.running = True
        render_timeline(active_idx=0)
        st.markdown('<div class="panel"><h4>Live Console</h4>', unsafe_allow_html=True)
        console_ph = st.empty()
        st.markdown("</div>", unsafe_allow_html=True)

        try:
            with contextlib.redirect_stdout(_ConsoleStream(console_ph)):
                result = run_research_pipeline(topic.strip())

            st.session_state.result = result
            st.session_state.history.append(
                {"topic": topic.strip(), "timestamp": dt.datetime.now().strftime("%H:%M:%S")}
            )
            st.success("Pipeline finished — all 4 agents completed.")
        except Exception as e:
            st.error(f"Pipeline error: {e}")
        finally:
            st.session_state.running = False

# ----------------------------------------------------------------------
# Results
# ----------------------------------------------------------------------
if st.session_state.result:
    state = st.session_state.result
    render_timeline(done_upto=3)

    c1, c2, c3, c4 = st.columns(4)
    for col, label, val in zip(
        (c1, c2, c3, c4),
        ("Search", "Reader", "Writer", "Critic"),
        ("OK", "OK", "OK", "OK"),
    ):
        with col:
            st.markdown(f'<div class="metric"><div class="v">{val}</div><div class="l">{label}</div></div>', unsafe_allow_html=True)

    st.write("")
    tab1, tab2, tab3, tab4 = st.tabs(["Report", "Critic Feedback", "Search Results", "Scraped Content"])

    def _text(v):
        return str(getattr(v, "content", v))

    with tab1:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown(_text(state.get("report", "")))
        st.markdown("</div>", unsafe_allow_html=True)
        st.download_button("Download report.md", _text(state.get("report", "")), file_name="report.md")

    with tab2:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown(_text(state.get("feedback", "")))
        st.markdown("</div>", unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.text(state.get("search_results", ""))
        st.markdown("</div>", unsafe_allow_html=True)

    with tab4:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.text(state.get("scraped_content", ""))
        st.markdown("</div>", unsafe_allow_html=True)
else:
    render_timeline()
    st.markdown(
        '<div class="panel" style="text-align:center; padding:2.5rem;">'
        '<h4 style="color:#e6e9ef;">Waiting for input</h4>'
        '<p style="color:#8892a6;">Enter a topic in the sidebar and click <b>Run Pipeline</b>.</p>'
        "</div>",
        unsafe_allow_html=True,
    )
