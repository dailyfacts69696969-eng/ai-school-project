import streamlit as st
from google import genai
import pandas as pd
from PIL import Image

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# --- CYBER-DARK THEME & CUSTOM CSS ---
st.set_page_config(page_title="EduPredict AI", layout="wide", initial_sidebar_state="expanded")
st.markdown("""
    <style>
    .stApp { background-color: #030712; color: #f8fafc; font-family: 'Inter', sans-serif; }
    
    .stTextInput label p, .stNumberInput label p, .stSlider label p, .stRadio label p, .stSelectbox label p {
        color: #94a3b8 !important; font-weight: 500 !important; font-size: 0.85rem !important; text-transform: uppercase; letter-spacing: 0.05em;
    }
    
    .stTextInput input, .stNumberInput input, .stChatInput textarea {
        background-color: #0f172a !important; color: #ffffff !important; border: 1px solid #1e293b !important; border-radius: 8px !important;
    }
    
    .stButton button, .stDownloadButton button {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
        color: #ffffff !important; border: none !important; border-radius: 8px !important;
        font-weight: 600 !important; letter-spacing: 0.025em; transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }
    
    .glass-panel { 
        background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(30, 41, 59, 0.8); 
        padding: 24px; border-radius: 16px; backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    
    hr { border-color: #1e293b; margin: 2rem 0; }
    </style>
""", unsafe_allow_html=True)

# Session States
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello Teacher! I am your AI assistant. How can I help optimize your classroom today?"}]

if "class_portfolio" not in st.session_state:
    st.session_state.class_portfolio = pd.DataFrame(columns=["Name", "Roll No", "Class", "Parent Phone", "Exam", "Attendance (%)", "Assignments (%)", "Average (%)"])

# --- SIDEBAR: AI TEACHER ASSISTANT PANEL ---
with st.sidebar:
    st.markdown("### 💬 AI Teacher Assistant")
    st.caption("Ask for lesson plans, parent emails, or grading guidance.")
    
    chat_container = st.container(height=450)
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if chat_prompt := st.chat_input("Type a prompt..."):
        st.session_state.messages.append({"role": "user", "content": chat_prompt})
        with chat_container:
            with st.chat_message("user"):
                st.markdown(chat_prompt)
            with st.chat_message("assistant"):
                try:
                    chat_resp = client.models.generate_content(model="gemini-3.6-flash", contents=chat_prompt)
                    st.markdown(chat_resp.text)
                    st.session_state.messages.append({"role": "assistant", "content": chat_resp.text})
                except Exception as e:
                    st.error(f"Chat Error: {e}")
        st.rerun()

# --- HEADER BAR ---
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.markdown("### ⚡ EduPredict AI <span style='color:#6366f1; font-size: 1rem;'>// Enterprise Classroom Intelligence</span>", unsafe_allow_html=True)
with col_head2:
    exam_phase = st.selectbox("Active Evaluation Phase", ["PT-1", "Half Yearly", "PT-2", "Preboards"])
    max_marks = 40 if "PT" in exam_phase else 80

st.markdown("<hr style='margin: 1rem 0;'>", unsafe_allow_html=True)

# --- AI DOCUMENT INGESTION HUB ---
with st.expander("📂 AI Document Ingestion & Score Extraction Hub", expanded=False):
    st.markdown("#### 📄 Upload Student Paper / Test Sheet for Auto-Extraction")
    uploaded_paper = st.file_uploader("Upload exam paper or answer sheet (Image)", type=["png", "jpg", "jpeg"], key="paper_up")
    if uploaded_paper and st.button("🤖 Auto-Extract Details & Scores via Gemini"):
        with st.spinner("Reading student paper details..."):
            try:
                image_input = Image.open(uploaded_paper)
                prompt_paper = "Analyze this student document image. Extract the Student Name, Roll Number, and estimate or locate scores for Math, Science, SST, and English as numbers. Format strictly as clear text."
                resp_paper = client.models.generate_content(
                    model="gemini-3.6-flash", 
                    contents=[prompt_paper, image_input]
                )
                st.success("Extraction Complete!")
                st.write(resp_paper.text)
            except Exception as e:
                st.error(f"Extraction failed: {e}")

st.markdown("<hr style='margin: 1rem 0;'>", unsafe_allow_html=True)

# --- SPLIT SCREEN LAYOUT ---
left_col, right_col = st.columns([4, 8], gap="large")

with left_col:
    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#f8fafc; font-size: 1rem; margin-bottom: 1rem;'>👤 Student Identity Credentials</h4>", unsafe_allow_html=True)
    student_name = st.text_input("Full Name", placeholder="e.g., Aarav Sharma")
    r_col1, r_col2 = st.columns(2)
    with r_col1:
        roll_no = st.text_input("Roll No.", placeholder="04")
    with r_col2:
        class_sec = st.text_input("Class/Sec", placeholder="10-B")
    
    parent_phone = st.text_input("Parent Phone Number", placeholder="+91 98765 43210")
    st.markdown("</div><br>", unsafe_allow_html=True)

    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#f8fafc; font-size: 1rem; margin-bottom: 1rem;'>🏫 Behavioral Telemetry</h4>", unsafe_allow_html=True)
    attendance = st.slider("Attendance Rate (%)", 0, 100, 88)
    assignments = st.slider("Assignment Completion (%)", 0, 100, 92)
    participation = st.slider("Class Participation Score", 1, 10, 8)
    behavior = st.slider("Classroom Conduct Index", 1, 10, 9)
    st.markdown("</div><br>", unsafe_allow_html=True)

    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#f8fafc; font-size: 1rem; margin-bottom: 1rem;'>📚 Subject Score Matrix</h4>", unsafe_allow_html=True)
    lang_opt = st.radio("Language Elective", ["Hindi", "Sanskrit", "French"], horizontal=True)
    skill_opt = st.radio("Skill Elective", ["Financial Literacy", "AI", "Computer"], horizontal=True)
    
    if skill_opt == "AI":
        max_skill_marks = 35 if "PT" in exam_phase else 50
    else:
        max_skill_marks = max_marks 
        
    sc_math = st.number_input(f"Mathematics (Max: {max_marks})", 0.0, float(max_marks), float(int(max_marks*0.75)), step=0.5)
    sc_sci = st.number_input(f"Science (Max: {max_marks})", 0.0, float(max_marks), float(int(max_marks*0.70)), step=0.5)
    sc_sst = st.number_input(f"Social Science (Max: {max_marks})", 0.0, float(max_marks), float(int(max_marks*0.70)), step=0.5)
    sc_eng = st.number_input(f"English (Max: {max_marks})", 0.0, float(max_marks), float(int(max_marks*0.80)), step=0.5)
    sc_lang = st.number_input(f"{lang_opt} (Max: {max_marks})", 0.0, float(max_marks), float(int(max_marks*0.85)), step=0.5)
    sc_skill = st.number_input(f"{skill_opt} (Max: {max_skill_marks})", 0.0, float(max_skill_marks), float(int(max_skill_marks*0.90)), step=0.5)
    st.markdown("</div>", unsafe_allow_html=True)

with right_col:
    scores = {
        "Maths": (sc_math/max_marks)*100, "Science": (sc_sci/max_marks)*100, 
        "SST": (sc_sst/max_marks)*100, "English": (sc_eng/max_marks)*100, 
        lang_opt: (sc_lang/max_marks)*100, skill_opt: (sc_skill/max_skill_marks)*100
    }
    avg_score = sum(scores.values()) / len(scores)
    
    # KPI Grid
    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.markdown(f"""
            <div class='glass-panel' style='text-align: center; padding: 15px;'>
                <p style='color: #94a3b8; font-size: 0.75rem; text-transform: uppercase;'>Predicted Average</p>
                <h3 style='color: #818cf8; font-size: 1.8rem; margin: 0;'>{avg_score:.1f}%</h3>
            </div>
        """, unsafe_allow_html=True)
    with kpi2:
        risk_color = "#10b981" if avg_score > 75 and attendance > 75 else "#ef4444"
        risk_text = "LOW RISK 🟢" if avg_score > 75 and attendance > 75 else "HIGH RISK 🔴"
        st.markdown(f"""
            <div class='glass-panel' style='text-align: center; padding: 15px;'>
                <p style='color: #94a3b8; font-size: 0.75rem; text-transform: uppercase;'>Risk Profile</p>
                <h3 style='color: {risk_color}; font-size: 1.2rem; margin-top: 5px;'>{risk_text}</h3>
            </div>
        """, unsafe_allow_html=True)
    with kpi3:
        st.markdown(f"""
            <div class='glass-panel' style='text-align: center; padding: 15px;'>
                <p style='color: #94a3b8; font-size: 0.75rem; text-transform: uppercase;'>Gain Potential</p>
                <h3 style='color: #10b981; font-size: 1.8rem; margin: 0;'>+6.2%</h3>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Roster Preview Section
    st.markdown("#### 📊 Live Master Class Roster Database")
    if not st.session_state.class_portfolio.empty:
        st.dataframe(st.session_state.class_portfolio, use_container_width=True)
    else:
        st.info("💡 Portfolio database is currently empty. Input student parameters on the left and click 'Add Student'.")

    # Action Buttons Bar
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    with btn_col1:
        if st.button("➕ Add Student to Roster", use_container_width=True):
            if not student_name:
                st.error("⚠️ Enter a valid student name.")
            else:
                new_student = pd.DataFrame({
                    "Name": [student_name], "Roll No": [roll_no], "Class": [class_sec], "Parent Phone": [parent_phone], 
                    "Exam": [exam_phase], "Attendance (%)": [attendance], "Assignments (%)": [assignments], "Average (%)": [round(avg_score, 1)]
                })
                st.session_state.class_portfolio = pd.concat([st.session_state.class_portfolio, new_student], ignore_index=True)
                st.rerun()

    with btn_col2:
        if not st.session_state.class_portfolio.empty:
            csv_file = st.session_state.class_portfolio.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Export Master CSV", data=csv_file,
                file_name=f"CBSE_Class_Portfolio_{exam_phase}.csv", mime="text/csv", use_container_width=True
            )
        else:
            st.button("📥 Export Master CSV", disabled=True, use_container_width=True)

    with btn_col3:
        if st.button("🗑️ Reset Database", use_container_width=True):
            st.session_state.class_portfolio = pd.DataFrame(columns=["Name", "Roll No", "Class", "Parent Phone", "Exam", "Attendance (%)", "Assignments (%)", "Average (%)"])
            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    
    # AI Report Generator Button using gemini-3.6-flash
    if st.button("🚀 Run Deep AI Telemetry & Diagnostic Report", use_container_width=True):
        if not student_name:
            st.error("⚠️ Please specify a student name before triggering diagnostics.")
        else:
            with st.spinner("Synthesizing behavioral metrics with Gemini core..."):
                try:
                    prompt = f"""
                    Act as an elite CBSE Class 10 academic coordinator.
                    Student: {student_name} ({class_sec}, Roll: {roll_no}). Phase: {exam_phase}
                    Telemetry: {attendance}% attendance, {assignments}% assignments.
                    Scores (%): Math {scores['Maths']:.1f}, Sci {scores['Science']:.1f}, SST {scores['SST']:.1f}, Eng {scores['English']:.1f}.
                    Provide an executive 4-bullet assessment covering grade trajectory and tactical intervention steps.
                    """
                    resp = client.models.generate_content(model="gemini-3.6-flash", contents=prompt)
                    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
                    st.markdown("#### 📑 Diagnostic Output Matrix")
                    st.write(resp.text)
                    st.markdown("</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"❌ AI Generation Failed: {e}")
