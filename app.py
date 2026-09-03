import streamlit as st
from google import genai
import pandas as pd

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

st.set_page_config(page_title="EduPredict AI", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
    <style>
    .stApp { background-color: #020617; color: #f1f5f9; }
    .stTextInput label p, .stNumberInput label p, .stSlider label p, .stRadio label p, .stSelectbox label p {
        color: #f8fafc !important; font-weight: 600 !important;
    }
    .stTextInput input, .stNumberInput input, .stChatInput textarea {
        background-color: #1e293b !important; color: #ffffff !important; border: 1px solid #334155 !important;
    }
    .stButton button, .stDownloadButton button {
        background-color: #6366f1 !important; color: #ffffff !important; border: none !important;
    }
    .glass-panel { background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(30, 41, 59, 0.8); padding: 20px; border-radius: 15px; }
    hr { border-color: #1e293b; }
    </style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi Teacher! I am your AI assistant. Ready to manage your class roster?"}]

if "class_portfolio" not in st.session_state:
    st.session_state.class_portfolio = pd.DataFrame(columns=["Name", "Roll No", "Class", "Exam", "Average (%)"])

col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.markdown("### 🧠 EduPredict AI: Class Roster & Portfolio Engine")
with col_head2:
    exam_phase = st.selectbox("Exam Phase", ["PT-1", "Half Yearly", "PT-2", "Preboards"])
    max_marks = 40 if "PT" in exam_phase else 80

st.markdown("---")

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
    
    if skill_opt == "AI":
        max_skill_marks = 35 if "PT" in exam_phase else 50
    else:
        max_skill_marks = max_marks 
        
    sc_math = st.number_input(f"Mathematics (out of {max_marks})", 0.0, float(max_marks), float(int(max_marks*0.75)), step=0.5)
    sc_sci = st.number_input(f"Science (out of {max_marks})", 0.0, float(max_marks), float(int(max_marks*0.70)), step=0.5)
    sc_sst = st.number_input(f"Social Science (out of {max_marks})", 0.0, float(max_marks), float(int(max_marks*0.70)), step=0.5)
    sc_eng = st.number_input(f"English (out of {max_marks})", 0.0, float(max_marks), float(int(max_marks*0.80)), step=0.5)
    sc_lang = st.number_input(f"{lang_opt} (out of {max_marks})", 0.0, float(max_marks), float(int(max_marks*0.85)), step=0.5)
    sc_skill = st.number_input(f"{skill_opt} (out of {max_skill_marks})", 0.0, float(max_skill_marks), float(int(max_skill_marks*0.90)), step=0.5)

with right_col:
    scores = {
        "Maths": (sc_math/max_marks)*100, "Science": (sc_sci/max_marks)*100, 
        "SST": (sc_sst/max_marks)*100, "English": (sc_eng/max_marks)*100, 
        lang_opt: (sc_lang/max_marks)*100, skill_opt: (sc_skill/max_skill_marks)*100
    }
    avg_score = sum(scores.values()) / len(scores)
    
    st.markdown("#### 📊 Live Class Roster Preview")
    
    # Show the table of added students dynamically on screen
    if not st.session_state.class_portfolio.empty:
        st.dataframe(st.session_state.class_portfolio, use_container_width=True)
    else:
        st.info("No students added to the portfolio yet. Fill out the form on the left and click 'Add Student'.")

    st.markdown("---")
    
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    with btn_col1:
        if st.button("➕ Add Student to Portfolio", use_container_width=True):
            if not student_name:
                st.error("Please enter a Student Name!")
            else:
                new_student = pd.DataFrame({
                    "Name": [student_name], "Roll No": [roll_no], "Class": [class_sec], "Exam": [exam_phase],
                    "Attendance (%)": [attendance], "Assignments (%)": [assignments], 
                    "Average (%)": [round(avg_score, 1)]
                })
                st.session_state.class_portfolio = pd.concat([st.session_state.class_portfolio, new_student], ignore_index=True)
                st.rerun()

    with btn_col2:
        if not st.session_state.class_portfolio.empty:
            csv_file = st.session_state.class_portfolio.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Master CSV", data=csv_file,
                file_name=f"Class_Portfolio_{exam_phase}.csv", mime="text/csv", use_container_width=True
            )
        else:
            st.button("📥 Download Master CSV", disabled=True, use_container_width=True)

    with btn_col3:
        if st.button("🗑️ Clear Roster", use_container_width=True):
            st.session_state.class_portfolio = pd.DataFrame(columns=["Name", "Roll No", "Class", "Exam", "Average (%)"])
            st.rerun()

    st.markdown("---")
    if st.button("🚀 Run Deep AI Report for Current Student", use_container_width=True):
        if not student_name:
            st.error("⚠️ Please enter a student name on the left.")
        else:
            with st.spinner("Analyzing telemetry..."):
                prompt = f"Act as a CBSE Data Analyst. Student: {student_name}, Exam: {exam_phase}, Attendance: {attendance}%. Average Score: {avg_score:.1f}%. Provide 3 bullet points of feedback."
                resp = client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
                st.write(resp.text)
