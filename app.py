"""
Multi-Agent Research System — Streamlit UI (purple/gradient, live step feed)
------------------------------------------------------------------------------
Drop this file in the same folder as pipeline.py, agents.py, tools.py, and .env,
then run:  streamlit run app.py

Note: this file talks to the underlying agents (build_search_agent,
build_reader_agent, writer_chain, critic_chain) directly, the same building
blocks pipeline.py uses, so it can show genuine live progress per step
without modifying pipeline.py itself. Running `python pipeline.py` from the
terminal still works exactly as before.
"""

import re
import time
import streamlit as st
from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

# ----------------------------------------------------------------------------
# Page config
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------------
# Session state defaults
# ----------------------------------------------------------------------------
if "result" not in st.session_state:
    st.session_state.result = None
if "recent_topics" not in st.session_state:
    st.session_state.recent_topics = []

MAX_RETRIES = 4
DEFAULT_WAIT = 20

# ----------------------------------------------------------------------------
# Global CSS
# ----------------------------------------------------------------------------
st.markdown(
    """
    <style>
        html, body, [class*="css"] { font-family: 'Inter', 'Segoe UI', sans-serif; }
        #MainMenu, footer, header {visibility: hidden;}
        .stApp { background: #0b0e14; }
        .block-container { padding-top: 2rem; max-width: 1150px; }

        section[data-testid="stSidebar"] {
            background: #0d1117;
            border-right: 1px solid #1f2430;
        }
        section[data-testid="stSidebar"] .block-container { padding-top: 2rem; }

        .sidebar-title {
            color: #f3f4f6;
            font-size: 1.25rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }
        .sidebar-caption {
            color: #8b8fa3;
            font-size: 0.88rem;
            line-height: 1.5;
            margin-bottom: 1.2rem;
        }
        .sidebar-divider {
            border-top: 1px solid #1f2430;
            margin: 1.2rem 0;
        }
        .sidebar-heading {
            color: #f3f4f6;
            font-weight: 700;
            font-size: 1.02rem;
            margin-bottom: 0.8rem;
        }
        .stage-item {
            margin-bottom: 0.9rem;
            color: #c3c6d4;
            font-size: 0.92rem;
            line-height: 1.5;
        }
        .stage-item b { color: #f3f4f6; }
        .recent-topic {
            color: #c3c6d4;
            font-size: 0.88rem;
            padding: 0.4rem 0;
            border-bottom: 1px solid #1a1f2b;
        }
        .no-topics { color: #6b7280; font-size: 0.88rem; }

        /* Hero */
        .hero-box {
            background: linear-gradient(120deg, #6d5df0 0%, #9b4de0 55%, #e0479f 100%);
            border-radius: 18px;
            padding: 2.2rem 2.4rem;
            margin-bottom: 1.6rem;
            box-shadow: 0 12px 32px rgba(109, 93, 240, 0.25);
        }
        .hero-box h1 {
            color: white;
            font-size: 2.3rem;
            font-weight: 800;
            margin: 0 0 0.6rem 0;
        }
        .hero-box p {
            color: rgba(255,255,255,0.92);
            font-size: 1.05rem;
            margin: 0;
        }

        /* Input */
        div[data-testid="stTextInput"] input {
            background: #141824 !important;
            border: 1px solid #262c3a !important;
            border-radius: 10px !important;
            color: #f3f4f6 !important;
            padding: 0.85rem 1rem !important;
        }
        div[data-testid="stTextInput"] input:focus {
            border: 1px solid #9b4de0 !important;
            box-shadow: 0 0 0 1px #9b4de033 !important;
        }

        div[data-testid="stFormSubmitButton"] button {
            background: linear-gradient(90deg, #6d5df0, #9b4de0);
            color: white;
            font-weight: 700;
            border: none;
            border-radius: 10px;
            padding: 0.85rem 1.4rem;
            width: 100%;
        }
        div[data-testid="stFormSubmitButton"] button:hover { opacity: 0.92; }

        /* Live feed */
        .feed-box {
            background: #10131c;
            border: 1px solid #1f2430;
            border-radius: 14px;
            padding: 1.4rem 1.6rem;
            margin-top: 1.2rem;
        }
        .feed-line {
            color: #d1d5db;
            font-size: 0.98rem;
            padding: 0.35rem 0;
        }
        .feed-line.done { color: #4ade80; }
        .feed-line b { color: #f3f4f6; }
        .feed-line.retry { color: #eab308; }

        .result-card {
            background: #10131c;
            border: 1px solid #1f2430;
            border-radius: 14px;
            padding: 1.6rem 1.8rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="sidebar-title">🧠 Research System</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sidebar-caption">Multi-agent pipeline: Search → Read → Write → Critique</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-heading">🔧 Pipeline Stages</div>', unsafe_allow_html=True)
    stages_html = """
    <div class="stage-item">1. <b>Search Agent</b> — finds recent, reliable sources</div>
    <div class="stage-item">2. <b>Reader Agent</b> — scrapes the best source in depth</div>
    <div class="stage-item">3. <b>Writer Chain</b> — drafts the final report</div>
    <div class="stage-item">4. <b>Critic Chain</b> — reviews & gives feedback</div>
    """
    st.markdown(stages_html, unsafe_allow_html=True)
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-heading">🕐 Recent Topics</div>', unsafe_allow_html=True)
    if not st.session_state.recent_topics:
        st.markdown('<div class="no-topics">No research run yet.</div>', unsafe_allow_html=True)
    else:
        for t in st.session_state.recent_topics[:6]:
            st.markdown(f'<div class="recent-topic">{t}</div>', unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# Hero
# ----------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero-box">
        <h1>🧠 Multi-Agent Research System</h1>
        <p>Enter a topic and let the Search, Reader, Writer &amp; Critic agents collaborate to produce a reviewed report.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Input form (single click triggers the run — no double-tap needed)
# ----------------------------------------------------------------------------
with st.form("research_form"):
    c1, c2 = st.columns([4, 1])
    with c1:
        topic = st.text_input(
            "Topic",
            placeholder="impact of quantum computing on cryptography",
            label_visibility="collapsed",
        )
    with c2:
        run_clicked = st.form_submit_button("🚀 Start Research", use_container_width=True)

# ----------------------------------------------------------------------------
# Helper: call any chain/agent with automatic retry on rate limits
# ----------------------------------------------------------------------------
def call_with_retry(fn, feed, retry_label):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return fn()
        except Exception as e:
            msg = str(e)
            if not ("rate_limit" in msg.lower() or "429" in msg) or attempt == MAX_RETRIES:
                raise
            match = re.search(r"try again in ([\d.]+)s", msg)
            wait_s = float(match.group(1)) + 1 if match else DEFAULT_WAIT
            feed.append(
                f'<div class="feed-line retry">⏳ Rate limit hit on {retry_label} — '
                f'retrying in {wait_s:.0f}s (attempt {attempt}/{MAX_RETRIES})...</div>'
            )
            render_feed(feed)
            time.sleep(wait_s)
    raise RuntimeError("Max retries exceeded")


def render_feed(lines):
    feed_placeholder.markdown(
        '<div class="feed-box">' + "".join(lines) + "</div>", unsafe_allow_html=True
    )


# ----------------------------------------------------------------------------
# Run pipeline live, step by step
# ----------------------------------------------------------------------------
feed_placeholder = st.empty()

if run_clicked:
    final_topic = topic.strip()
    if not final_topic:
        st.warning("Please enter a topic before starting research.")
    else:
        state = {}
        feed = ['<div class="feed-line">⏳ Running multi-agent pipeline...</div>']
        render_feed(feed)

        try:
            # --- Step 1: Search ---
            feed.append('<div class="feed-line">🔍 <b>Search Agent</b> is looking for recent, reliable sources...</div>')
            render_feed(feed)
            search_agent = build_search_agent()
            search_result = call_with_retry(
                lambda: search_agent.invoke(
                    {"messages": [("user", f"Find recent, reliable and detailed information about: {final_topic}")]}
                ),
                feed, "Search Agent",
            )
            state["search_results"] = search_result["messages"][-1].content
            feed.append('<div class="feed-line done">✅ Search complete.</div>')
            render_feed(feed)

            # --- Step 2: Read / scrape ---
            feed.append('<div class="feed-line">📖 <b>Reader Agent</b> is scraping the top resource for deeper content...</div>')
            render_feed(feed)
            reader_agent = build_reader_agent()
            reader_result = call_with_retry(
                lambda: reader_agent.invoke({
                    "messages": [("user",
                        f"Based on the following search results about '{final_topic}', "
                        f"pick the most relevant URL and scrape it for deeper content.\n\n"
                        f"Search Results:\n{state['search_results'][:800]}"
                    )]
                }),
                feed, "Reader Agent",
            )
            state["scraped_content"] = reader_result["messages"][-1].content
            feed.append('<div class="feed-line done">✅ Scraping complete.</div>')
            render_feed(feed)

            # --- Step 3: Write ---
            feed.append('<div class="feed-line">✍️ <b>Writer Chain</b> is drafting the report...</div>')
            render_feed(feed)
            research_combined = (
                f"SEARCH RESULTS : \n {state['search_results']} \n\n"
                f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
            )
            state["report"] = call_with_retry(
                lambda: writer_chain.invoke({"topic": final_topic, "research": research_combined}),
                feed, "Writer Chain",
            )
            feed.append('<div class="feed-line done">✅ Draft complete.</div>')
            render_feed(feed)

            # --- Step 4: Critique ---
            feed.append('<div class="feed-line">🧐 <b>Critic Chain</b> is reviewing the report...</div>')
            render_feed(feed)
            state["feedback"] = call_with_retry(
                lambda: critic_chain.invoke({"topic": final_topic, "report": state["report"]}),
                feed, "Critic Chain",
            )
            feed.append('<div class="feed-line done">✅ Review complete. Report ready!</div>')
            render_feed(feed)

            st.session_state.result = state
            if final_topic not in st.session_state.recent_topics:
                st.session_state.recent_topics.insert(0, final_topic)

        except Exception as e:
            feed.append(f'<div class="feed-line retry">⚠️ Pipeline failed: {e}</div>')
            render_feed(feed)

# ----------------------------------------------------------------------------
# Results
# ----------------------------------------------------------------------------
if st.session_state.result:
    result = st.session_state.result
    st.markdown("## 📄 Results")

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
