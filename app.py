import streamlit as st
from pipeline import run_research_pipeline


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="MULTI AGENT RESEARCH SYSTEM",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

    /* ================================
       GLOBAL
       ================================ */

    .stApp {
        background: #080b16;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    /* Remove top decoration */
    [data-testid="stHeader"] {
        background: transparent;
    }


    /* ================================
       SIDEBAR
       ================================ */

    section[data-testid="stSidebar"] {
        background: #0b0f1c;
        border-right: 1px solid #20263a;
    }

    section[data-testid="stSidebar"] h1 {
        font-size: 21px;
        font-weight: 800;
    }


    /* ================================
       HEADER
       ================================ */

    .header-badge {
        text-align: center;
        color: #a78bfa;
        font-size: 14px;
        font-weight: 700;
        letter-spacing: 2px;
        margin-bottom: 10px;
    }

    .header-title {
        text-align: center;
        font-size: 46px;
        font-weight: 850;
        color: #f8fafc;
        margin: 0;
    }

    .header-gradient {
        background: linear-gradient(
            90deg,
            #a78bfa,
            #22d3ee
        );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .header-subtitle {
        text-align: center;
        color: #8993aa;
        font-size: 17px;
        margin-top: 10px;
        margin-bottom: 35px;
    }


    /* ================================
       PIPELINE
       ================================ */

    .pipeline-label {
        color: #7c89a8;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 2px;
        margin-bottom: 10px;
    }

    .agent-number {
        color: #64748b;
        font-size: 12px;
        font-weight: 700;
    }

    .agent-name {
        color: #f8fafc;
        font-size: 18px;
        font-weight: 750;
        margin-top: 6px;
    }

    .agent-desc {
        color: #7f8ba3;
        font-size: 13px;
        line-height: 1.5;
        margin-top: 7px;
    }


    /* ================================
       INPUT SECTION
       ================================ */

    .research-label {
        color: #f8fafc;
        font-size: 25px;
        font-weight: 750;
        margin-top: 35px;
        margin-bottom: 12px;
    }

    textarea {
        background-color: #0f1424 !important;
        border: 1px solid #29334d !important;
        color: #f8fafc !important;
        border-radius: 14px !important;
    }


    /* ================================
       BUTTON
       ================================ */

    .stButton > button {
        width: 100%;
        height: 52px;
        border-radius: 12px;
        font-weight: 750;
        font-size: 16px;
        border: 1px solid #5946a8;
        background: linear-gradient(
            90deg,
            #6d4aff,
            #8b5cf6
        );
    }


    /* ================================
       METRICS
       ================================ */

    [data-testid="stMetric"] {
        background: #0f1424;
        border: 1px solid #222c43;
        border-radius: 14px;
        padding: 16px;
    }


    /* ================================
       TABS
       ================================ */

    button[data-baseweb="tab"] {
        color: #9ca8bd;
        font-weight: 650;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #a78bfa;
    }


    /* ================================
       DIVIDERS
       ================================ */

    hr {
        border-color: #1e2639;
    }


    /* ================================
       STATUS
       ================================ */

    [data-testid="stStatusWidget"] {
        border-radius: 14px;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("# 🧠 MULTI AI")

    st.markdown("### RESEARCH SYSTEM")

    st.caption("Autonomous AI Research Workspace")

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

    st.divider()

    st.caption("Ready to research.")


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="header-badge">AUTONOMOUS AI RESEARCH WORKSPACE</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="header-title">
        🧠 MULTI AI
        <span class="header-gradient">RESEARCH SYSTEM</span>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="header-subtitle">
        Research smarter. Analyze deeper. Generate better insights.
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# PIPELINE HEADER
# =========================================================

st.markdown(
    '<div class="pipeline-label">RESEARCH PIPELINE</div>',
    unsafe_allow_html=True
)


# =========================================================
# AGENT PIPELINE
# =========================================================

col1, arrow1, col2, arrow2, col3, arrow3, col4 = st.columns(
    [2.2, 0.35, 2.2, 0.35, 2.2, 0.35, 2.2]
)


# SEARCH
with col1:

    st.markdown("**01**")

    st.markdown("### 🔎 Search Agent")

    st.caption(
        "Finds recent, reliable and relevant information from the web."
    )


# ARROW
with arrow1:

    st.markdown(
        "<br><br>→",
        unsafe_allow_html=True
    )


# READER
with col2:

    st.markdown("**02**")

    st.markdown("### 📖 Reader Agent")

    st.caption(
        "Selects relevant sources and extracts deeper content."
    )


# ARROW
with arrow2:

    st.markdown(
        "<br><br>→",
        unsafe_allow_html=True
    )


# WRITER
with col3:

    st.markdown("**03**")

    st.markdown("### ✍️ Writer Agent")

    st.caption(
        "Transforms collected research into a structured report."
    )


# ARROW
with arrow3:

    st.markdown(
        "<br><br>→",
        unsafe_allow_html=True
    )


# CRITIC
with col4:

    st.markdown("**04**")

    st.markdown("### 🧐 Critic Agent")

    st.caption(
        "Evaluates the report and provides critical feedback."
    )


# =========================================================
# RESEARCH INPUT
# =========================================================

st.markdown(
    '<div class="research-label">🔬 What do you want to research?</div>',
    unsafe_allow_html=True
)

topic = st.text_area(
    "Research Topic",
    placeholder=(
        "Example: Impact of Generative AI and Large Language Models "
        "on the Future of Software Development"
    ),
    height=120,
    label_visibility="collapsed"
)


# =========================================================
# START BUTTON
# =========================================================

if st.button("🚀 START AI RESEARCH", type="primary"):

    if not topic.strip():

        st.warning(
            "Please enter a research topic before starting."
        )

    else:

        progress = st.progress(0)

        status = st.status(
            "Initializing Multi AI Research System...",
            expanded=True
        )

        try:

            # ------------------------------------------
            # SEARCH
            # ------------------------------------------

            status.write(
                "🔎 Search Agent → Finding recent information..."
            )

            progress.progress(15)


            # ------------------------------------------
            # READER
            # ------------------------------------------

            status.write(
                "📖 Reader Agent → Analyzing relevant resources..."
            )

            progress.progress(35)


            # ------------------------------------------
            # WRITER
            # ------------------------------------------

            status.write(
                "✍️ Writer Agent → Generating research report..."
            )

            progress.progress(65)


            # ------------------------------------------
            # CRITIC
            # ------------------------------------------

            status.write(
                "🧐 Critic Agent → Reviewing generated report..."
            )

            progress.progress(85)


            # ------------------------------------------
            # ACTUAL PIPELINE
            # ------------------------------------------

            result = run_research_pipeline(topic)


            # ------------------------------------------
            # COMPLETE
            # ------------------------------------------

            progress.progress(100)

            status.update(
                label="Research completed successfully!",
                state="complete",
                expanded=False
            )

            st.session_state["research_result"] = result

            st.success(
                "🎉 Multi-agent research completed successfully."
            )

        except Exception as e:

            status.update(
                label="Research pipeline failed",
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

    st.markdown("## 📊 Research Dashboard")

    # =====================================================
    # EXTRACT DATA
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
    # LANGCHAIN AIMESSAGE
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
    # DASHBOARD METRICS
    # =====================================================

    m1, m2, m3, m4 = st.columns(4)

    with m1:

        st.metric(
            "🤖 Agents",
            "4"
        )

    with m2:

        st.metric(
            "🔎 Web Research",
            "Complete"
        )

    with m3:

        st.metric(
            "📝 Report",
            "Ready"
        )

    with m4:

        st.metric(
            "🧐 Review",
            "Complete"
        )


    st.write("")


    # =====================================================
    # OUTPUT TABS
    # =====================================================

    tab1, tab2, tab3, tab4 = st.tabs([
        "📝 FINAL REPORT",
        "🧐 CRITIC REVIEW",
        "🔎 SEARCH DATA",
        "📖 RESEARCH CONTENT"
    ])


    # =====================================================
    # FINAL REPORT
    # =====================================================

    with tab1:

        st.subheader(
            "📝 AI Generated Research Report"
        )

        st.markdown(str(report))

        st.download_button(
            label="⬇️ Download Research Report",
            data=str(report),
            file_name="research_report.txt",
            mime="text/plain"
        )


    # =====================================================
    # CRITIC
    # =====================================================

    with tab2:

        st.subheader(
            "🧐 Critic Agent Review"
        )

        st.markdown(str(feedback))


    # =====================================================
    # SEARCH
    # =====================================================

    with tab3:

        st.subheader(
            "🔎 Search Agent Results"
        )

        st.write(search_data)


    # =====================================================
    # SCRAPED CONTENT
    # =====================================================

    with tab4:

        st.subheader(
            "📖 Reader Agent Research"
        )

        st.write(scraped_data)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "MULTI AI RESEARCH SYSTEM  •  Autonomous Research Pipeline"
)
