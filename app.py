import streamlit as st
from google import genai
import pandas as pd
from PIL import Image
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# --- APPLE-INSPIRED DESIGN SYSTEM & FLUID ANIMATIONS ---
st.set_page_config(page_title="EduPredict AI | NCS Goa", layout="wide", initial_sidebar_state="expanded")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    @keyframes appleFadeIn {
        from { opacity: 0; transform: translateY(16px) scale(0.99); }
        to { opacity: 1; transform: translateY(0) scale(1); }
    }
    
    @keyframes appleGlow {
        0% { box-shadow: 0 0 0px rgba(10, 132, 255, 0.1); }
        50% { box-shadow: 0 0 25px rgba(10, 132, 255, 0.35); }
        100% { box-shadow: 0 0 0px rgba(10, 132, 255, 0.1); }
    }

    @keyframes rotateTips {
        0% { opacity: 0; transform: translateY(10px); filter: blur(4px); }
        8% { opacity: 1; transform: translateY(0); filter: blur(0px); }
        18% { opacity: 1; transform: translateY(0); filter: blur(0px); }
        24% { opacity: 0; transform: translateY(-10px); filter: blur(4px); }
        100% { opacity: 0; transform: translateY(-10px); filter: blur(4px); }
    }

    .tip-item {
        position: absolute;
        width: 100%;
        opacity: 0;
        will-change: transform, opacity, filter;
        animation: rotateTips 35s cubic-bezier(0.16, 1, 0.3, 1) infinite;
    }
    
    .tip-item:nth-child(1) { animation-delay: 0s; }
    .tip-item:nth-child(2) { animation-delay: 7s; }
    .tip-item:nth-child(3) { animation-delay: 14s; }
    .tip-item:nth-child(4) { animation-delay: 21s; }
    .tip-item:nth-child(5) { animation-delay: 28s; }

    .tips-container {
        position: relative;
        height: 24px;
        overflow: hidden;
        width: 100%;
        display: flex;
        align-items: center;
    }

    .stApp { 
        background-color: #000000; 
        color: #f5f5f7; 
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Inter", "Helvetica Neue", sans-serif; 
        animation: appleFadeIn 0.7s cubic-bezier(0.16, 1, 0.3, 1); 
    }
    
    .stTextInput label p, .stNumberInput label p, .stSlider label p, .stRadio label p, .stSelectbox label p {
        color: #86868b !important; font-weight: 500 !important; font-size: 0.75rem !important; text-transform: uppercase; letter-spacing: 0.08em;
    }
    
    .stTextInput input, .stNumberInput input, .stChatInput textarea {
        background-color: #1c1c1e !important; color: #f5f5f7 !important; border: 1px solid rgba(255, 255, 255, 0.1) !important; border-radius: 10px !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #0a84ff !important; box-shadow: 0 0 0 4px rgba(10, 132, 255, 0.25);
    }
    
    .stButton button, .stDownloadButton button {
        background: linear-gradient(135deg, #0a84ff 0%, #0062d2) !important;
        color: #ffffff !important; border: none !important; border-radius: 980px !important;
        font-weight: 500 !important; letter-spacing: 0.01em; padding: 0.5rem 1.25rem;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        box-shadow: 0 4px 16px rgba(10, 132, 255, 0.3);
    }
    
    .stButton button:hover {
        transform: scale(1.02);
        animation: appleGlow 1.5s infinite;
    }
    
    .glass-panel { 
        background: rgba(28, 28, 30, 0.65); border: 1px solid rgba(255, 255, 255, 0.08); 
        padding: 28px; border-radius: 20px; backdrop-filter: blur(25px); -webkit-backdrop-filter: blur(25px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        animation: appleFadeIn 0.6s cubic-bezier(0.16, 1, 0.3, 1);
        transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.3s ease;
    }
    
    .glass-panel:hover {
        border-color: rgba(10, 132, 255, 0.3);
    }

    .nav-guide {
        background: linear-gradient(135deg, rgba(28, 28, 30, 0.8), rgba(10, 132, 255, 0.08));
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 14px 22px;
        border-radius: 14px;
        color: #a1a1a6;
        font-size: 0.85rem;
        margin-bottom: 1.5rem;
        backdrop-filter: blur(20px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }

    .welcome-card {
        background: linear-gradient(135deg, rgba(28, 28, 30, 0.85), rgba(10, 132, 255, 0.12));
        border: 1px solid rgba(255, 255, 255, 0.12);
        padding: 50px;
        border-radius: 28px;
        text-align: center;
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.6);
        animation: appleFadeIn 0.8s cubic-bezier(0.16, 1, 0.3, 1);
        backdrop-filter: blur(30px);
    }
    
    hr { border-color: rgba(255, 255, 255, 0.08); margin: 2rem 0; }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATES ---
if "app_started" not in st.session_state:
    st.session_state.app_started = False

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello Teacher! I am your Apple-styled AI assistant. How can I help optimize your Standard 10 classroom today?"}]

if "class_portfolio" not in st.session_state:
    st.session_state.class_portfolio = pd.DataFrame(columns=["Name", "Roll No", "Class", "Parent Phone", "Parent Email", "Exam", "Attendance (%)", "Assignments (%)", "Average (%)"])

# Extracted Data States
if "ext_name" not in st.session_state: st.session_state.ext_name = ""
if "ext_roll" not in st.session_state: st.session_state.ext_roll = ""
if "ext_math" not in st.session_state: st.session_state.ext_math = None
if "ext_sci" not in st.session_state: st.session_state.ext_sci = None
if "ext_sst" not in st.session_state: st.session_state.ext_sst = None
if "ext_eng" not in st.session_state: st.session_state.ext_eng = None
if "raw_extracted" not in st.session_state: st.session_state.raw_extracted = None

# --- APPLE-STYLE WELCOME / LANDING PAGE ---
if not st.session_state.app_started:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_w1, col_w2, col_w3 = st.columns([1, 2.6, 1])
    with col_w2:
        st.markdown("""
            <div class="welcome-card">
                <div style="font-size: 3rem; margin-bottom: 12px;"></div>
                <h4 style="color: #0a84ff; text-transform: uppercase; letter-spacing: 0.2em; font-size: 0.75rem; margin-bottom: 6px;">Navy Children School, Goa</h4>
                <h1 style="color: #f5f5f7; font-size: 2.8rem; font-weight: 700; letter-spacing: -0.015em; margin-bottom: 12px;">EduPredict AI</h1>
                <p style="color: #86868b; font-size: 1.1rem; margin-bottom: 25px;">Pro-Grade Classroom Intelligence & Predictive Analytics<br><b style='color: #0a84ff;'>Standard 10th Exclusive Edition</b></p>
                <hr style="margin: 1.5rem 0;">
                <p style="color: #a1a1a6; font-size: 0.9rem; line-height: 1.6; margin-bottom: 30px;">
                    Designed with precision for educators. Featuring computer vision extraction, fluid predictive modeling, and seamless parent communication workflows.
                </p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Launch Standard 10th Intelligence Hub", use_container_width=True):
            st.session_state.app_started = True
            st.rerun()
    st.stop()

# --- SIDEBAR: AI TEACHER ASSISTANT PANEL ---
with st.sidebar:
    st.markdown("### 💬 AI Teacher Assistant")
    st.caption("Standard 10th Guidance & Workflows.")
    
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
                    chat_resp = client.models.generate_content_stream(model="gemini-3.5-flash", contents=chat_prompt)
                    full_text = st.write_stream(chunk.text for chunk in chat_resp)
                    st.session_state.messages.append({"role": "assistant", "content": full_text})
                except Exception as e:
                    st.error(f"Chat Error: {e}")
        st.rerun()

# --- HEADER BAR ---
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.markdown("### EduPredict AI <span style='color:#0a84ff; font-size: 0.9rem; font-weight: 400;'>// NCS Goa · Standard 10</span>", unsafe_allow_html=True)
with col_head2:
    exam_phase = st.selectbox("Active Evaluation Phase", ["PT-1", "Half Yearly", "PT-2", "Preboards"])
    max_marks = 40 if "PT" in exam_phase else 80

st.markdown("<hr style='margin: 1rem 0;'>", unsafe_allow_html=True)

# Unified Single Box with Smooth Blur-Fade Rotating Navigation & Pro Tips Ticker
st.markdown("""
    <div class="nav-guide">
        <div class="tips-container">
            <div class="tip-item">🧭 <b>Navigation Notice:</b> Click the <b>>></b> arrow in the top-left corner to access the hidden AI Teacher Assistant chat.</div>
            <div class="tip-item">⚡ <b>Pro Tip:</b> Upload clear Standard 10 test sheets into the Extraction Hub for instant score and roll number auto-fill.</div>
            <div class="tip-item">🛡️ <b>Pro Tip:</b> Keep an eye on the Risk Profile badge to instantly spot students needing urgent board exam intervention.</div>
            <div class="tip-item">📊 <b>Pro Tip:</b> Use the Batch Class CSV Upload to analyze entire Standard 10 classroom datasets and identify outliers in seconds.</div>
            <div class="tip-item">🎙️ <b>Pro Tip:</b> Generate professional, customized Parent-Teacher Conference scripts for board readiness with a single click.</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- AI DOCUMENT INGESTION HUB ---
with st.expander("📂 AI Document Ingestion & Score Extraction Hub", expanded=False):
    st.markdown("#### 📄 Upload Standard 10 Student Paper / Test Sheet for Extraction")
    uploaded_paper = st.file_uploader("Upload exam paper or answer sheet (Image)", type=["png", "jpg", "jpeg"], key="paper_up")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        extract_clicked = st.button("🔍 Extract & Inspect Details", use_container_width=True)
        
    if uploaded_paper and extract_clicked:
        with st.spinner("Analyzing document with Gemini core..."):
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
                if raw_text.startswith("```json"): raw_text = raw_text[7:-3]
                elif raw_text.startswith("```"): raw_text = raw_text[3:-3]
                
                st.session_state.raw_extracted = json.loads(raw_text)
                st.success("✅ Extraction Complete! View clean preview below.")
            except Exception as e:
                st.error(f"Extraction or Parsing failed: {e}")

    if st.session_state.raw_extracted:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown("#### 📋 Extracted Document Preview Matrix", unsafe_allow_html=True)
        
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
        if st.button("✨ Apply Extracted Data to Form (Auto-Fill)", use_container_width=True):
            st.session_state.ext_name = p_name if p_name != "Not Detected" else ""
            st.session_state.ext_roll = p_roll if p_roll != "N/A" else ""
            st.session_state.ext_math = float(p_math)
            st.session_state.ext_sci = float(p_sci)
            st.session_state.ext_sst = float(p_sst)
            st.session_state.ext_eng = float(p_eng)
            
            st.success("✅ Form successfully auto-filled with extracted data!")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# --- BATCH CLASS CSV UPLOAD HUB ---
with st.expander("📊 Batch Class CSV Upload & AI Classroom Analytics", expanded=False):
    st.markdown("#### Upload Standard 10 Class Dataset for Bulk AI Insights & Outlier Detection")
    uploaded_csv = st.file_uploader("Upload Class Dataset (CSV format)", type=["csv"], key="batch_csv_up")
    if uploaded_csv:
        df_batch = pd.read_csv(uploaded_csv)
        st.dataframe(df_batch, use_container_width=True)
        if st.button("🚀 Run AI Bulk Class Analysis", use_container_width=True):
            with st.spinner("Analyzing bulk telemetry and identifying classroom outliers with Gemini..."):
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
                    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
                    st.markdown("#### 📑 Bulk Classroom Intelligence Report")
                    st.markdown(batch_resp.text)
                    st.markdown("</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Bulk Analysis Failed: {e}")

st.markdown("<hr style='margin: 1rem 0;'>", unsafe_allow_html=True)

# --- SPLIT SCREEN LAYOUT ---
left_col, right_col = st.columns([4, 8], gap="large")

with left_col:
    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#f5f5f7; font-size: 1rem; margin-bottom: 1rem;'>👤 Standard 10 Student Credentials</h4>", unsafe_allow_html=True)
    student_name = st.text_input("Full Name", value=st.session_state.ext_name, placeholder="e.g., Aarav Sharma")
    r_col1, r_col2 = st.columns(2)
    with r_col1:
        roll_no = st.text_input("Roll No.", value=st.session_state.ext_roll, placeholder="04")
    with r_col2:
        class_sec = st.text_input("Class/Sec", value="10-", placeholder="10-A")
    
    p_col1, p_col2 = st.columns(2)
    with p_col1:
        parent_phone = st.text_input("Parent Phone Number", placeholder="+91 98765 43210")
    with p_col2:
        parent_email = st.text_input("Parent Email Address", placeholder="parent@example.com")
    st.markdown("</div><br>", unsafe_allow_html=True)

    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#f5f5f7; font-size: 1rem; margin-bottom: 1rem;'>🏫 Behavioral Telemetry</h4>", unsafe_allow_html=True)
    attendance = st.slider("Attendance Rate (%)", 0, 100, 88)
    assignments = st.slider("Assignment Completion (%)", 0, 100, 92)
    participation = st.slider("Class Participation Score", 1, 10, 8)
    behavior = st.slider("Classroom Conduct Index", 1, 10, 9)
    st.markdown("</div><br>", unsafe_allow_html=True)

    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#f5f5f7; font-size: 1rem; margin-bottom: 1rem;'>📚 Subject Score Matrix</h4>", unsafe_allow_html=True)
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
    
    # CALCULATED GAIN POTENTIAL FORMULA
    headroom = max(0.0, 100.0 - avg_score)
    assignment_gap = max(0.0, 100.0 - assignments)
    gain_potential = round(min(25.0, max(1.2, (headroom * 0.22) + (assignment_gap * 0.08))), 1)

    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.markdown(f"""
            <div class='glass-panel' style='text-align: center; padding: 15px;'>
                <p style='color: #86868b; font-size: 0.75rem; text-transform: uppercase;'>AVG</p>
                <h3 style='color: #0a84ff; font-size: 1.8rem; margin: 0;'>{avg_score:.1f}%</h3>
            </div>
        """, unsafe_allow_html=True)
    with kpi2:
        risk_color = "#30d158" if avg_score > 75 and attendance > 75 else "#ff453a"
        risk_text = "LOW RISK 🟢" if avg_score > 75 and attendance > 75 else "HIGH RISK 🔴"
        st.markdown(f"""
            <div class='glass-panel' style='text-align: center; padding: 15px;'>
                <p style='color: #86868b; font-size: 0.75rem; text-transform: uppercase;'>Risk Profile</p>
                <h3 style='color: {risk_color}; font-size: 1.2rem; margin-top: 5px;'>{risk_text}</h3>
            </div>
        """, unsafe_allow_html=True)
    with kpi3:
        st.markdown(f"""
            <div class='glass-panel' style='text-align: center; padding: 15px;'>
                <p style='color: #86868b; font-size: 0.75rem; text-transform: uppercase;'>Gain Potential</p>
                <h3 style='color: #30d158; font-size: 1.8rem; margin: 0;'>+{gain_potential}%</h3>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("#### 📈 Subject Performance Breakdown")
    chart_data = pd.DataFrame({
        "Subject": list(scores.keys()),
        "Score (%)": list(scores.values())
    })
    st.bar_chart(chart_data, x="Subject", y="Score (%)", color="#0a84ff", height=250)

    if avg_score < 50:
        st.error("⚠️ Critical Alert: Student's overall average is below 50%. Immediate board intervention required.")
        if st.button("📧 Dispatch Automated Email Alert to Parent", use_container_width=True):
            if not parent_email:
                st.warning("Please enter a valid Parent Email Address on the left panel.")
            else:
                with st.spinner("Dispatching secure email alert..."):
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
EduPredict AI Automated System
Navy Children School, Goa
"""
                            msg.attach(MIMEText(body, 'plain'))
                            
                            server = smtplib.SMTP('smtp.gmail.com', 587)
                            server.starttls()
                            server.login(sender_email, sender_password)
                            text = msg.as_string()
                            server.sendmail(sender_email, parent_email, text)
                            server.quit()
                            
                            st.success(f"✅ Alert successfully dispatched to {parent_email}")
                    except Exception as e:
                        st.error(f"Failed to send email: {e}")

    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("#### 📊 Live Master Class Roster Database (Standard 10)")
    if not st.session_state.class_portfolio.empty:
        st.dataframe(st.session_state.class_portfolio, use_container_width=True)
    else:
        st.info("💡 Portfolio database is currently empty. Input student parameters on the left and click 'Add Student'.")

    btn_col1, btn_col2, btn_col3 = st.columns(3)
    with btn_col1:
        if st.button("➕ Add Student to Roster", use_container_width=True):
            if not student_name:
                st.error("⚠️ Enter a valid student name.")
            else:
                new_student = pd.DataFrame({
                    "Name": [student_name], "Roll No": [roll_no], "Class": [class_sec], "Parent Phone": [parent_phone], "Parent Email": [parent_email],
                    "Exam": [exam_phase], "Attendance (%)": [attendance], "Assignments (%)": [assignments], "Average (%)": [round(avg_score, 1)]
                })
                st.session_state.class_portfolio = pd.concat([st.session_state.class_portfolio, new_student], ignore_index=True)
                st.rerun()

    with btn_col2:
        if not st.session_state.class_portfolio.empty:
            csv_file = st.session_state.class_portfolio.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Export Master CSV", data=csv_file,
                file_name=f"NCS_Goa_Std10_Portfolio_{exam_phase}.csv", mime="text/csv", use_container_width=True
            )
        else:
            st.button("📥 Export Master CSV", disabled=True, use_container_width=True)

    with btn_col3:
        if st.button("🗑️ Reset Database", use_container_width=True):
            st.session_state.class_portfolio = pd.DataFrame(columns=["Name", "Roll No", "Class", "Parent Phone", "Parent Email", "Exam", "Attendance (%)", "Assignments (%)", "Average (%)"])
            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    
    action_col1, action_col2 = st.columns(2)
    
    with action_col1:
        if st.button("🚀 Run Deep AI Telemetry & Diagnostic Report", use_container_width=True):
            if not student_name:
                st.error("⚠️ Please specify a student name before triggering diagnostics.")
            else:
                with st.spinner("Synthesizing behavioral metrics with Gemini core..."):
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
                        st.markdown("#### 📑 Standard 10 Board Diagnostic Output Matrix")
                        st.write(resp.text)
                        st.markdown("</div>", unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"❌ AI Generation Failed: {e}")

    with action_col2:
        if st.button("🎙️ Generate Parent-Teacher Conference Script", use_container_width=True):
            if not student_name:
                st.error("⚠️ Please specify a student name before generating conference scripts.")
            else:
                with st.spinner("Drafting personalized meeting agenda and conversation script with Gemini..."):
                    try:
                        script_prompt = f"""
                        Act as an expert CBSE Class 10 educator at Navy Children School, Goa preparing for a Parent-Teacher Conference.
                        Student: {student_name} ({class_sec}, Roll: {roll_no}). Phase: {exam_phase}
                        Telemetry: Attendance {attendance}%, Assignments {assignments}%.
                        Scores (%): Math {scores['Maths']:.1f}, Science {scores['Science']:.1f}, SST {scores['SST']:.1f}, English {scores['English']:.1f}, {lang_opt} {scores[lang_opt]:.1f}, {skill_opt} {scores[skill_opt]:.1f}.
                        Overall Average: {avg_score:.1f}%
                        
                        Generate a professional, personalized meeting agenda and a conversation script for the teacher to use when sitting down with the parents regarding board preparation. 
                        Highlight:
                        1. Meeting Agenda Structure
                        2. Key Student Strengths
                        3. Specific Areas for Improvement
                        4. Step-by-Step Conversation Script & Talking Points
                        """
                        script_resp = client.models.generate_content(model="gemini-3.5-flash", contents=script_prompt)
                        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
                        st.markdown("#### 🎙️ NCS Goa - Parent-Teacher Conference Script & Agenda")
                        st.markdown(script_resp.text)
                        st.markdown("</div>", unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"❌ Script Generation Failed: {e}")
