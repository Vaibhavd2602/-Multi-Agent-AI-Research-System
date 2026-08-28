import streamlit as st
from pipeline import run_research_pipeline

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="ResearchMind AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background: #0b1020;
    }

    /* Hide default Streamlit elements */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    /* Main container */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    /* Hero section */
    .hero {
        padding: 35px 40px;
        border-radius: 24px;
        background: linear-gradient(
            135deg,
            #111936 0%,
            #18234a 50%,
            #10182f 100%
        );
        border: 1px solid #28345e;
        margin-bottom: 30px;
        box-shadow: 0 15px 50px rgba(0,0,0,0.25);
    }

    .hero-title {
        font-size: 48px;
        font-weight: 800;
        margin-bottom: 8px;
        background: linear-gradient(
            90deg,
            #8b5cf6,
            #06b6d4,
            #38bdf8
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        font-size: 18px;
        color: #aab4d0;
        line-height: 1.6;
    }

    /* Agent cards */
    .agent-card {
        background: #11182d;
        border: 1px solid #273252;
        border-radius: 18px;
        padding: 22px;
        min-height: 150px;
        transition: 0.3s;
    }

    .agent-card:hover {
        border-color: #6366f1;
        transform: translateY(-3px);
    }

    .agent-icon {
        font-size: 30px;
        margin-bottom: 10px;
    }

    .agent-title {
        font-size: 19px;
        font-weight: 700;
        color: #ffffff;
    }

    .agent-description {
        color: #8f9bb8;
        font-size: 14px;
        margin-top: 7px;
        line-height: 1.5;
    }

    /* Section heading */
    .section-title {
        font-size: 25px;
        font-weight: 700;
        color: #ffffff;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    /* Result cards */
    .result-card {
        background: #10172b;
        border: 1px solid #263354;
        border-radius: 18px;
        padding: 25px;
        margin-bottom: 18px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #080d1b;
        border-right: 1px solid #202a47;
    }

    /* Button */
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 50px;
        font-size: 16px;
        font-weight: 700;
        border: none;
        background: linear-gradient(
            90deg,
            #6366f1,
            #8b5cf6
        );
        color: white;
    }

    .stButton > button:hover {
        background: linear-gradient(
            90deg,
            #7c3aed,
            #6366f1
        );
        border: none;
    }

    /* Text area */
    textarea {
        border-radius: 12px !important;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background: #11182d;
        border: 1px solid #273252;
        padding: 15px;
        border-radius: 15px;
    }

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown("""
    <div style="text-align:center; padding:10px;">
        <div style="font-size:50px;">🧠</div>
        <h2 style="margin:0;">ResearchMind AI</h2>
        <p style="color:#8994b2;">
            Multi-Agent Research System
        </p>
    </div>
    """, unsafe_allow_html=True)

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
    Reviews the report and provides feedback.
    """)

    st.divider()

    st.markdown("### 🛠️ Tech Stack")

    st.markdown("""
    - 🐍 Python
    - ⚡ Streamlit
    - 🔗 LangChain
    - 🤖 Multi-Agent AI
    - 🌐 Web Search
    - 📚 Web Scraping
    """)

    st.divider()

    st.caption("Built with ❤️ using Multi-Agent AI")


# --------------------------------------------------
# HERO
# --------------------------------------------------

st.markdown("""
<div class="hero">

    <div class="hero-title">
        🧠 ResearchMind AI
    </div>

    <div class="hero-subtitle">
        An intelligent multi-agent research system that searches the web,
        reads relevant resources, writes a detailed report, and critically
        evaluates the final result — automatically.
    </div>

</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# AGENT PIPELINE
# --------------------------------------------------

st.markdown(
    '<div class="section-title">🤖 AI Research Pipeline</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

agents = [
    (
        col1,
        "🔎",
        "Search Agent",
        "Searches for recent, reliable and relevant information."
    ),
    (
        col2,
        "📖",
        "Reader Agent",
        "Selects and analyzes the most relevant sources."
    ),
    (
        col3,
        "✍️",
        "Writer Agent",
        "Creates a structured and detailed research report."
    ),
    (
        col4,
        "🧐",
        "Critic Agent",
        "Reviews the report and identifies improvements."
    )
]

for col, icon, title, description in agents:

    with col:

        st.markdown(
            f"""
            <div class="agent-card">

                <div class="agent-icon">{icon}</div>

                <div class="agent-title">
                    {title}
                </div>

                <div class="agent-description">
                    {description}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# --------------------------------------------------
# TOPIC INPUT
# --------------------------------------------------

st.markdown(
    '<div class="section-title">🔬 Start Your Research</div>',
    unsafe_allow_html=True
)

topic = st.text_area(
    "Research Topic",
    placeholder=(
        "Example: Impact of Generative AI and Large Language "
        "Models on the Future of Software Development"
    ),
    height=100,
    label_visibility="collapsed"
)

st.write("")


# --------------------------------------------------
# RESEARCH BUTTON
# --------------------------------------------------

if st.button("🚀 Start AI Research"):

    if not topic.strip():

        st.warning("⚠️ Please enter a research topic first.")

    else:

        # Store topic
        st.session_state["topic"] = topic

        # Progress UI
        progress = st.progress(0)

        status = st.status(
            "🚀 Initializing ResearchMind AI...",
            expanded=True
        )

        try:

            # ------------------------------------------
            # STEP 1
            # ------------------------------------------

            status.write("🔎 Search Agent is searching the web...")
            progress.progress(15)

            # ------------------------------------------
            # RUN COMPLETE PIPELINE
            # ------------------------------------------

            result = run_research_pipeline(topic)

            # ------------------------------------------
            # COMPLETE
            # ------------------------------------------

            progress.progress(100)

            status.update(
                label="✅ Research completed successfully!",
                state="complete",
                expanded=False
            )

            # Save results
            st.session_state["research_result"] = result

            st.success(
                "🎉 Your multi-agent research report is ready!"
            )

        except Exception as e:

            status.update(
                label="❌ Research pipeline failed",
                state="error"
            )

            st.error(f"Error: {str(e)}")


# --------------------------------------------------
# RESULTS
# --------------------------------------------------

if "research_result" in st.session_state:

    result = st.session_state["research_result"]

    st.markdown("---")

    st.markdown(
        '<div class="section-title">📊 Research Results</div>',
        unsafe_allow_html=True
    )

    # Metrics
    search_data = result.get("search_results", "")
    scraped_data = result.get("scraped_content", "")
    report = result.get("report", "")
    feedback = result.get("feedback", "")

    # Handle LangChain AIMessage objects
    if hasattr(report, "content"):
        report = report.content

    if hasattr(feedback, "content"):
        feedback = feedback.content

    if hasattr(search_data, "content"):
        search_data = search_data.content

    if hasattr(scraped_data, "content"):
        scraped_data = scraped_data.content

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric("🤖 AI Agents", "4")

    with m2:
        st.metric("🔎 Search", "Completed")

    with m3:
        st.metric("📝 Report", "Generated")

    with m4:
        st.metric("🧐 Review", "Completed")


    # --------------------------------------------------
    # TABS
    # --------------------------------------------------

    tab1, tab2, tab3, tab4 = st.tabs([
        "📝 Final Report",
        "🧐 Critic Review",
        "🔎 Search Results",
        "📖 Scraped Content"
    ])


    # --------------------------------------------------
    # FINAL REPORT
    # --------------------------------------------------

    with tab1:

        st.markdown(
            '<div class="result-card">',
            unsafe_allow_html=True
        )

        st.markdown("### 📝 AI Generated Research Report")

        st.markdown(report)

        st.markdown("</div>", unsafe_allow_html=True)

        # Download report
        st.download_button(
            label="⬇️ Download Research Report",
            data=str(report),
            file_name="research_report.txt",
            mime="text/plain"
        )


    # --------------------------------------------------
    # CRITIC
    # --------------------------------------------------

    with tab2:

        st.markdown(
            '<div class="result-card">',
            unsafe_allow_html=True
        )

        st.markdown("### 🧐 Critic Agent Feedback")

        st.markdown(feedback)

        st.markdown("</div>", unsafe_allow_html=True)


    # --------------------------------------------------
    # SEARCH RESULTS
    # --------------------------------------------------

    with tab3:

        st.markdown(
            '<div class="result-card">',
            unsafe_allow_html=True
        )

        st.markdown("### 🔎 Search Agent Output")

        st.write(search_data)

        st.markdown("</div>", unsafe_allow_html=True)


    # --------------------------------------------------
    # SCRAPED CONTENT
    # --------------------------------------------------

    with tab4:

        st.markdown(
            '<div class="result-card">',
            unsafe_allow_html=True
        )

        st.markdown("### 📖 Reader Agent Output")

        st.write(scraped_data)

        st.markdown("</div>", unsafe_allow_html=True)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:#66708f; padding:20px;">
        <b>ResearchMind AI</b> · Multi-Agent Research System
        <br>
        <small>Search → Read → Write → Critique</small>
    </div>
    """,
    unsafe_allow_html=True
)
