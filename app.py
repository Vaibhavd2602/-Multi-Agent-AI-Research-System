import streamlit as st
from pipeline import run_research_pipeline


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="ResearchMind AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background-color: #0b1020;
    }

    /* Main content */
    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #080d1b;
        border-right: 1px solid #222b45;
    }

    /* Main title */
    .main-title {
        font-size: 48px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #9ca8c4;
        font-size: 18px;
        margin-bottom: 35px;
    }

    /* Agent boxes */
    .agent-box {
        background-color: #11182d;
        border: 1px solid #283453;
        border-radius: 16px;
        padding: 20px;
        min-height: 150px;
    }

    .agent-box:hover {
        border-color: #6366f1;
    }

    /* Section title */
    .section-heading {
        font-size: 25px;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    /* Button */
    .stButton > button {
        width: 100%;
        height: 52px;
        border-radius: 12px;
        font-size: 17px;
        font-weight: 700;
    }

    /* Text area */
    textarea {
        border-radius: 12px !important;
    }

    /* Metrics */
    [data-testid="stMetric"] {
        background-color: #11182d;
        border: 1px solid #283453;
        border-radius: 14px;
        padding: 15px;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("# 🧠 ResearchMind AI")

    st.caption("Multi-Agent Research System")

    st.divider()

    st.markdown("### ⚙️ System Architecture")

    st.markdown("""
    **🔎 Search Agent**

    Finds recent and reliable information.

    **📖 Reader Agent**

    Scrapes and analyzes relevant resources.

    **✍️ Writer Agent**

    Generates a structured research report.

    **🧐 Critic Agent**

    Reviews the final report.
    """)

    st.divider()

    st.markdown("### 🛠️ Tech Stack")

    st.markdown("""
    🐍 Python  
    ⚡ Streamlit  
    🔗 LangChain  
    🤖 Multi-Agent AI  
    🌐 Web Search  
    📚 Web Scraping
    """)

    st.divider()

    st.caption("Built with ❤️ using Multi-Agent AI")


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🧠 ResearchMind AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'An intelligent multi-agent system for automated research, '
    'analysis, report generation and critical review.'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# AGENT PIPELINE
# =========================================================

st.markdown(
    '<div class="section-heading">🤖 AI Research Pipeline</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)


with col1:
    with st.container(border=True):
        st.markdown("### 🔎 Search Agent")
        st.write(
            "Searches the web for recent, reliable and "
            "relevant information."
        )


with col2:
    with st.container(border=True):
        st.markdown("### 📖 Reader Agent")
        st.write(
            "Selects the best source and extracts "
            "deeper information."
        )


with col3:
    with st.container(border=True):
        st.markdown("### ✍️ Writer Agent")
        st.write(
            "Uses the collected research to create "
            "a detailed report."
        )


with col4:
    with st.container(border=True):
        st.markdown("### 🧐 Critic Agent")
        st.write(
            "Reviews the generated report and provides "
            "critical feedback."
        )


# =========================================================
# RESEARCH INPUT
# =========================================================

st.markdown(
    '<div class="section-heading">🔬 Start Your Research</div>',
    unsafe_allow_html=True
)

topic = st.text_area(
    "Enter your research topic",
    placeholder=(
        "Example: Impact of Generative AI and Large Language "
        "Models on the Future of Software Development"
    ),
    height=120
)


# =========================================================
# START RESEARCH
# =========================================================

if st.button("🚀 Start AI Research", type="primary"):

    if not topic.strip():

        st.warning("⚠️ Please enter a research topic.")

    else:

        st.session_state["topic"] = topic

        # Progress
        progress = st.progress(0)

        # Status
        status = st.status(
            "🚀 ResearchMind AI is working...",
            expanded=True
        )

        try:

            status.write("🔎 Search Agent is searching for information...")
            progress.progress(20)

            status.write("📖 Reader Agent is analyzing resources...")
            progress.progress(40)

            status.write("✍️ Writer Agent is preparing the report...")
            progress.progress(70)

            status.write("🧐 Critic Agent is reviewing the report...")
            progress.progress(90)

            # Run actual pipeline
            result = run_research_pipeline(topic)

            progress.progress(100)

            status.update(
                label="✅ Research completed successfully!",
                state="complete",
                expanded=False
            )

            st.session_state["research_result"] = result

            st.success("🎉 Your research report is ready!")

        except Exception as e:

            status.update(
                label="❌ Research failed",
                state="error",
                expanded=True
            )

            st.error(f"Error: {e}")


# =========================================================
# RESULTS
# =========================================================

if "research_result" in st.session_state:

    result = st.session_state["research_result"]

    st.divider()

    st.markdown(
        '<div class="section-heading">📊 Research Results</div>',
        unsafe_allow_html=True
    )

    # Get results
    search_data = result.get("search_results", "")
    scraped_data = result.get("scraped_content", "")
    report = result.get("report", "")
    feedback = result.get("feedback", "")

    # LangChain AIMessage handling
    if hasattr(search_data, "content"):
        search_data = search_data.content

    if hasattr(scraped_data, "content"):
        scraped_data = scraped_data.content

    if hasattr(report, "content"):
        report = report.content

    if hasattr(feedback, "content"):
        feedback = feedback.content


    # =====================================================
    # METRICS
    # =====================================================

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric("🤖 AI Agents", "4")

    with m2:
        st.metric("🔎 Search", "Completed")

    with m3:
        st.metric("📝 Report", "Generated")

    with m4:
        st.metric("🧐 Review", "Completed")


    st.write("")


    # =====================================================
    # RESULT TABS
    # =====================================================

    tab1, tab2, tab3, tab4 = st.tabs([
        "📝 Final Report",
        "🧐 Critic Review",
        "🔎 Search Results",
        "📖 Scraped Content"
    ])


    # =====================================================
    # REPORT
    # =====================================================

    with tab1:

        st.subheader("📝 AI Generated Research Report")

        st.markdown(report)

        st.download_button(
            "⬇️ Download Report",
            data=str(report),
            file_name="research_report.txt",
            mime="text/plain"
        )


    # =====================================================
    # CRITIC
    # =====================================================

    with tab2:

        st.subheader("🧐 Critic Agent Feedback")

        st.markdown(feedback)


    # =====================================================
    # SEARCH
    # =====================================================

    with tab3:

        st.subheader("🔎 Search Agent Output")

        st.write(search_data)


    # =====================================================
    # SCRAPED CONTENT
    # =====================================================

    with tab4:

        st.subheader("📖 Reader Agent Output")

        st.write(scraped_data)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "ResearchMind AI • Search → Read → Write → Critique"
)
