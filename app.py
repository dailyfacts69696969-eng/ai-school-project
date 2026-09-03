import streamlit as st
from google import genai
import pandas as pd

# Connect to Gemini
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# Setup Page layout and hidden Custom CSS for the dark glassmorphism look
st.set_page_config(page_title="EduPredict AI", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
    <style>
    .stApp { background-color: #020617; color: #f1f5f9; }
    
    /* FIX FOR INVISIBLE LABELS: Make text above input boxes white */
    .stTextInput label p, .stNumberInput label p, .stSlider label p, .stRadio label p, .stSelectbox label p {
        color: #f8fafc !important;
        font-weight: 600 !important;
    }
    
    /* Input box styling */
    .stTextInput input, .stNumberInput input, .stChatInput textarea {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 1px solid #334155 !important;
    }
    
    /* Button styling */
    .stButton button, .stDownloadButton button {
        background-color: #6366f1 !important;
        color: #ffffff !important;
        border: none !important;
    }
    .stButton button:hover, .stDownloadButton button:hover {
        background-color: #4f46e5 !important;
    }
    
    div[data-testid="stMetricValue"] { color: #818cf8; font-size: 2rem; font-weight: 800; }
    div[data-testid="stMetricLabel"] { color: #94a3b8; font-size: 0.9rem; }
    .glass-panel { background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(30, 41, 59, 0.8); padding: 20px; border-radius: 15px; box-shadow: 0 0 15px rgba(99, 102, 241, 0.1); }
    hr { border-color: #1e293b; }
    </style>
""", unsafe_allow_html=True)

# Initialize background memory for Chat AND the Class Portfolio
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi Teacher! I am your AI assistant. Need help writing a parent email or generating a quick lesson plan?"}]

if "class_portfolio" not in st.session_state:
    st.session_state.class_portfolio = pd.DataFrame()

# --- HEADER SECTION ---
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.markdown("### 🧠 EduPredict AI: Dynamic Student Performance Engine")
with col_head2:
    exam_phase = st.selectbox("Exam Phase", ["PT-1", "Half Yearly", "PT-2", "Preboards"])
    # Standard subjects max marks
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
    
    # --- DYNAMIC SKILL MARKS LOGIC ---
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
    # Calculate percentages for the UI charts
    scores = {
        "Maths": (sc_math/max_marks)*100, 
        "Science": (sc_sci/max_marks)*100, 
        "SST": (sc_sst/max_marks)*100, 
        "English": (sc_eng/max_marks)*100, 
        lang_opt: (sc_lang/max_marks)*100, 
        skill_opt: (sc_skill/max_skill_marks)*100
    }
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
    
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.markdown("**Factor Impact Breakdown**")
        factor_data = pd.DataFrame({"Factor": ["Attendance", "Assignments", "Participation", "Behavior"], "Impact": [15.0, 12.0, 5.0, 3.0]}).set_index("Factor")
        st.bar_chart(factor_data, color="#818cf8")
    with chart_col2:
        st.markdown("**Subject Performance (%)**")
        sub_data = pd.DataFrame({"Subject": list(scores.keys()), "Score": list(scores.values())}).set_index("Subject")
        st.bar_chart(sub_data, color="#10b981")

    st.markdown("---")
    
    # --- MULTI-STUDENT PORTFOLIO & AI REPORT ---
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    with btn_col1:
        # Button to add current student to the master list
        if st.button("➕ Add Student to Portfolio", use_container_width=True):
            if not student_name:
                st.error("Please enter a Name!")
            else:
                new_student = pd.DataFrame({
                    "Name": [student_name], "Roll No": [roll_no], "Class": [class_sec], "Exam": [exam_phase],
                    "Attendance (%)": [attendance], "Assignments (%)": [assignments], 
                    "Math": [sc_math], "Science": [sc_sci], "SST": [sc_sst], "English": [sc_eng],
                    lang_opt: [sc_lang], skill_opt: [sc_skill], "Average (%)": [round(avg_score, 1)]
                })
                # Append to the background memory
                st.session_state.class_portfolio = pd.concat([st.session_state.class_portfolio, new_student], ignore_index=True)
                st.success(f"Added! ({len(st.session_state.class_portfolio)} students in portfolio)")

    with btn_col2:
        # Download the entire portfolio of all saved students
        if not st.session_state.class_portfolio.empty:
            csv_file = st.session_state.class_portfolio.to_csv(index=False).encode('utf-8')
            st.download_button(
                label=f"📥 Download Portfolio CSV ({len(st.session_state.class_portfolio)})",
                data=csv_file,
                file_name=f"Class_Portfolio_{exam_phase.split()[0]}.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.button("📥 Download Portfolio (Empty)", disabled=True, use_container_width=True)

    with btn_col3:
        run_analysis = st.button("🚀 Run Deep AI Report", use_container_width=True)

    if run_analysis:
        if not student_name:
            st.error("⚠️ Please enter a student name on the left before running the analysis.")
        else:
            with st.spinner("Connecting to EduPredict AI Core..."):
                # FIXED: The exact, working model name for the AI!
                report_prompt = f"""
                Act as a strict CBSE Data Analyst assisting a classroom teacher.
                Student: {student_name} ({class_sec}, Roll: {roll_no}). Exam Phase: {exam_phase}
                School Telemetry: {attendance}% attendance, {assignments}% assignments, {participation}/10 participation, {behavior}/10 behavior.
                Scores (%): Math {scores['Maths']:.1f}, Sci {scores['Science']:.1f}, SST {scores['SST']:.1f}, Eng {scores['English']:.1f}, {lang_opt} {scores[lang_opt]:.1f}, {skill_opt} {scores[skill_opt]:.1f}.
                Provide a structured, 4-bullet point report highlighting weaknesses and actionable strategies.
                """
                report_resp = client.models.generate_content(model="gemini-1.5-flash", contents=report_prompt)
                st.info("Report Output:")
                st.write(report_resp.text)

    # --- THE NEW TEACHER AI WIDGET ---
    st.markdown("---")
    st.markdown("#### 💬 Quick Teacher Assistant")
    
    chat_box = st.container(height=300)
    
    with chat_box:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Ask me for lesson plans, email templates, or grading advice..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_box:
            with st.chat_message("user"):
                st.markdown(prompt)
                
            with st.chat_message("assistant"):
                # FIXED: The exact, working model name for the Chat!
                chat_resp = client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
                st.markdown(chat_resp.text)
                
        st.session_state.messages.append({"role": "assistant", "content": chat_resp.text})
