import streamlit as st
from pipeline import run_research_pipeline


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="MULTI AI RESEARCH SYSTEM",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

    /* =========================
       MAIN APP
       ========================= */

    .stApp {
        background-color: #0b1020;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* =========================
       SIDEBAR
       ========================= */

    section[data-testid="stSidebar"] {
        background-color: #080d1b;
        border-right: 1px solid #222b45;
    }

    section[data-testid="stSidebar"] h1 {
        font-size: 23px;
        text-align: center;
    }


    /* =========================
       MAIN TITLE
       ========================= */

    .main-title {
        font-size: 45px;
        font-weight: 800;
        text-align: center;
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


    .subtitle {
        text-align: center;
        color: #9ca8c4;
        font-size: 17px;
        line-height: 1.6;
        margin-bottom: 35px;
    }


    /* =========================
       SECTION HEADINGS
       ========================= */

    .section-heading {
        font-size: 25px;
        font-weight: 700;
        color: white;
        margin-top: 25px;
        margin-bottom: 18px;
    }


    /* =========================
       AGENT AREA
       ========================= */

    .agent-title {
        font-size: 19px;
        font-weight: 700;
        color: white;
    }

    .agent-description {
        color: #9ca8c4;
        font-size: 14px;
        line-height: 1.5;
    }


    /* =========================
       TEXT AREA
       ========================= */

    textarea {
        border-radius: 12px !important;
    }


    /* =========================
       BUTTON
       ========================= */

    .stButton > button {
        width: 100%;
        height: 52px;
        border-radius: 12px;
        font-size: 17px;
        font-weight: 700;
    }


    /* =========================
       METRICS
       ========================= */

    [data-testid="stMetric"] {
        background-color: #11182d;
        border: 1px solid #283453;
        border-radius: 14px;
        padding: 15px;
    }


    /* =========================
       TABS
       ========================= */

    button[data-baseweb="tab"] {
        font-size: 15px;
        font-weight: 600;
    }


    /* =========================
       DIVIDER
       ========================= */

    hr {
        border-color: #26314d;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("# 🧠 MULTI AI RESEARCH SYSTEM")

    st.caption("Intelligent Multi-Agent Research")

    st.divider()

    st.markdown("### 🔎 Research Agents")

    st.markdown("""
    **🔎 Search Agent**

    Finds recent and reliable information.

    **📖 Reader Agent**

    Scrapes and analyzes relevant resources.

    **✍️ Writer Agent**

    Generates a structured research report.

    **🧐 Critic Agent**

    Reviews the final report and provides feedback.
    """)


# =========================================================
# MAIN HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🧠 MULTI AI RESEARCH SYSTEM</div>',
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
# AI RESEARCH PIPELINE
# =========================================================

st.markdown(
    '<div class="section-heading">🤖 AI Research Pipeline</div>',
    unsafe_allow_html=True
)


col1, col2, col3, col4 = st.columns(4)


# ---------------------------------------------------------
# SEARCH AGENT
# ---------------------------------------------------------

with col1:

    st.markdown("### 🔎 Search Agent")

    st.markdown(
        '<div class="agent-description">'
        'Searches the web for recent, reliable and relevant information.'
        '</div>',
        unsafe_allow_html=True
    )


# ---------------------------------------------------------
# READER AGENT
# ---------------------------------------------------------

with col2:

    st.markdown("### 📖 Reader Agent")

    st.markdown(
        '<div class="agent-description">'
        'Selects the best source and extracts deeper information.'
        '</div>',
        unsafe_allow_html=True
    )


# ---------------------------------------------------------
# WRITER AGENT
# ---------------------------------------------------------

with col3:

    st.markdown("### ✍️ Writer Agent")

    st.markdown(
        '<div class="agent-description">'
        'Uses the collected research to create a detailed report.'
        '</div>',
        unsafe_allow_html=True
    )


# ---------------------------------------------------------
# CRITIC AGENT
# ---------------------------------------------------------

with col4:

    st.markdown("### 🧐 Critic Agent")

    st.markdown(
        '<div class="agent-description">'
        'Reviews the generated report and provides critical feedback.'
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# RESEARCH INPUT
# =========================================================

st.markdown(
    '<div class="section-heading">🔬 Start Your Research</div>',
    unsafe_allow_html=True
)


topic = st.text_area(
    "Research Topic",
    placeholder=(
        "Example: Impact of Generative AI and Large Language "
        "Models on the Future of Software Development"
    ),
    height=120,
    label_visibility="collapsed"
)


# =========================================================
# START RESEARCH BUTTON
# =========================================================

if st.button("🚀 Start AI Research", type="primary"):

    if not topic.strip():

        st.warning("⚠️ Please enter a research topic first.")

    else:

        st.session_state["topic"] = topic

        # ---------------------------------------------
        # Progress bar
        # ---------------------------------------------

        progress = st.progress(0)

        # ---------------------------------------------
        # Status box
        # ---------------------------------------------

        status = st.status(
            "🚀 ResearchMind AI is working...",
            expanded=True
        )

        try:

            # -----------------------------------------
            # STEP 1
            # -----------------------------------------

            status.write(
                "🔎 Search Agent is searching for recent information..."
            )

            progress.progress(15)


            # -----------------------------------------
            # STEP 2
            # -----------------------------------------

            status.write(
                "📖 Reader Agent is analyzing relevant resources..."
            )

            progress.progress(35)


            # -----------------------------------------
            # STEP 3
            # -----------------------------------------

            status.write(
                "✍️ Writer Agent is preparing the research report..."
            )

            progress.progress(65)


            # -----------------------------------------
            # STEP 4
            # -----------------------------------------

            status.write(
                "🧐 Critic Agent is reviewing the generated report..."
            )

            progress.progress(85)


            # -----------------------------------------
            # ACTUAL PIPELINE
            # -----------------------------------------

            result = run_research_pipeline(topic)


            # -----------------------------------------
            # COMPLETE
            # -----------------------------------------

            progress.progress(100)

            status.update(
                label="✅ Research completed successfully!",
                state="complete",
                expanded=False
            )


            # Save result
            st.session_state["research_result"] = result

            st.success(
                "🎉 Your multi-agent research report is ready!"
            )


        except Exception as e:

            status.update(
                label="❌ Research pipeline failed",
                state="error",
                expanded=True
            )

            st.error(f"Error: {str(e)}")


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


    # =====================================================
    # GET RESULTS
    # =====================================================

    search_data = result.get(
        "search_results",
        ""
    )

    scraped_data = result.get(
        "scraped_content",
        ""
    )

    report = result.get(
        "report",
        ""
    )

    feedback = result.get(
        "feedback",
        ""
    )


    # =====================================================
    # HANDLE LANGCHAIN AIMESSAGE
    # =====================================================

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

        st.metric(
            "🤖 AI Agents",
            "4"
        )


    with m2:

        st.metric(
            "🔎 Search",
            "Completed"
        )


    with m3:

        st.metric(
            "📝 Report",
            "Generated"
        )


    with m4:

        st.metric(
            "🧐 Review",
            "Completed"
        )


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
    # FINAL REPORT
    # =====================================================

    with tab1:

        st.subheader(
            "📝 AI Generated Research Report"
        )

        st.markdown(
            str(report)
        )


        st.download_button(
            label="⬇️ Download Research Report",
            data=str(report),
            file_name="research_report.txt",
            mime="text/plain"
        )


    # =====================================================
    # CRITIC REVIEW
    # =====================================================

    with tab2:

        st.subheader(
            "🧐 Critic Agent Feedback"
        )

        st.markdown(
            str(feedback)
        )


    # =====================================================
    # SEARCH RESULTS
    # =====================================================

    with tab3:

        st.subheader(
            "🔎 Search Agent Output"
        )

        st.write(
            search_data
        )


    # =====================================================
    # SCRAPED CONTENT
    # =====================================================

    with tab4:

        st.subheader(
            "📖 Reader Agent Output"
        )

        st.write(
            scraped_data
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "MULTI AI RESEARCH SYSTEM • Search → Read → Write → Critique"
)
