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

# Vibrant & Colorful Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main Background */
    .stApp {
        background: #0d0f18;
    }
    
    /* Dynamic Colorful Header Banner */
    .banner {
        background: linear-gradient(135deg, #FF007A 0%, #7B2CBF 50%, #00F5D4 100%);
        border-radius: 20px;
        padding: 2.5rem;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(255, 0, 122, 0.3);
        margin-bottom: 2rem;
    }
    .banner h1 {
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.4);
    }
    .banner p {
        font-size: 1.1rem;
        font-weight: 500;
        opacity: 0.95;
    }

    /* Distinct Vibrant Agent Cards */
    .agent-card-search {
        background: linear-gradient(135deg, rgba(0, 180, 216, 0.15) 0%, rgba(3, 4, 94, 0.3) 100%);
        border: 2px solid #00B4D8;
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 180, 216, 0.2);
    }
    
    .agent-card-reader {
        background: linear-gradient(135deg, rgba(157, 78, 221, 0.15) 0%, rgba(60, 9, 108, 0.3) 100%);
        border: 2px solid #9D4EDD;
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(157, 78, 221, 0.2);
    }

    .agent-card-writer {
        background: linear-gradient(135deg, rgba(255, 183, 3, 0.15) 0%, rgba(208, 0, 0, 0.3) 100%);
        border: 2px solid #FFB703;
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(255, 183, 3, 0.2);
    }

    .agent-card-critic {
        background: linear-gradient(135deg, rgba(0, 245, 212, 0.15) 0%, rgba(20, 110, 120, 0.3) 100%);
        border: 2px solid #00F5D4;
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 245, 212, 0.2);
    }

    .card-title {
        font-weight: 700;
        font-size: 1rem;
        text-transform: uppercase;
        margin-bottom: 0.3rem;
    }
    
    .status-text {
        font-weight: 600;
        font-size: 0.95rem;
    }

    /* Colorful Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
    }

    .stTabs [data-baseweb="tab"] {
        background: #181c2b;
        border-radius: 10px;
        color: #e0e0e0;
        padding: 10px 20px;
        font-weight: 600;
        border: 1px solid rgba(255,255,255,0.1);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #FF007A, #7B2CBF) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(255, 0, 122, 0.4);
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #121522;
        border-right: 1px solid rgba(255,255,255,0.05);
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🧠 **Research System**")
    st.caption("Multi-agent pipeline: Search ➔ Read ➔ Write ➔ Critique")
    st.markdown("---")
    
    st.markdown("### 🔧 **Pipeline Stages**")
    st.markdown("""
    <span style="color:#00B4D8; font-weight:bold;">1. Search Agent</span> — Finds recent, reliable sources<br><br>
    <span style="color:#9D4EDD; font-weight:bold;">2. Reader Agent</span> — Scrapes the best source in depth<br><br>
    <span style="color:#FFB703; font-weight:bold;">3. Writer Chain</span> — Drafts the final report<br><br>
    <span style="color:#00F5D4; font-weight:bold;">4. Critic Chain</span> — Reviews & gives feedback
    """, unsafe_allow_html=True)

# Header Banner
st.markdown("""
<div class="banner">
    <h1>🧠 Multi-Agent Research System</h1>
    <p>Enter a topic and let the Search, Reader, Writer & Critic agents collaborate to produce a reviewed report.</p>
</div>
""", unsafe_allow_html=True)

# Input Row
col_input, col_btn = st.columns([4, 1])
with col_input:
    topic = st.text_input("Enter Topic", placeholder="e.g., impact of quantum computing on cryptography", label_visibility="collapsed")
with col_btn:
    start_btn = st.button("🚀 Start Research", type="primary", use_container_width=True)

# Main Execution Flow
if start_btn:
    if not topic.strip():
        st.warning("⚠️ Enter a research topic first.")
    else:
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 4 Dynamic Agent Cards Layout
        col1, col2, col3, col4 = st.columns(4)
        c1 = col1.empty()
        c2 = col2.empty()
        c3 = col3.empty()
        c4 = col4.empty()

        # Initial Card State
        c1.markdown("<div class='agent-card-search'><div class='card-title' style='color:#00B4D8;'>1. Search</div><div class='status-text' style='color:#6c757d;'>⏳ Idle</div></div>", unsafe_allow_html=True)
        c2.markdown("<div class='agent-card-reader'><div class='card-title' style='color:#9D4EDD;'>2. Reader</div><div class='status-text' style='color:#6c757d;'>⏳ Idle</div></div>", unsafe_allow_html=True)
        c3.markdown("<div class='agent-card-writer'><div class='card-title' style='color:#FFB703;'>3. Writer</div><div class='status-text' style='color:#6c757d;'>⏳ Idle</div></div>", unsafe_allow_html=True)
        c4.markdown("<div class='agent-card-critic'><div class='card-title' style='color:#00F5D4;'>4. Critic</div><div class='status-text' style='color:#6c757d;'>⏳ Idle</div></div>", unsafe_allow_html=True)

        progress_bar = st.progress(0)
        status_box = st.empty()
        state = {}

        try:
            # 1. Search Agent
            c1.markdown("<div class='agent-card-search'><div class='card-title' style='color:#00B4D8;'>1. Search</div><div class='status-text' style='color:#00B4D8;'>🔎 Working...</div></div>", unsafe_allow_html=True)
            status_box.info("🔎 **Search Agent** is finding recent, reliable sources...")
            progress_bar.progress(25)

            search_agent = build_search_agent()
            search_result = search_agent.invoke({
                "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
            })
            state["search_results"] = search_result['messages'][-1].content
            c1.markdown("<div class='agent-card-search'><div class='card-title' style='color:#00B4D8;'>1. Search</div><div class='status-text' style='color:#00F5D4;'>✅ Complete</div></div>", unsafe_allow_html=True)

            # 2. Reader Agent
            c2.markdown("<div class='agent-card-reader'><div class='card-title' style='color:#9D4EDD;'>2. Reader</div><div class='status-text' style='color:#9D4EDD;'>📖 Scraping...</div></div>", unsafe_allow_html=True)
            status_box.info("📖 **Reader Agent** is scraping top content from web sources...")
            progress_bar.progress(50)

            reader_agent = build_reader_agent()
            reader_result = reader_agent.invoke({
                "messages": [("user",
                    f"Based on the following search results about '{topic}', "
                    f"pick the most relevant URL and scrape it for deeper content.\n\n"
                    f"Search Results:\n{state['search_results'][:800]}"
                )]
            })
            state['scraped_content'] = reader_result['messages'][-1].content
            c2.markdown("<div class='agent-card-reader'><div class='card-title' style='color:#9D4EDD;'>2. Reader</div><div class='status-text' style='color:#00F5D4;'>✅ Complete</div></div>", unsafe_allow_html=True)

            # 3. Writer Chain
            c3.markdown("<div class='agent-card-writer'><div class='card-title' style='color:#FFB703;'>3. Writer</div><div class='status-text' style='color:#FFB703;'>✍️ Drafting...</div></div>", unsafe_allow_html=True)
            status_box.info("✍️ **Writer Chain** is assembling information and drafting report...")
            progress_bar.progress(75)

            research_combined = (
                f"SEARCH RESULTS : \n {state['search_results']} \n\n"
                f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
            )
            state["report"] = writer_chain.invoke({
                "topic": topic,
                "research": research_combined
            })
            c3.markdown("<div class='agent-card-writer'><div class='card-title' style='color:#FFB703;'>3. Writer</div><div class='status-text' style='color:#00F5D4;'>✅ Complete</div></div>", unsafe_allow_html=True)

            # 4. Critic Chain
            c4.markdown("<div class='agent-card-critic'><div class='card-title' style='color:#00F5D4;'>4. Critic</div><div class='status-text' style='color:#00F5D4;'>🧐 Reviewing...</div></div>", unsafe_allow_html=True)
            status_box.info("🧐 **Critic Chain** is analyzing report for review & feedback...")
            progress_bar.progress(90)

            state["feedback"] = critic_chain.invoke({
                "topic": topic,
                "report": state['report']
            })
            c4.markdown("<div class='agent-card-critic'><div class='card-title' style='color:#00F5D4;'>4. Critic</div><div class='status-text' style='color:#00F5D4;'>✅ Complete</div></div>", unsafe_allow_html=True)

            progress_bar.progress(100)
            status_box.success("🎉 **All agents finished their workflow successfully!**")

            st.markdown("<br>", unsafe_allow_html=True)

            # Color Output Tabs
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
                    file_name=f"{topic.replace(' ', '_')}_report.md",
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
