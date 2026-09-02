import streamlit as st
from google import genai
import pandas as pd
import random

# Connect to Gemini
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# Setup Page layout and hidden Custom CSS for the dark glassmorphism look
st.set_page_config(page_title="EduPredict AI", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
    <style>
    .stApp { background-color: #020617; color: #f1f5f9; }
    div[data-testid="stMetricValue"] { color: #818cf8; font-size: 2rem; font-weight: 800; }
    div[data-testid="stMetricLabel"] { color: #94a3b8; font-size: 0.9rem; }
    .glass-panel { background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(30, 41, 59, 0.8); padding: 20px; border-radius: 15px; box-shadow: 0 0 15px rgba(99, 102, 241, 0.1); }
    hr { border-color: #1e293b; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.markdown("### 🧠 EduPredict AI: Dynamic Student Performance Engine")
with col_head2:
    exam_phase = st.selectbox("Exam Phase", ["PT-1 (40 Marks)", "Half Yearly (80 Marks)", "PT-2 (40 Marks)", "Preboards (80 Marks)"])
    max_marks = 40 if "PT" in exam_phase else 80

st.markdown("---")

# --- MAIN DASHBOARD LAYOUT ---
left_col, right_col = st.columns([4, 8], gap="large")

with left_col:
    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    st.markdown("#### 👤 Student Identity Profile")
    student_name = st.text_input("Full Name", placeholder="e.g., Rahul Sharma")
    r_col1, r_col2 = st.columns(2)
    with r_col1:
        roll_no = st.text_input("Roll No.", placeholder="12")
    with r_col2:
        class_sec = st.text_input("Class/Sec", placeholder="10-A")
    st.markdown("</div><br>", unsafe_allow_html=True)

    st.markdown("#### 🏫 Academic Telemetry")
    attendance = st.slider("Attendance Rate (%)", 0, 100, 85)
    assignments = st.slider("Assignment Completion (%)", 0, 100, 90)
    participation = st.slider("Class Participation (1-10)", 1, 10, 7)
    behavior = st.slider("Classroom Behavior (1-10)", 1, 10, 8)

    st.markdown("#### 📚 Subject Scores")
    lang_opt = st.radio("Language Elective", ["Hindi", "Sanskrit", "French"], horizontal=True)
    skill_opt = st.radio("Skill Elective", ["Financial Literacy", "AI", "Computer"], horizontal=True)
    
    sc_math = st.number_input("Mathematics", 0, max_marks, int(max_marks*0.75))
    sc_sci = st.number_input("Science", 0, max_marks, int(max_marks*0.70))
    sc_sst = st.number_input("Social Science", 0, max_marks, int(max_marks*0.70))
    sc_eng = st.number_input("English", 0, max_marks, int(max_marks*0.80))
    sc_lang = st.number_input(f"{lang_opt}", 0, max_marks, int(max_marks*0.85))
    sc_skill = st.number_input(f"{skill_opt}", 0, max_marks, int(max_marks*0.90))

with right_col:
    # Calculate basic averages for the UI
    scores = {"Maths": (sc_math/max_marks)*100, "Science": (sc_sci/max_marks)*100, "SST": (sc_sst/max_marks)*100, "English": (sc_eng/max_marks)*100, lang_opt: (sc_lang/max_marks)*100, skill_opt: (sc_skill/max_marks)*100}
    avg_score = sum(scores.values()) / len(scores)
    
    st.markdown("#### 📊 Real-Time Analytics")
    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.metric(label="Current Academic Average", value=f"{avg_score:.1f}%", delta="Grade A" if avg_score > 80 else "Grade B")
    with kpi2:
        st.metric(label="Student Risk Assessment", value="Low 🟢" if avg_score > 75 and attendance > 75 else "High 🔴")
    with kpi3:
        st.metric(label="Max Gain Opportunity", value="+5.5%", delta="via missing assignments", delta_color="normal")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.markdown("**Factor Impact Breakdown**")
        # Updated chart to reflect school factors
        factor_data = pd.DataFrame({"Factor": ["Attendance", "Assignments", "Participation", "Behavior"], "Impact": [15.0, 12.0, 5.0, 3.0]}).set_index("Factor")
        st.bar_chart(factor_data, color="#818cf8")
    with chart_col2:
        st.markdown("**Subject Performance (%)**")
        sub_data = pd.DataFrame({"Subject": list(scores.keys()), "Score": list(scores.values())}).set_index("Subject")
        st.bar_chart(sub_data, color="#10b981")

    st.markdown("---")
    
    # AI Terminal
    if st.button("🚀 Run Deep AI Analysis", use_container_width=True):
        if not student_name:
            st.error("⚠️ Please enter a student name on the left before running the analysis.")
        else:
            with st.spinner("Connecting to EduPredict AI Core..."):
                prompt = f"""
                Act as a strict CBSE Data Analyst assisting a classroom teacher.
                Student: {student_name} ({class_sec}, Roll: {roll_no}).
                Exam Phase: {exam_phase}
                
                School Telemetry:
                - Attendance: {attendance}%
                - Assignment Completion: {assignments}%
                - Class Participation: {participation}/10
                - Classroom Behavior: {behavior}/10
                
                Scores (Converted to %): Math {scores['Maths']:.1f}, Sci {scores['Science']:.1f}, SST {scores['SST']:.1f}, Eng {scores['English']:.1f}, {lang_opt} {scores[lang_opt]:.1f}, {skill_opt} {scores[skill_opt]:.1f}.
                
                Provide a highly structured, 4-bullet point report for the teacher highlighting:
                1. Overall performance summary.
                2. Subject-specific weaknesses based on the scores.
                3. How their specific attendance, missing assignments, or behavior is impacting their grades.
                4. Actionable strategies the teacher can use to help this student improve before the next exam.
                """
                response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
                st.info("Terminal Output:")
                st.write(response.text)
