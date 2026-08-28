import streamlit as st
import time
from pipeline import run_research_pipeline

# Page Configuration
st.set_page_config(
    page_title="Multi-Agent Research Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Modern Styling
st.markdown("""
<style>
    /* Main Background & Fonts */
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    
    /* Header Styling */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #4A90E2, #50E3C2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #8892b0;
        margin-bottom: 2rem;
    }
    
    /* Custom Metric Cards */
    .agent-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }
    .agent-title {
        font-weight: 600;
        color: #58a6ff;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    
    /* Status Badges */
    .badge-pending { color: #8b949e; }
    .badge-running { color: #d29922; font-weight: bold; }
    .badge-complete { color: #3fb950; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Sidebar Setup
with st.sidebar:
    st.image("https://img.icons8.com/isometric-folders/100/brain.png", width=60)
    st.title("System Control")
    st.markdown("---")
    
    st.subheader("Agent Workflow")
    st.markdown("""
    1. **Search Agent:** Queries recent web data.
    2. **Reader Agent:** Scrapes top URLs for deep content.
    3. **Writer Chain:** Synthesizes and drafts report.
    4. **Critic Chain:** Reviews and provides feedback.
    """)
    
    st.markdown("---")
    st.caption("Powered by LangChain & Streamlit")

# Main Interface
st.markdown('<div class="main-header">Multi-Agent Research System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Automated web research, content scraping, drafting, and critique</div>', unsafe_allow_html=True)

# Input Section
topic = st.text_input(
    "Research Topic",
    placeholder="e.g., Quantum Computing Advancements in 2026, Autonomous AI Agents...",
    help="Enter any topic you want the agent team to investigate."
)

start_button = st.button("🚀 Launch Research Pipeline", type="primary", use_container_width=True)

# State Management for Pipeline Execution
if start_button and topic:
    st.markdown("---")
    
    # Visual Progress Bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Layout Grid for Real-time Status Updates
    status_container = st.container()
    
    with status_container:
        col1, col2, col3, col4 = st.columns(4)
        
        s1 = col1.empty()
        s2 = col2.empty()
        s3 = col3.empty()
        s4 = col4.empty()

        # Initial Status
        s1.markdown("<div class='agent-card'><div class='agent-title'>1. Search</div><span class='badge-pending'>⏳ Waiting...</span></div>", unsafe_allow_html=True)
        s2.markdown("<div class='agent-card'><div class='agent-title'>2. Reader</div><span class='badge-pending'>⏳ Waiting...</span></div>", unsafe_allow_html=True)
        s3.markdown("<div class='agent-card'><div class='agent-title'>3. Writer</div><span class='badge-pending'>⏳ Waiting...</span></div>", unsafe_allow_html=True)
        s4.markdown("<div class='agent-card'><div class='agent-title'>4. Critic</div><span class='badge-pending'>⏳ Waiting...</span></div>", unsafe_allow_html=True)

    state = {}

    try:
        # Step 1: Search Agent
        s1.markdown("<div class='agent-card'><div class='agent-title'>1. Search</div><span class='badge-running'>🔄 Searching...</span></div>", unsafe_allow_html=True)
        status_text.text("🔍 Search Agent is querying reliable sources...")
        progress_bar.progress(15)
        
        from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain
        
        search_agent = build_search_agent()
        search_result = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
        })
        state["search_results"] = search_result['messages'][-1].content
        s1.markdown("<div class='agent-card'><div class='agent-title'>1. Search</div><span class='badge-complete'>✅ Done</span></div>", unsafe_allow_html=True)

        # Step 2: Reader Agent
        s2.markdown("<div class='agent-card'><div class='agent-title'>2. Reader</div><span class='badge-running'>🔄 Scraping...</span></div>", unsafe_allow_html=True)
        status_text.text("📖 Reader Agent is scraping deep content from top URLs...")
        progress_bar.progress(40)
        
        reader_agent = build_reader_agent()
        reader_result = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{state['search_results'][:800]}"
            )]
        })
        state['scraped_content'] = reader_result['messages'][-1].content
        s2.markdown("<div class='agent-card'><div class='agent-title'>2. Reader</div><span class='badge-complete'>✅ Done</span></div>", unsafe_allow_html=True)

        # Step 3: Writer Chain
        s3.markdown("<div class='agent-card'><div class='agent-title'>3. Writer</div><span class='badge-running'>🔄 Drafting...</span></div>", unsafe_allow_html=True)
        status_text.text("✍️ Writer Chain is assembling and drafting the comprehensive report...")
        progress_bar.progress(70)
        
        research_combined = (
            f"SEARCH RESULTS : \n {state['search_results']} \n\n"
            f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
        )
        state["report"] = writer_chain.invoke({
            "topic": topic,
            "research": research_combined
        })
        s3.markdown("<div class='agent-card'><div class='agent-title'>3. Writer</div><span class='badge-complete'>✅ Done</span></div>", unsafe_allow_html=True)

        # Step 4: Critic Chain
        s4.markdown("<div class='agent-card'><div class='agent-title'>4. Critic</div><span class='badge-running'>🔄 Reviewing...</span></div>", unsafe_allow_html=True)
        status_text.text("🧐 Critic Chain is evaluating and reviewing the report...")
        progress_bar.progress(90)
        
        state["feedback"] = critic_chain.invoke({
            "topic": topic,
            "report": state['report']
        })
        s4.markdown("<div class='agent-card'><div class='agent-title'>4. Critic</div><span class='badge-complete'>✅ Done</span></div>", unsafe_allow_html=True)

        # Execution Complete
        progress_bar.progress(100)
        status_text.success("🎉 Research Pipeline execution complete!")

        # Display Output Tabs
        st.markdown("### Research Artifacts")
        tab1, tab2, tab3, tab4 = st.tabs([
            "📄 Final Draft Report", 
            "🔍 Critic Feedback", 
            "🌐 Search Results", 
            "📑 Scraped Raw Content"
        ])

        with tab1:
            st.markdown(state["report"])
            st.download_button(
                label="📥 Download Draft Report",
                data=str(state["report"]),
                file_name=f"{topic.replace(' ', '_')}_report.md",
                mime="text/markdown"
            )

        with tab2:
            st.info("Constructive criticism and validation notes from the Critic Agent:")
            st.markdown(state["feedback"])

        with tab3:
            st.text_area("Search Raw Data", state["search_results"], height=300)

        with tab4:
            st.text_area("Scraped Web Data", state["scraped_content"], height=300)

    except Exception as e:
        st.error(f"An error occurred during execution: {str(e)}")

elif start_button and not topic:
    st.warning("Please enter a research topic before launching the pipeline.")
