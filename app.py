import streamlit as st
from google import genai
import pandas as pd

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="EduPredict AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# GEMINI CLIENT
# =========================================================

try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    client = None

# =========================================================
# CYBER-DARK THEME
# =========================================================

st.markdown("""
    <style>
    .stApp {
        background-color: #030712;
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }

    .stTextInput label p,
    .stNumberInput label p,
    .stSlider label p,
    .stRadio label p,
    .stSelectbox label p {
        color: #94a3b8 !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea {
        background-color: #0f172a !important;
        color: #ffffff !important;
        border: 1px solid #1e293b !important;
        border-radius: 8px !important;
    }

    .stButton button,
    .stDownloadButton button {
        background: linear-gradient(
            135deg,
            #6366f1 0%,
            #4f46e5 100%
        ) !important;

        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        letter-spacing: 0.025em;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }

    .stButton button:hover,
    .stDownloadButton button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 18px rgba(99, 102, 241, 0.45);
    }

    .glass-panel {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(30, 41, 59, 0.8);
        padding: 24px;
        border-radius: 16px;
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }

    hr {
        border-color: #1e293b;
        margin: 2rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello Teacher! I am your AI assistant. "
                "How can I help optimize your classroom today?"
            )
        }
    ]

if "class_portfolio" not in st.session_state:
    st.session_state.class_portfolio = pd.DataFrame(
        columns=[
            "Name",
            "Roll No",
            "Class",
            "Exam",
            "Attendance (%)",
            "Assignments (%)",
            "Average (%)"
        ]
    )

# =========================================================
# HEADER
# =========================================================

col_head1, col_head2 = st.columns([3, 1])

with col_head1:
    st.markdown(
        """
        ### ⚡ EduPredict AI
        <span style='color:#6366f1; font-size: 1rem;'>
        // Enterprise Classroom Intelligence
        </span>
        """,
        unsafe_allow_html=True
    )

with col_head2:
    exam_phase = st.selectbox(
        "Active Evaluation Phase",
        ["PT-1", "Half Yearly", "PT-2", "Preboards"]
    )

    max_marks = 40 if "PT" in exam_phase else 80

st.markdown(
    "<hr style='margin: 1rem 0;'>",
    unsafe_allow_html=True
)

# =========================================================
# MAIN LAYOUT
# =========================================================

left_col, right_col = st.columns([4, 8], gap="large")

# =========================================================
# LEFT SIDE
# =========================================================

with left_col:

    # -----------------------------------------------------
    # STUDENT IDENTITY
    # -----------------------------------------------------

    st.markdown(
        "<div class='glass-panel'>",
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <h4 style='color:#f8fafc; font-size:1rem; margin-bottom:1rem;'>
        👤 Student Identity Credentials
        </h4>
        """,
        unsafe_allow_html=True
    )

    student_name = st.text_input(
        "Full Name",
        placeholder="e.g., Aarav Sharma"
    )

    r_col1, r_col2 = st.columns(2)

    with r_col1:
        roll_no = st.text_input(
            "Roll No.",
            placeholder="04"
        )

    with r_col2:
        class_sec = st.text_input(
            "Class/Sec",
            placeholder="10-B"
        )

    st.markdown(
        "</div><br>",
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # BEHAVIORAL TELEMETRY
    # -----------------------------------------------------

    st.markdown(
        "<div class='glass-panel'>",
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <h4 style='color:#f8fafc; font-size:1rem; margin-bottom:1rem;'>
        🏫 Behavioral Telemetry
        </h4>
        """,
        unsafe_allow_html=True
    )

    attendance = st.slider(
        "Attendance Rate (%)",
        0,
        100,
        88
    )

    assignments = st.slider(
        "Assignment Completion (%)",
        0,
        100,
        92
    )

    participation = st.slider(
        "Class Participation Score",
        1,
        10,
        8
    )

    behavior = st.slider(
        "Classroom Conduct Index",
        1,
        10,
        9
    )

    st.markdown(
        "</div><br>",
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # SUBJECT SCORE MATRIX
    # -----------------------------------------------------

    st.markdown(
        "<div class='glass-panel'>",
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <h4 style='color:#f8fafc; font-size:1rem; margin-bottom:1rem;'>
        📚 Subject Score Matrix
        </h4>
        """,
        unsafe_allow_html=True
    )

    lang_opt = st.radio(
        "Language Elective",
        ["Hindi", "Sanskrit", "French"],
        horizontal=True
    )

    skill_opt = st.radio(
        "Skill Elective",
        ["Financial Literacy", "AI", "Computer"],
        horizontal=True
    )

    if skill_opt == "AI":
        max_skill_marks = 35 if "PT" in exam_phase else 50
    else:
        max_skill_marks = max_marks

    sc_math = st.number_input(
        f"Mathematics (Max: {max_marks})",
        0.0,
        float(max_marks),
        float(int(max_marks * 0.75)),
        step=0.5
    )

    sc_sci = st.number_input(
        f"Science (Max: {max_marks})",
        0.0,
        float(max_marks),
        float(int(max_marks * 0.70)),
        step=0.5
    )

    sc_sst = st.number_input(
        f"Social Science (Max: {max_marks})",
        0.0,
        float(max_marks),
        float(int(max_marks * 0.70)),
        step=0.5
    )

    sc_eng = st.number_input(
        f"English (Max: {max_marks})",
        0.0,
        float(max_marks),
        float(int(max_marks * 0.80)),
        step=0.5
    )

    sc_lang = st.number_input(
        f"{lang_opt} (Max: {max_marks})",
        0.0,
        float(max_marks),
        float(int(max_marks * 0.85)),
        step=0.5
    )

    sc_skill = st.number_input(
        f"{skill_opt} (Max: {max_skill_marks})",
        0.0,
        float(max_skill_marks),
        float(int(max_skill_marks * 0.90)),
        step=0.5
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

# =========================================================
# CALCULATIONS
# =========================================================

scores = {
    "Mathematics": (sc_math / max_marks) * 100,
    "Science": (sc_sci / max_marks) * 100,
    "Social Science": (sc_sst / max_marks) * 100,
    "English": (sc_eng / max_marks) * 100,
    lang_opt: (sc_lang / max_marks) * 100,
    skill_opt: (sc_skill / max_skill_marks) * 100
}

avg_score = sum(scores.values()) / len(scores)

# Dynamic gain potential
gain_potential = max(0, 95 - avg_score)

# Risk calculation
if avg_score >= 75 and attendance >= 75:
    risk_text = "LOW RISK 🟢"
    risk_color = "#10b981"
elif avg_score >= 50 and attendance >= 65:
    risk_text = "MODERATE RISK 🟡"
    risk_color = "#f59e0b"
else:
    risk_text = "HIGH RISK 🔴"
    risk_color = "#ef4444"

# =========================================================
# RIGHT SIDE
# =========================================================

with right_col:

    # -----------------------------------------------------
    # KPI GRID
    # -----------------------------------------------------

    kpi1, kpi2, kpi3 = st.columns(3)

    with kpi1:
        st.markdown(
            f"""
            <div class='glass-panel' style='text-align:center; padding:15px;'>
                <p style='color:#94a3b8; font-size:0.75rem;
                text-transform:uppercase;'>Predicted Average</p>

                <h3 style='color:#818cf8; font-size:1.8rem; margin:0;'>
                    {avg_score:.1f}%
                </h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    with kpi2:
        st.markdown(
            f"""
            <div class='glass-panel' style='text-align:center; padding:15px;'>
                <p style='color:#94a3b8; font-size:0.75rem;
                text-transform:uppercase;'>Risk Profile</p>

                <h3 style='color:{risk_color};
                font-size:1.2rem; margin-top:5px;'>
                    {risk_text}
                </h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    with kpi3:
        st.markdown(
            f"""
            <div class='glass-panel' style='text-align:center; padding:15px;'>
                <p style='color:#94a3b8; font-size:0.75rem;
                text-transform:uppercase;'>Gain Potential</p>

                <h3 style='color:#10b981;
                font-size:1.8rem; margin:0;'>
                    +{gain_potential:.1f}%
                </h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # -----------------------------------------------------
    # ROSTER
    # -----------------------------------------------------

    st.markdown(
        "#### 📊 Live Master Class Roster Database"
    )

    if not st.session_state.class_portfolio.empty:
        st.dataframe(
            st.session_state.class_portfolio,
            use_container_width=True
        )
    else:
        st.info(
            "💡 Portfolio database is currently empty. "
            "Input student parameters on the left and click "
            "'Add Student'."
        )

    # -----------------------------------------------------
    # ACTION BUTTONS
    # -----------------------------------------------------

    btn_col1, btn_col2, btn_col3 = st.columns(3)

    with btn_col1:

        if st.button(
            "➕ Add Student to Roster",
            use_container_width=True
        ):

            if not student_name.strip():

                st.error(
                    "⚠️ Enter a valid student name."
                )

            else:

                new_student = pd.DataFrame({
                    "Name": [student_name],
                    "Roll No": [roll_no],
                    "Class": [class_sec],
                    "Exam": [exam_phase],
                    "Attendance (%)": [attendance],
                    "Assignments (%)": [assignments],
                    "Average (%)": [round(avg_score, 1)]
                })

                st.session_state.class_portfolio = pd.concat(
                    [
                        st.session_state.class_portfolio,
                        new_student
                    ],
                    ignore_index=True
                )

                st.success(
                    f"✅ {student_name} added to roster."
                )

                st.rerun()

    with btn_col2:

        if not st.session_state.class_portfolio.empty:

            csv_file = (
                st.session_state.class_portfolio
                .to_csv(index=False)
                .encode("utf-8")
            )

            st.download_button(
                label="📥 Export Master CSV",
                data=csv_file,
                file_name=f"CBSE_Class_Portfolio_{exam_phase}.csv",
                mime="text/csv",
                use_container_width=True
            )

        else:

            st.button(
                "📥 Export Master CSV",
                disabled=True,
                use_container_width=True
            )

    with btn_col3:

        if st.button(
            "🗑️ Reset Database",
            use_container_width=True
        ):

            st.session_state.class_portfolio = pd.DataFrame(
                columns=[
                    "Name",
                    "Roll No",
                    "Class",
                    "Exam",
                    "Attendance (%)",
                    "Assignments (%)",
                    "Average (%)"
                ]
            )

            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

    # =====================================================
    # AI DIAGNOSTIC REPORT
    # =====================================================

    if st.button(
        "🚀 Run Deep AI Telemetry & Diagnostic Report",
        use_container_width=True
    ):

        if not student_name.strip():

            st.error(
                "⚠️ Please specify a student name before "
                "triggering diagnostics."
            )

        elif client is None:

            st.error(
                "❌ Gemini API key is missing. "
                "Please configure GEMINI_API_KEY in Streamlit secrets."
            )

        else:

            with st.spinner(
                "Synthesizing behavioral metrics with Gemini..."
            ):

                try:

                    subject_text = "\n".join(
                        [
                            f"- {subject}: {score:.1f}%"
                            for subject, score in scores.items()
                        ]
                    )

                    prompt = f"""
Act as an elite CBSE Class 10 academic coordinator.

Analyze the following student.

STUDENT
Name: {student_name}
Class: {class_sec}
Roll No: {roll_no}
Evaluation Phase: {exam_phase}

BEHAVIORAL TELEMETRY
Attendance: {attendance}%
Assignment Completion: {assignments}%
Class Participation: {participation}/10
Classroom Conduct: {behavior}/10

SUBJECT PERFORMANCE
{subject_text}

OVERALL AVERAGE
{avg_score:.1f}%

RISK PROFILE
{risk_text}

GAIN POTENTIAL
+{gain_potential:.1f}%

Provide a concise executive diagnostic covering:

1. Overall academic trajectory
2. Strongest subjects
3. Weakest subjects
4. Attendance and behavioral observations
5. Main academic risks
6. Three specific tactical intervention strategies
7. A realistic short-term improvement target

Keep the response practical for a CBSE Class 10 teacher.
Do not invent marks or information that was not provided.
"""

                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt
                    )

                    st.markdown(
                        "<div class='glass-panel'>",
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        "#### 📑 Diagnostic Output Matrix"
                    )

                    st.write(response.text)

                    st.markdown(
                        "</div>",
                        unsafe_allow_html=True
                    )

                except Exception as e:

                    st.error(
                        f"❌ AI Generation Failed: {e}"
                    )

# =========================================================
# FLOATING AI TEACHER ASSISTANT
# =========================================================

with st.popover(
    "💬 AI Teacher Assistant",
    help="Click to open popup assistant"
):

    st.markdown(
        "#### ⚡ Quick Pedagogy AI"
    )

    st.caption(
        "Ask for lesson plans, parent emails, grading guidance, "
        "remedial strategies, or classroom ideas."
    )

    chat_container = st.container(height=320)

    with chat_container:

        for message in st.session_state.messages:

            with st.chat_message(message["role"]):

                st.markdown(
                    message["content"]
                )

    chat_prompt = st.text_input(
        "Type a prompt...",
        key="teacher_prompt",
        placeholder="e.g. Create a revision plan for Class 10 Maths"
    )

    if st.button(
        "Send",
        key="send_teacher_prompt",
        use_container_width=True
    ):

        if not chat_prompt.strip():

            st.warning(
                "Please enter a prompt."
            )

        elif client is None:

            st.error(
                "❌ Gemini API key is missing."
            )

        else:

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": chat_prompt
                }
            )

            try:

                chat_resp = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=chat_prompt
                )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": chat_resp.text
                    }
                )

                st.rerun()

            except Exception as e:

                st.error(
                    f"❌ Chat Error: {e}"
                )
