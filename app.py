import streamlit as st
from pipeline import run_research_pipeline
from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

# Page Configuration
st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State for Recent Topics
if "recent_topics" not in st.session_state:
    st.session_state.recent_topics = []

if "search_topic" not in st.session_state:
    st.session_state.search_topic = ""

# Subdued, Elegant & Balanced Dark Theme CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Background */
    .stApp {
        background-color: #0e1117;
        color: #c9d1d9;
    }
    
    /* Soft Subdued Header Banner */
    .banner {
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        border: 1px solid #374151;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .banner h1 {
        color: #f3f4f6;
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.4rem;
    }
    .banner p {
        color: #9ca3af;
        font-size: 1rem;
        margin: 0;
    }

    /* Muted Status Cards */
    .agent-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }

    .card-title {
        font-weight: 600;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.3rem;
    }
    
    .status-text {
        font-weight: 500;
        font-size: 0.9rem;
    }

    /* Clean Styled Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #161b22;
        border-radius: 8px;
        color: #9ca3af;
        padding: 8px 16px;
        font-weight: 500;
        border: 1px solid #30363d;
    }

    .stTabs [aria-selected="true"] {
        background-color: #2563eb !important;
        color: #ffffff !important;
        border-color: #2563eb !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }
</style>
""", unsafe_allow_html=True)

# Function to handle search click from Recent Searches
def select_topic(topic_name):
    st.session_state.search_topic = topic_name

# Sidebar Setup
with st.sidebar:
    st.markdown("## 🧠 **Research System**")
    st.caption("Multi-agent pipeline: Search ➔ Read ➔ Write ➔ Critique")
    st.markdown("---")
    
    st.markdown("### 🔧 **Pipeline Stages**")
    st.markdown("""
    <span style="color:#60a5fa; font-weight:600;">1. Search Agent</span> — Finds recent, reliable sources<br><br>
    <span style="color:#c084fc; font-weight:600;">2. Reader Agent</span> — Scrapes the best source in depth<br><br>
    <span style="color:#facc15; font-weight:600;">3. Writer Chain</span> — Drafts the final report<br><br>
    <span style="color:#34d399; font-weight:600;">4. Critic Chain</span> — Reviews & gives feedback
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🕒 **Recent Searches**")
    
    if st.session_state.recent_topics:
        for past_topic in reversed(st.session_state.recent_topics[-5:]):  # Shows last 5
            st.button(f"🔍 {past_topic}", key=f"recent_{past_topic}", on_click=select_topic, args=(past_topic,), use_container_width=True)
    else:
        st.caption("No recent searches yet.")

# Main Header Banner
st.markdown("""
<div class="banner">
    <h1>🧠 Multi-Agent Research System</h1>
    <p>Enter a topic and let the Search, Reader, Writer & Critic agents collaborate to produce a reviewed report.</p>
</div>
""", unsafe_allow_html=True)

# Input Row
col_input, col_btn = st.columns([4, 1])
with col_input:
    topic_input = st.text_input(
        "Enter Topic", 
        value=st.session_state.search_topic,
        placeholder="e.g., impact of quantum computing on cryptography", 
        label_visibility="collapsed"
    )
with col_btn:
    start_btn = st.button("🚀 Start Research", type="primary", use_container_width=True)

# Main Execution Flow
if start_btn:
    if not topic_input.strip():
        st.warning("⚠️ Enter a research topic first.")
    else:
        # Save to Recent Searches list
        if topic_input not in st.session_state.recent_topics:
            st.session_state.recent_topics.append(topic_input)

        st.markdown("<br>", unsafe_allow_html=True)
        
        # 4 Dynamic Agent Status Cards Layout
        col1, col2, col3, col4 = st.columns(4)
        c1, c2, c3, c4 = col1.empty(), col2.empty(), col3.empty(), col4.empty()

        # Initial Card States (Muted Dark Colors)
        c1.markdown("<div class='agent-card'><div class='card-title' style='color:#60a5fa;'>1. Search</div><div class='status-text' style='color:#6b7280;'>⏳ Idle</div></div>", unsafe_allow_html=True)
        c2.markdown("<div class='agent-card'><div class='card-title' style='color:#c084fc;'>2. Reader</div><div class='status-text' style='color:#6b7280;'>⏳ Idle</div></div>", unsafe_allow_html=True)
        c3.markdown("<div class='agent-card'><div class='card-title' style='color:#facc15;'>3. Writer</div><div class='status-text' style='color:#6b7280;'>⏳ Idle</div></div>", unsafe_allow_html=True)
        c4.markdown("<div class='agent-card'><div class='card-title' style='color:#34d399;'>4. Critic</div><div class='status-text' style='color:#6b7280;'>⏳ Idle</div></div>", unsafe_allow_html=True)

        progress_bar = st.progress(0)
        status_box = st.empty()
        state = {}

        try:
            # 1. Search Agent
            c1.markdown("<div class='agent-card' style='border-color:#60a5fa;'><div class='card-title' style='color:#60a5fa;'>1. Search</div><div class='status-text' style='color:#60a5fa;'>🔎 Working...</div></div>", unsafe_allow_html=True)
            status_box.info("🔎 **Search Agent** is finding recent, reliable sources...")
            progress_bar.progress(25)

            search_agent = build_search_agent()
            search_result = search_agent.invoke({
                "messages": [("user", f"Find recent, reliable and detailed information about: {topic_input}")]
            })
            state["search_results"] = search_result['messages'][-1].content
            c1.markdown("<div class='agent-card' style='border-color:#34d399;'><div class='card-title' style='color:#60a5fa;'>1. Search</div><div class='status-text' style='color:#34d399;'>✅ Complete</div></div>", unsafe_allow_html=True)

            # 2. Reader Agent
            c2.markdown("<div class='agent-card' style='border-color:#c084fc;'><div class='card-title' style='color:#c084fc;'>2. Reader</div><div class='status-text' style='color:#c084fc;'>📖 Scraping...</div></div>", unsafe_allow_html=True)
            status_box.info("📖 **Reader Agent** is scraping top content from web sources...")
            progress_bar.progress(50)

            reader_agent = build_reader_agent()
            reader_result = reader_agent.invoke({
                "messages": [("user",
                    f"Based on the following search results about '{topic_input}', "
                    f"pick the most relevant URL and scrape it for deeper content.\n\n"
                    f"Search Results:\n{state['search_results'][:800]}"
                )]
            })
            state['scraped_content'] = reader_result['messages'][-1].content
            c2.markdown("<div class='agent-card' style='border-color:#34d399;'><div class='card-title' style='color:#c084fc;'>2. Reader</div><div class='status-text' style='color:#34d399;'>✅ Complete</div></div>", unsafe_allow_html=True)

            # 3. Writer Chain
            c3.markdown("<div class='agent-card' style='border-color:#facc15;'><div class='card-title' style='color:#facc15;'>3. Writer</div><div class='status-text' style='color:#facc15;'>✍️ Drafting...</div></div>", unsafe_allow_html=True)
            status_box.info("✍️ **Writer Chain** is assembling information and drafting report...")
            progress_bar.progress(75)

            research_combined = (
                f"SEARCH RESULTS : \n {state['search_results']} \n\n"
                f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
            )
            state["report"] = writer_chain.invoke({
                "topic": topic_input,
                "research": research_combined
            })
            c3.markdown("<div class='agent-card' style='border-color:#34d399;'><div class='card-title' style='color:#facc15;'>3. Writer</div><div class='status-text' style='color:#34d399;'>✅ Complete</div></div>", unsafe_allow_html=True)

            # 4. Critic Chain
            c4.markdown("<div class='agent-card' style='border-color:#34d399;'><div class='card-title' style='color:#34d399;'>4. Critic</div><div class='status-text' style='color:#34d399;'>🧐 Reviewing...</div></div>", unsafe_allow_html=True)
            status_box.info("🧐 **Critic Chain** is analyzing report for review & feedback...")
            progress_bar.progress(90)

            state["feedback"] = critic_chain.invoke({
                "topic": topic_input,
                "report": state['report']
            })
            c4.markdown("<div class='agent-card' style='border-color:#34d399;'><div class='card-title' style='color:#34d399;'>4. Critic</div><div class='status-text' style='color:#34d399;'>✅ Complete</div></div>", unsafe_allow_html=True)

            progress_bar.progress(100)
            status_box.success("🎉 **Research pipeline execution finished!**")

            st.markdown("<br>", unsafe_allow_html=True)

            # Output Tabs
            t1, t2, t3, t4 = st.tabs([
                "📄 Draft Report", 
                "🧐 Critic Review", 
                "🔍 Search Results", 
                "📑 Scraped Content"
            ])

            with t1:
                st.markdown(state["report"])
                st.download_button(
                    label="📥 Download Report (.md)",
                    data=str(state["report"]),
                    file_name=f"{topic_input.replace(' ', '_')}_report.md",
                    mime="text/markdown"
                )

            with t2:
                st.markdown(state["feedback"])

            with t3:
                st.code(state["search_results"], language="text")

            with t4:
                st.code(state["scraped_content"], language="text")

        except Exception as err:
            st.error(f"Execution Error: {err}")
