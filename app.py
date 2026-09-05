import streamlit as st
from google import genai
import pandas as pd
from PIL import Image
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import time

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# --- PREMIUM LIGHT/ARCHITECTURAL DESIGN SYSTEM ---
st.set_page_config(page_title="EduPredict AI | NCS Goa", layout="wide", initial_sidebar_state="expanded")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    @keyframes smoothFadeIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Base Theme - Clean Light Mode */
    .stApp { 
        background-color: #FAFAFA; 
        color: #1E293B; 
        font-family: 'Plus Jakarta Sans', sans-serif; 
        animation: smoothFadeIn 0.8s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    /* Inputs & Labels */
    .stTextInput label p, .stNumberInput label p, .stSlider label p, .stRadio label p, .stSelectbox label p {
        color: #64748B !important; font-weight: 600 !important; font-size: 0.75rem !important; text-transform: uppercase; letter-spacing: 0.1em;
    }
    
    .stTextInput input, .stNumberInput input, .stChatInput textarea {
        background-color: #FFFFFF !important; color: #1E293B !important; border: 1px solid #E2E8F0 !important; border-radius: 8px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        transition: all 0.2s ease;
    }
    
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #F28C28 !important; box-shadow: 0 0 0 3px rgba(242, 140, 40, 0.15) !important;
    }
    
    /* Premium Buttons (Matching the warm orange from your reference) */
    .stButton button, .stDownloadButton button {
        background: linear-gradient(135deg, #F28C28 0%, #E87A14 100%) !important;
        color: #ffffff !important; border: none !important; border-radius: 4px !important;
        font-weight: 600 !important; letter-spacing: 0.05em; padding: 0.6rem 1.8rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 14px rgba(242, 140, 40, 0.3);
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(242, 140, 40, 0.4);
    }
    
    /* Clean White Glass/Card Panels */
    .glass-panel { 
        background: #FFFFFF; 
        border: 1px solid #F1F5F9; 
        padding: 32px; border-radius: 16px; 
        box-shadow: 0 10px 40px -10px rgba(0, 0, 0, 0.08);
        animation: smoothFadeIn 0.6s ease-out;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .glass-panel:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.12);
    }

    /* Notice Bar */
    .nav-guide {
        background: #FFFFFF;
        border-left: 4px solid #F28C28;
        padding: 16px 24px;
        border-radius: 8px;
        color: #475569;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        font-size: 0.9rem;
    }
    
    hr { border-color: #E2E8F0; margin: 2rem 0; }
    
    /* Typography Overrides */
    h1, h2, h3, h4, h5, h6 {
        color: #0F172A;
        font-weight: 800;
        letter-spacing: -0.02em;
    }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATES ---
if "app_started" not in st.session_state:
    st.session_state.app_started = False

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Welcome to the NCS Dashboard. How can I assist you with your Standard 10 class today?"}]

if "class_portfolio" not in st.session_state:
    st.session_state.class_portfolio = pd.DataFrame(columns=["Name", "Roll No", "Class", "Parent Phone", "Parent Email", "Exam", "Attendance (%)", "Assignments (%)", "Average (%)"])

if "ext_name" not in st.session_state: st.session_state.ext_name = ""
if "ext_roll" not in st.session_state: st.session_state.ext_roll = ""
if "ext_math" not in st.session_state: st.session_state.ext_math = None
if "ext_sci" not in st.session_state: st.session_state.ext_sci = None
if "ext_sst" not in st.session_state: st.session_state.ext_sst = None
if "ext_eng" not in st.session_state: st.session_state.ext_eng = None
if "raw_extracted" not in st.session_state: st.session_state.raw_extracted = None

# --- ARCHITECTURAL LANDING PAGE (NCS GOA) ---
if not st.session_state.app_started:
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Using a container to create a subtle background box for the whole hero section
    st.markdown("""
        <div style="background-color: #FFF5F0; border-radius: 20px; padding: 40px; margin-bottom: 20px;">
    """, unsafe_allow_html=True)
    
    col_text, col_img = st.columns([1, 1.2])
    
    with col_text:
        st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True) # Vertical spacer
        st.markdown("""
            <div>
                <h1 style="font-size: 5.5rem; font-weight: 800; color: #2A3644; line-height: 1.1; margin-bottom: 20px;">We Build<br>Future</h1>
                <p style="color: #64748B; font-size: 1.1rem; line-height: 1.8; margin-bottom: 35px; max-width: 90%;">
                    In the fast-paced environment of Standard 10th board preparation, seamless data is required. Welcome to EduPredict AI — executing advanced computer vision extraction and diagnostic workflows for Navy Children School, Goa.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        btn_c1, btn_c2 = st.columns([0.6, 0.4])
        with btn_c1:
            if st.button("Explore Now  >", use_container_width=True):
                st.session_state.app_started = True
                st.rerun()
                
    with col_img:
        # The school photo, properly sized with a soft elegant shadow
        ncs_photo_url = "https://drive.scientificstudy.co/preview/eyJQYXRoIjoiV2ViU2l0ZUNvbnRlbnQvTUVESUFDT05URU5ULzMwMTYvMTMwMTYvMjgwNTciLCJOYW1lIjoiTWVkaWFfMjUwNDMwMTMxNDU3NDA4LmpwZyJ9.Lso2JNxIJM5mPFWSMxOxybFbKN1H2sYFGJ%2FONjGlcJo"
        st.markdown(f"""
            <img src="{ncs_photo_url}" 
                 style="width: 100%; height: 600px; object-fit: cover; border-radius: 12px; 
                        box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);">
        """, unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True) # End hero background
    st.stop()

# --- SIDEBAR: AI TEACHER ASSISTANT PANEL ---
with st.sidebar:
    st.markdown("### 💬 Assistant")
    st.caption("Standard 10th Guidance & Workflows.")
    
    chat_container = st.container(height=450)
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if chat_prompt := st.chat_input("Ask a question..."):
        st.session_state.messages.append({"role": "user", "content": chat_prompt})
        with chat_container:
            with st.chat_message("user"):
                st.markdown(chat_prompt)
            with st.chat_message("assistant"):
                try:
                    chat_resp = client.models.generate_content_stream(model="gemini-3.5-flash", contents=chat_prompt)
                    full_text = st.write_stream(chunk.text for chunk in chat_resp)
                    st.session_state.messages.append({"role": "assistant", "content": full_text})
                except Exception as e:
                    st.error(f"Error: {e}")
        st.rerun()

# --- HEADER BAR ---
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.markdown("<h3 style='margin-bottom: 0;'>EduPredict AI</h3><p style='color: #64748B; font-weight: 600; letter-spacing: 1px; font-size: 0.8rem;'>NAVY CHILDREN SCHOOL, GOA • STD 10</p>", unsafe_allow_html=True)
with col_head2:
    exam_phase = st.selectbox("EVALUATION PHASE", ["PT-1", "Half Yearly", "PT-2", "Preboards"])
    max_marks = 40 if "PT" in exam_phase else 80

st.markdown("<hr>", unsafe_allow_html=True)

# Notice Bar
st.markdown("""
    <div class="nav-guide">
        <b>Navigation Notice:</b> Click the <b>></b> arrow in the top-left corner to access the AI Chat Assistant. Upload test sheets below for instant score auto-fill.
    </div>
""", unsafe_allow_html=True)

# --- AI DOCUMENT INGESTION HUB ---
with st.expander("📂 VISION INGESTION & EXTRACTION HUB", expanded=False):
    st.markdown("#### Upload Standard 10 Test Sheet Image")
    uploaded_paper = st.file_uploader("Accepts PNG, JPG, JPEG", type=["png", "jpg", "jpeg"], key="paper_up")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        extract_clicked = st.button("Extract Document", use_container_width=True)
        
    if uploaded_paper and extract_clicked:
        with st.spinner("Analyzing document..."):
            try:
                image_input = Image.open(uploaded_paper)
                prompt_paper = """Analyze this student document image. Extract the Student Name, Roll Number, and scores for Math, Science, SST, and English. 
                You MUST return the data STRICTLY as a valid JSON object (no markdown formatting, no backticks, just the raw JSON) with exactly these keys: 
                {"name": "...", "roll_no": "...", "math": 0.0, "science": 0.0, "sst": 0.0, "english": 0.0}"""
                
                resp_paper = client.models.generate_content(
                    model="gemini-3.5-flash", 
                    contents=[prompt_paper, image_input]
                )
                
                raw_text = resp_paper.text.strip()
                if raw_text.startswith("```json"): 
                    raw_text = raw_text[7:-3]
                elif raw_text.startswith("```"): 
                    raw_text = raw_text[3:-3]
                
                st.session_state.raw_extracted = json.loads(raw_text)
                st.toast('Extraction Complete!', icon='✅')
            except Exception as e:
                st.error(f"Extraction failed: {e}")

    if st.session_state.raw_extracted:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown("#### Extracted Data Matrix", unsafe_allow_html=True)
        
        ext = st.session_state.raw_extracted
        p_name = ext.get("name") or "Not Detected"
        p_roll = ext.get("roll_no") or "N/A"
        p_math = ext.get("math") if ext.get("math") is not None else 0.0
        p_sci = ext.get("science") if ext.get("science") is not None else 0.0
        p_sst = ext.get("sst") if ext.get("sst") is not None else 0.0
        p_eng = ext.get("english") if ext.get("english") is not None else 0.0

        prev_col1, prev_col2, prev_col3 = st.columns(3)
        with prev_col1:
            st.metric("Detected Student", p_name)
            st.metric("Roll Number", p_roll)
        with prev_col2:
            st.metric("Mathematics", p_math)
            st.metric("Science", p_sci)
        with prev_col3:
            st.metric("Social Science", p_sst)
            st.metric("English", p_eng)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Apply to Form", use_container_width=True):
            st.session_state.ext_name = p_name if p_name != "Not Detected" else ""
            st.session_state.ext_roll = p_roll if p_roll != "N/A" else ""
            st.session_state.ext_math = float(p_math)
            st.session_state.ext_sci = float(p_sci)
            st.session_state.ext_sst = float(p_sst)
            st.session_state.ext_eng = float(p_eng)
            
            st.toast("Form updated!", icon="✨")
            time.sleep(0.5)
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# --- BATCH CLASS CSV UPLOAD HUB ---
with st.expander("📊 BATCH DATASET & OUTLIER DETECTION", expanded=False):
    st.markdown("#### Upload Standard 10 CSV Telemetry")
    uploaded_csv = st.file_uploader("Upload Class Dataset", type=["csv"], key="batch_csv_up")
    if uploaded_csv:
        df_batch = pd.read_csv(uploaded_csv)
        st.dataframe(df_batch, use_container_width=True)
        if st.button("Run AI Batch Analysis", use_container_width=True):
            with st.spinner("Processing trends..."):
                try:
                    csv_summary = df_batch.to_string(index=False)
                    batch_prompt = f"""
                    Act as an elite CBSE Class 10 principal and data analyst at Navy Children School Goa. 
                    Analyze this Standard 10 classroom dataset containing student performance and behavioral telemetry:
                    {csv_summary}
                    Provide an executive bulk summary including:
                    1. Overall class performance health and board exam readiness.
                    2. Identification of high-risk or outlier students needing urgent intervention.
                    3. Actionable recommendations for pedagogical adjustments.
                    """
                    batch_resp = client.models.generate_content(model="gemini-3.5-flash", contents=batch_prompt)
                    st.toast("Analysis Complete", icon="📊")
                    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
                    st.markdown("#### Diagnostic Batch Report")
                    st.markdown(batch_resp.text)
                    st.markdown("</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Batch Analysis Failed: {e}")

st.markdown("<hr>", unsafe_allow_html=True)

# --- SPLIT SCREEN LAYOUT ---
left_col, right_col = st.columns([4, 8], gap="large")

with left_col:
    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    st.markdown("<h4 style='font-size: 1.1rem; margin-bottom: 1rem;'>👤 Student Credentials</h4>", unsafe_allow_html=True)
    student_name = st.text_input("Full Name", value=st.session_state.ext_name, placeholder="e.g., Aarav Sharma")
    r_col1, r_col2 = st.columns(2)
    with r_col1:
        roll_no = st.text_input("Roll No.", value=st.session_state.ext_roll, placeholder="04")
    with r_col2:
        class_sec = st.text_input("Class/Sec", value="10-", placeholder="10-A")
    
    p_col1, p_col2 = st.columns(2)
    with p_col1:
        parent_phone = st.text_input("Parent Phone", placeholder="+91 98765 43210")
    with p_col2:
        parent_email = st.text_input("Parent Email", placeholder="parent@example.com")
    st.markdown("</div><br>", unsafe_allow_html=True)

    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    st.markdown("<h4 style='font-size: 1.1rem; margin-bottom: 1rem;'>🏫 Behavioral Telemetry</h4>", unsafe_allow_html=True)
    attendance = st.slider("Attendance Rate (%)", 0, 100, 88)
    assignments = st.slider("Assignment Completion (%)", 0, 100, 92)
    participation = st.slider("Participation Score", 1, 10, 8)
    behavior = st.slider("Conduct Index", 1, 10, 9)
    st.markdown("</div><br>", unsafe_allow_html=True)

    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    st.markdown("<h4 style='font-size: 1.1rem; margin-bottom: 1rem;'>📚 Subject Scores</h4>", unsafe_allow_html=True)
    lang_opt = st.radio("Language Elective", ["Hindi", "Sanskrit", "French"], horizontal=True)
    skill_opt = st.radio("Skill Elective", ["Financial Literacy", "AI", "Computer"], horizontal=True)
    
    if skill_opt == "AI": max_skill_marks = 35 if "PT" in exam_phase else 50
    else: max_skill_marks = max_marks 
    
    raw_math = st.session_state.ext_math if st.session_state.ext_math is not None else float(int(max_marks*0.75))
    val_math = min(float(raw_math), float(max_marks))

    raw_sci = st.session_state.ext_sci if st.session_state.ext_sci is not None else float(int(max_marks*0.70))
    val_sci = min(float(raw_sci), float(max_marks))

    raw_sst = st.session_state.ext_sst if st.session_state.ext_sst is not None else float(int(max_marks*0.70))
    val_sst = min(float(raw_sst), float(max_marks))

    raw_eng = st.session_state.ext_eng if st.session_state.ext_eng is not None else float(int(max_marks*0.80))
    val_eng = min(float(raw_eng), float(max_marks))
        
    sc_math = st.number_input(f"Mathematics (Max: {max_marks})", 0.0, float(max_marks), val_math, step=0.5)
    sc_sci = st.number_input(f"Science (Max: {max_marks})", 0.0, float(max_marks), val_sci, step=0.5)
    sc_sst = st.number_input(f"Social Science (Max: {max_marks})", 0.0, float(max_marks), val_sst, step=0.5)
    sc_eng = st.number_input(f"English (Max: {max_marks})", 0.0, float(max_marks), val_eng, step=0.5)
    sc_lang = st.number_input(f"{lang_opt} (Max: {max_marks})", 0.0, float(max_marks), min(float(int(max_marks*0.85)), float(max_marks)), step=0.5)
    sc_skill = st.number_input(f"{skill_opt} (Max: {max_skill_marks})", 0.0, float(max_skill_marks), min(float(int(max_skill_marks*0.90)), float(max_skill_marks)), step=0.5)
    st.markdown("</div>", unsafe_allow_html=True)

with right_col:
    scores = {
        "Maths": (sc_math/max_marks)*100, "Science": (sc_sci/max_marks)*100, 
        "SST": (sc_sst/max_marks)*100, "English": (sc_eng/max_marks)*100, 
        lang_opt: (sc_lang/max_marks)*100, skill_opt: (sc_skill/max_skill_marks)*100
    }
    avg_score = sum(scores.values()) / len(scores)
    
    headroom = max(0.0, 100.0 - avg_score)
    assignment_gap = max(0.0, 100.0 - assignments)
    gain_potential = round(min(25.0, max(1.2, (headroom * 0.22) + (assignment_gap * 0.08))), 1)

    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.markdown(f"""
            <div class='glass-panel' style='text-align: center; padding: 15px;'>
                <p style='color: #64748B; font-size: 0.75rem; text-transform: uppercase;'>Current Average</p>
                <h3 style='color: #1E293B; font-size: 2rem; margin: 0;'>{avg_score:.1f}%</h3>
            </div>
        """, unsafe_allow_html=True)
    with kpi2:
        risk_color = "#10B981" if avg_score > 75 and attendance > 75 else "#EF4444"
        risk_text = "LOW RISK" if avg_score > 75 and attendance > 75 else "HIGH RISK"
        st.markdown(f"""
            <div class='glass-panel' style='text-align: center; padding: 15px;'>
                <p style='color: #64748B; font-size: 0.75rem; text-transform: uppercase;'>Risk Profile</p>
                <h3 style='color: {risk_color}; font-size: 1.4rem; margin-top: 5px;'>{risk_text}</h3>
            </div>
        """, unsafe_allow_html=True)
    with kpi3:
        st.markdown(f"""
            <div class='glass-panel' style='text-align: center; padding: 15px;'>
                <p style='color: #64748B; font-size: 0.75rem; text-transform: uppercase;'>Gain Potential</p>
                <h3 style='color: #F28C28; font-size: 2rem; margin: 0;'>+{gain_potential}%</h3>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("#### 📈 Performance Distribution")
    chart_data = pd.DataFrame({
        "Subject": list(scores.keys()),
        "Score (%)": list(scores.values())
    })
    st.bar_chart(chart_data, x="Subject", y="Score (%)", color="#1E3A8A", height=250)

    if avg_score < 50:
        st.error("⚠️ ALERT: Student's overall average is below 50%. Immediate intervention required.")
        if st.button("Dispatch Email Alert", use_container_width=True):
            if not parent_email:
                st.warning("Please enter a valid Parent Email Address on the left panel.")
            else:
                with st.spinner("Dispatching alert..."):
                    try:
                        sender_email = st.secrets.get("EMAIL_SENDER", "")
                        sender_password = st.secrets.get("EMAIL_PASSWORD", "")
                        
                        if not sender_email or not sender_password:
                            st.error("❌ Email credentials missing in Streamlit Secrets.")
                        else:
                            msg = MIMEMultipart()
                            msg['From'] = sender_email
                            msg['To'] = parent_email
                            msg['Subject'] = f"NCS Goa Board Academic Alert: {student_name} - {exam_phase}"
                            
                            body = f"""Dear Parent,

This is an automated academic alert from the EduPredict AI system for Navy Children School, Goa (Standard 10).

We are writing to inform you regarding {student_name}'s performance in the recent {exam_phase} evaluations. Currently, their overall average is {avg_score:.1f}%, which requires immediate attention for board preparation.

Subject Breakdown (Percentage):
- Mathematics: {scores['Maths']:.1f}%
- Science: {scores['Science']:.1f}%
- Social Science: {scores['SST']:.1f}%
- English: {scores['English']:.1f}%
- {lang_opt}: {scores[lang_opt]:.1f}%
- {skill_opt}: {scores[skill_opt]:.1f}%

Attendance: {attendance}%

Please contact the school academic coordinator at your earliest convenience to schedule a parent-teacher meeting.

Sincerely,
Navy Children School, Goa
"""
                            msg.attach(MIMEText(body, 'plain'))
                            server = smtplib.SMTP('smtp.gmail.com', 587)
                            server.starttls()
                            server.login(sender_email, sender_password)
                            server.sendmail(sender_email, parent_email, msg.as_string())
                            server.quit()
                            
                            st.success(f"✅ Alert successfully dispatched to {parent_email}")
                    except Exception as e:
                        st.error(f"Failed to send email: {e}")

    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("#### 📊 Live Master Roster")
    if not st.session_state.class_portfolio.empty:
        st.dataframe(st.session_state.class_portfolio, use_container_width=True)
    else:
        st.info("Database is empty. Input parameters on the left and append to roster.")

    btn_col1, btn_col2, btn_col3 = st.columns(3)
    with btn_col1:
        if st.button("Append to Roster", use_container_width=True):
            if not student_name:
                st.error("⚠️ Invalid student name.")
            else:
                new_student = pd.DataFrame({
                    "Name": [student_name], "Roll No": [roll_no], "Class": [class_sec], "Parent Phone": [parent_phone], "Parent Email": [parent_email],
                    "Exam": [exam_phase], "Attendance (%)": [attendance], "Assignments (%)": [assignments], "Average (%)": [round(avg_score, 1)]
                })
                st.session_state.class_portfolio = pd.concat([st.session_state.class_portfolio, new_student], ignore_index=True)
                st.toast(f"Added {student_name} to roster!", icon="📋")
                time.sleep(1)
                st.rerun()

    with btn_col2:
        if not st.session_state.class_portfolio.empty:
            csv_file = st.session_state.class_portfolio.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Export Dataset", data=csv_file,
                file_name=f"NCS_Goa_Std10_{exam_phase}.csv", mime="text/csv", use_container_width=True
            )
        else:
            st.button("Export Dataset", disabled=True, use_container_width=True)

    with btn_col3:
        if st.button("Clear Database", use_container_width=True):
            st.session_state.class_portfolio = pd.DataFrame(columns=["Name", "Roll No", "Class", "Parent Phone", "Parent Email", "Exam", "Attendance (%)", "Assignments (%)", "Average (%)"])
            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    
    action_col1, action_col2 = st.columns(2)
    
    with action_col1:
        if st.button("Generate Diagnostic Report", use_container_width=True):
            if not student_name:
                st.error("⚠️ Specify a student first.")
            else:
                with st.spinner("Generating AI report..."):
                    try:
                        prompt = f"""
                        Act as an elite CBSE Class 10 academic coordinator at Navy Children School, Goa.
                        Student: {student_name} ({class_sec}, Roll: {roll_no}). Phase: {exam_phase}
                        Telemetry: {attendance}% attendance, {assignments}% assignments.
                        Scores (%): Math {scores['Maths']:.1f}, Sci {scores['Science']:.1f}, SST {scores['SST']:.1f}, Eng {scores['English']:.1f}.
                        Provide an executive 4-bullet assessment covering board exam trajectory and tactical intervention steps.
                        """
                        resp = client.models.generate_content(model="gemini-3.5-flash", contents=prompt)
                        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
                        st.markdown("#### Diagnostic Report")
                        st.write(resp.text)
                        st.markdown("</div>", unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Failed: {e}")

    with action_col2:
        if st.button("Generate Meeting Script", use_container_width=True):
            if not student_name:
                st.error("⚠️ Specify a student first.")
            else:
                with st.spinner("Drafting script..."):
                    try:
                        script_prompt = f"""
                        Act as an expert CBSE Class 10 educator at Navy Children School, Goa preparing for a Parent-Teacher Conference.
                        Student: {student_name} ({class_sec}, Roll: {roll_no}). Phase: {exam_phase}
                        Telemetry: Attendance {attendance}%, Assignments {assignments}%.
                        Scores (%): Math {scores['Maths']:.1f}, Science {scores['Science']:.1f}, SST {scores['SST']:.1f}, English {scores['English']:.1f}, {lang_opt} {scores[lang_opt]:.1f}, {skill_opt} {scores[skill_opt]:.1f}.
                        Overall Average: {avg_score:.1f}%
                        
                        Generate a professional, personalized meeting agenda and a conversation script for the teacher to use when sitting down with the parents regarding board preparation. 
                        """
                        script_resp = client.models.generate_content(model="gemini-3.5-flash", contents=script_prompt)
                        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
                        st.markdown("#### Conference Script")
                        st.markdown(script_resp.text)
                        st.markdown("</div>", unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Failed: {e}")
