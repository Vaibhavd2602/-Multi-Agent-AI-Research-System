import streamlit as st
from pipeline import run_research_pipeline
from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

# 1. Page Config
st.set_page_config(
    page_title="ResearchAI | Autonomous Multi-Agent Suite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Premium Custom CSS (Dark Glassmorphism Theme)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Global App Styling */
    .stApp {
        background: #090d16;
    }
    
    /* Hero Banner */
    .hero-container {
        background: linear-gradient(135deg, rgba(255,255,255,0.03) 0%, rgba(255,255,255,0.01) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        backdrop-filter: blur(10px);
    }
    
    .hero-title {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(90deg, #60A5FA, #A78BFA, #F472B6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .hero-subtitle {
        color: #9CA3AF;
        font-size: 1.1rem;
        margin-bottom: 0;
    }

    /* Agent Status Cards */
    .status-card {
        background: rgba(17, 24, 39, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .status-card-active {
        border: 1px solid #60A5FA;
        box-shadow: 0 0 15px rgba(96, 165, 250, 0.2);
    }
    
    .status-card-done {
        border: 1px solid #34D399;
        box-shadow: 0 0 15px rgba(52, 211, 153, 0.15);
    }

    .status-title {
        font-size: 0.9rem;
        font-weight: 600;
        color: #9CA3AF;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .status-value {
        font-size: 1.1rem;
        font-weight: 700;
        margin-top: 0.4rem;
    }

    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: rgba(31, 41, 55, 0.5);
        border-radius: 8px;
        padding: 8px 16px;
        color: #9CA3AF;
    }

    .stTabs [aria-selected="true"] {
        background-color: #2563EB !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Sidebar Controls
with st.sidebar:
    st.markdown("## ⚡ **Control Panel**")
    st.markdown("---")
    
    st.markdown("### 🤖 **Active Agents**")
    st.markdown("""
    * 🔍 **Search Agent:** Web Scraping
    * 📖 **Reader Agent:** URL Extraction
    * ✍️ **Writer Chain:** Report Draft
    * 🧐 **Critic Chain:** Peer Review
    """)
    
    st.markdown("---")
    output_format = st.selectbox("Output Format", ["Markdown (.md)", "Text (.txt)"])
    st.caption("v2.4 • Multi-Agent Autonomous Framework")

# 4. Hero Section
st.markdown("""
<div class="hero-container">
    <div class="hero-title">Autonomous AI Research Lab</div>
    <div class="hero-subtitle">Multi-Agent System for Deep Information Gathering, Synthesis, and Peer Critique</div>
</div>
""", unsafe_allow_html=True)

# 5. User Input Form
with st.container():
    col_input, col_btn = st.columns([4, 1])
    with col_input:
        topic = st.text_input(
            "Topic Input",
            placeholder="Enter research target (e.g., Quantum Computing Trends, AI in Healthcare...)",
            label_visibility="collapsed"
        )
    with col_btn:
        start_button = st.button("🚀 Start Pipeline", use_container_width=True, type="primary")

st.markdown("<br>", unsafe_allow_html=True)

# 6. Pipeline Execution
if start_button:
    if not topic.strip():
        st.warning("⚠️ Please enter a valid topic before running.")
    else:
        # Dashboard Cards Grid
        c1, c2, c3, c4 = st.columns(4)
        
        card1 = c1.empty()
        card2 = c2.empty()
        card3 = c3.empty()
        card4 = c4.empty()

        # Initial Idle Cards Display
        card1.markdown("<div class='status-card'><div class='status-title'>1. Search</div><div class='status-value' style='color:#6B7280;'>Idle</div></div>", unsafe_allow_html=True)
        card2.markdown("<div class='status-card'><div class='status-title'>2. Reader</div><div class='status-value' style='color:#6B7280;'>Idle</div></div>", unsafe_allow_html=True)
        card3.markdown("<div class='status-card'><div class='status-title'>3. Writer</div><div class='status-value' style='color:#6B7280;'>Idle</div></div>", unsafe_allow_html=True)
        card4.markdown("<div class='status-card'><div class='status-title'>4. Critic</div><div class='status-value' style='color:#6B7280;'>Idle</div></div>", unsafe_allow_html=True)

        progress_bar = st.progress(0)
        status_msg = st.empty()
        state = {}

        try:
            # Step 1: Search Agent
            card1.markdown("<div class='status-card status-card-active'><div class='status-title'>1. Search</div><div class='status-value' style='color:#60A5FA;'>Running...</div></div>", unsafe_allow_html=True)
            status_msg.info("🔍 **Search Agent:** Gathering recent web data and top sources...")
            progress_bar.progress(20)

            search_agent = build_search_agent()
            search_result = search_agent.invoke({
                "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
            })
            state["search_results"] = search_result['messages'][-1].content
            card1.markdown("<div class='status-card status-card-done'><div class='status-title'>1. Search</div><div class='status-value' style='color:#34D399;'>Completed</div></div>", unsafe_allow_html=True)

            # Step 2: Reader Agent
            card2.markdown("<div class='status-card status-card-active'><div class='status-title'>2. Reader</div><div class='status-value' style='color:#60A5FA;'>Running...</div></div>", unsafe_allow_html=True)
            status_msg.info("📖 **Reader Agent:** Scraping deep details from selected URLs...")
            progress_bar.progress(45)

            reader_agent = build_reader_agent()
            reader_result = reader_agent.invoke({
                "messages": [("user",
                    f"Based on the following search results about '{topic}', "
                    f"pick the most relevant URL and scrape it for deeper content.\n\n"
                    f"Search Results:\n{state['search_results'][:800]}"
                )]
            })
            state['scraped_content'] = reader_result['messages'][-1].content
            card2.markdown("<div class='status-card status-card-done'><div class='status-title'>2. Reader</div><div class='status-value' style='color:#34D399;'>Completed</div></div>", unsafe_allow_html=True)

            # Step 3: Writer Chain
            card3.markdown("<div class='status-card status-card-active'><div class='status-title'>3. Writer</div><div class='status-value' style='color:#60A5FA;'>Running...</div></div>", unsafe_allow_html=True)
            status_msg.info("✍️ **Writer Chain:** Synthesizing content and building draft...")
            progress_bar.progress(70)

            research_combined = (
                f"SEARCH RESULTS : \n {state['search_results']} \n\n"
                f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
            )
            state["report"] = writer_chain.invoke({
                "topic": topic,
                "research": research_combined
            })
            card3.markdown("<div class='status-card status-card-done'><div class='status-title'>3. Writer</div><div class='status-value' style='color:#34D399;'>Completed</div></div>", unsafe_allow_html=True)

            # Step 4: Critic Chain
            card4.markdown("<div class='status-card status-card-active'><div class='status-title'>4. Critic</div><div class='status-value' style='color:#60A5FA;'>Running...</div></div>", unsafe_allow_html=True)
            status_msg.info("🧐 **Critic Chain:** Evaluating draft and generating feedback...")
            progress_bar.progress(90)

            state["feedback"] = critic_chain.invoke({
                "topic": topic,
                "report": state['report']
            })
            card4.markdown("<div class='status-card status-card-done'><div class='status-title'>4. Critic</div><div class='status-value' style='color:#34D399;'>Completed</div></div>", unsafe_allow_html=True)

            progress_bar.progress(100)
            status_msg.success("✨ **Pipeline Execution Finished Successfully!**")

            st.markdown("<br>", unsafe_allow_html=True)

            # 7. Output Presentation
            tab_report, tab_critic, tab_search, tab_scraped = st.tabs([
                "📄 Final Report", 
                "🧐 Peer Critique", 
                "🔍 Search Results", 
                "📑 Raw Scraped Data"
            ])

            with tab_report:
                st.markdown(state["report"])
                
                ext = ".md" if "Markdown" in output_format else ".txt"
                st.download_button(
                    label="📥 Download Generated Report",
                    data=str(state["report"]),
                    file_name=f"{topic.lower().replace(' ', '_')}_report{ext}",
                    mime="text/plain",
                    type="primary"
                )

            with tab_critic:
                st.markdown("### Agent Evaluation")
                st.markdown(state["feedback"])

            with tab_search:
                st.markdown("### Search Data")
                st.code(state["search_results"], language="markdown")

            with tab_scraped:
                st.markdown("### Extracted Page Content")
                st.code(state["scraped_content"], language="markdown")

        except Exception as e:
            st.error(f"Execution Error: {str(e)}")
