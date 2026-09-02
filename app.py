import streamlit as st
from google import genai
import pandas as pd
import random

# Connect to Gemini
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

st.set_page_config(page_title="AI Teacher Dashboard", layout="wide")

# --- HEADER & CONTROL BAR ---
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.title("⚡ Dynamic Student Performance AI")
    st.caption("Live Telemetry & Predictive Analytics Dashboard")
with col2:
    st.info("🟢 Live Feed: Active")
with col3:
    preset = st.selectbox("Quick-Load Student Profile", ["Custom", "High Achiever", "Average", "At-Risk"])

# Preset Logic (Mocking telemetry changes based on preset)
if preset == "High Achiever":
    def_study, def_sleep, def_screen, def_att = 20, 8, 2, 98
elif preset == "At-Risk":
    def_study, def_sleep, def_screen, def_att = 4, 5, 8, 65
else:
    def_study, def_sleep, def_screen, def_att = 10, 7, 4, 85

st.markdown("---")

# --- EXAM & SUBJECT SETUP ---
st.subheader("📋 Academic Framework")
exam_col1, exam_col2, exam_col3 = st.columns(3)

with exam_col1:
    exam_phase = st.selectbox("Exam Phase", ["PT-1", "Half Yearly", "PT-2", "Preboards 1", "Preboards 2"])
    # Dynamically set max marks based on exam phase
    max_marks = 40 if "PT" in exam_phase else 80
    st.write(f"**Max Marks for this exam: {max_marks}**")

with exam_col2:
    lang_opt = st.radio("Select Language Elective", ["Hindi", "Sanskrit", "French"])

with exam_col3:
    skill_opt = st.radio("Select Skill Elective", ["Financial Literacy", "Artificial Intelligence", "Computer Applications"])

st.markdown("---")

# --- TELEMETRY & SCORES PANEL ---
left_col, right_col = st.columns([1, 1])

with left_col:
    st.subheader("🎛️ Lifestyle & Habit Telemetry")
    attendance = st.slider("Attendance Rate (%)", 0, 100, def_att)
    study_hours = st.slider("Weekly Study Hours", 0, 40, def_study)
    sleep = st.slider("Daily Sleep (hrs)", 0, 12, def_sleep)
    screen_time = st.slider("Non-Academic Screen Time (hrs)", 0, 12, def_screen)
    participation = st.slider("Class Participation Score", 1, 10, 7)

with right_col:
    st.subheader(f"📝 {exam_phase} Score Entry (out of {max_marks})")
    sc_math = st.number_input("Mathematics", 0, max_marks, int(max_marks * 0.75))
    sc_sci = st.number_input("Science", 0, max_marks, int(max_marks * 0.70))
    sc_sst = st.number_input("Social Science (SST)", 0, max_marks, int(max_marks * 0.70))
    sc_eng = st.number_input("English", 0, max_marks, int(max_marks * 0.80))
    sc_lang = st.number_input(f"{lang_opt}", 0, max_marks, int(max_marks * 0.85))
    sc_skill = st.number_input(f"{skill_opt}", 0, max_marks, int(max_marks * 0.90))

# --- DATA PROCESSING FOR CHARTS & KPIs ---
# Calculate percentages for fair comparison
scores = {
    "Maths": (sc_math / max_marks) * 100,
    "Science": (sc_sci / max_marks) * 100,
    "SST": (sc_sst / max_marks) * 100,
    "English": (sc_eng / max_marks) * 100,
    lang_opt: (sc_lang / max_marks) * 100,
    skill_opt: (sc_skill / max_marks) * 100,
}
avg_score = sum(scores.values()) / len(scores)

st.markdown("---")

# --- TOP-LEVEL KPI METRIC CARDS ---
st.subheader("📊 Real-Time Analytics")
kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    st.metric(label="Current Academic Average", value=f"{avg_score:.1f}%", delta=f"{random.randint(-3, 3)}% from last exam")
with kpi2:
    risk = "Low Risk 🟢" if avg_score > 75 and attendance > 80 else "Moderate Risk 🟡" if avg_score > 50 else "High Risk 🔴"
    st.metric(label="Student Risk Assessment", value=risk)
with kpi3:
    potential = "+12%" if sleep < 7 or screen_time > 4 else "+4%"
    st.metric(label="Improvement Potential", value=potential, help="Based on optimizing current sleep and screen time habits.")

# --- VISUAL ANALYTICS ---
chart_data = pd.DataFrame({
    "Subject": list(scores.keys()),
    "Percentage (%)": list(scores.values())
})
st.bar_chart(chart_data, x="Subject", y="Percentage (%)", color="#4CAF50")

# --- SIMULATION TERMINAL & AI FEED ---
st.markdown("---")
st.subheader("🧠 AI Generation & Event Terminal")

if st.button("🚀 Run Deep AI Analysis"):
    with st.spinner("Compiling telemetry and querying Gemini..."):
        
        # Terminal mock output
        st.code("""
        [SYSTEM] Initiating analysis...
        [TELEMETRY] Logging attendance and screen time impacts...
        [CALCULATING] Mapping subject deficits to CBSE syllabus...
        [API] Connecting to Generative AI...
        """, language="bash")
        
        prompt = f"""
        Act as an expert CBSE Class 10 Data Analyst. 
        Exam: {exam_phase} (Max {max_marks} marks).
        
        Student Habits:
        - Study Hours: {study_hours}/week
        - Sleep: {sleep} hrs/day
        - Screen Time: {screen_time} hrs/day
        - Attendance: {attendance}%
        
        Scores (Converted to %):
        - Math: {scores['Maths']:.1f}%
        - Science: {scores['Science']:.1f}%
        - SST: {scores['SST']:.1f}%
        - English: {scores['English']:.1f}%
        - {lang_opt}: {scores[lang_opt]:.1f}%
        - {skill_opt}: {scores[skill_opt]:.1f}%
        
        Provide:
        1. A brief predictive grade (A, B, C) for the upcoming board exams based on these habits and scores.
        2. A habit-impact breakdown (how their specific screen time or sleep is affecting their weak subjects).
        3. Dynamic, targeted recommendations for teachers to intervene.
        """
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        st.success("Analysis Complete!")
        st.write(response.text)
