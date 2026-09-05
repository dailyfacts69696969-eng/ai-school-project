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

# --- LINEAR.APP DESIGN SYSTEM ---
st.set_page_config(page_title="EduPredict AI | NCS Goa", layout="wide", initial_sidebar_state="expanded")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    @keyframes linearFade {
        from { opacity: 0; transform: translateY(4px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Base Theme - Linear Dark */
    .stApp { 
        background-color: #08080A; 
        color: #F4F5F8; 
        font-family: 'Inter', -apple-system, sans-serif; 
        animation: linearFade 0.4s ease-out;
        /* Signature Linear Top Glow */
        background-image: radial-gradient(circle at 50% -20%, rgba(94, 106, 210, 0.15), rgba(8, 8, 10, 1) 50%);
        background-repeat: no-repeat;
    }
    
    /* Typography & Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #F4F5F8 !important;
        font-weight: 600 !important;
        letter-spacing: -0.02em !important;
    }

    /* Inputs & Labels */
    .stTextInput label p, .stNumberInput label p, .stSlider label p, .stRadio label p, .stSelectbox label p {
        color: #8A8F98 !important; font-weight: 500 !important; font-size: 0.8rem !important; margin-bottom: 4px;
    }
    
    .stTextInput input, .stNumberInput input, .stChatInput textarea {
        background-color: #121315 !important; color: #ECECF1 !important; border: 1px solid #27282B !important; border-radius: 6px !important;
        font-size: 0.9rem !important;
        transition: all 0.15s ease;
        box-shadow: 0 1px 2px rgba(0,0,0,0.2);
    }
    
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #5E6AD2 !important; box-shadow: 0 0 0 1px #5E6AD2 !important;
    }
    
    /* Linear Style Buttons */
    .stButton button, .stDownloadButton button {
        background-color: #ECECF1 !important;
        color: #08080A !important; 
        border: 1px solid #ECECF1 !important; 
        border-radius: 6px !important;
        font-weight: 500 !important; font-size: 0.9rem !important; padding: 0.4rem 1rem;
        transition: all 0.15s ease;
        box-shadow: 0 1px 3px rgba(0,0,0,0.3);
    }
    
    .stButton button:hover {
        background-color: #FFFFFF !important;
        transform: translateY(-1px);
    }

    /* Primary Actions Override (Indigo) */
    div[data-testid="stButton"] button:contains("Launch"),
    div[data-testid="stButton"] button:contains("Run"),
    div[data-testid="stButton"] button:contains("Extract"),
    div[data-testid="stButton"] button:contains("Generate"),
    div[data-testid="stButton"] button:contains("Dispatch") {
        background-color: #5E6AD2 !important;
        border-color: #5E6AD2 !important;
        color: #FFFFFF !important;
    }
    
    div[data-testid="stButton"] button:contains("Launch"):hover,
    div[data-testid="stButton"] button:contains("Run"):hover {
        background-color: #6C79DF !important;
        border-color: #6C79DF !important;
    }
    
    /* Clean Solid Panels (No heavy glass) */
    .linear-panel { 
        background: #111216; 
        border: 1px solid #222326; 
        padding: 24px; border-radius: 8px; 
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        animation: linearFade 0.4s ease-out;
        transition: border-color 0.15s ease;
    }
    
    .linear-panel:hover {
        border-color: #313338;
    }

    /* Command Menu Bar Style */
    .nav-guide {
        background: #111216;
        border: 1px solid #222326;
        padding: 12px 16px;
        border-radius: 6px;
        color: #8A8F98;
        font-size: 0.85rem;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    /* Landing Page Modal */
    .welcome-card {
        background: #111216;
        border: 1px solid #27282B;
        padding: 40px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        animation: linearFade 0.5s ease-out;
    }
    
    hr { border-color: #222326; margin: 2rem 0; }
    
    /* Metrics */
    div[data-testid="stMetricValue"] {
        color: #F4F5F8 !important;
        font-weight: 600 !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #8A8F98 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATES ---
if "app_started" not in st.session_state:
    st.session_state.app_started = False

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "EduPredict AI initialized. Ready for Standard 10 workflow."}]

if "class_portfolio" not in st.session_state:
    st.session_state.class_portfolio = pd.DataFrame(columns=["Name", "Roll No", "Class", "Parent Phone", "Parent Email", "Exam", "Attendance (%)", "Assignments (%)", "Average (%)"])

if "ext_name" not in st.session_state: st.session_state.ext_name = ""
if "ext_roll" not in st.session_state: st.session_state.ext_roll = ""
if "ext_math" not in st.session_state: st.session_state.ext_math = None
if "ext_sci" not in st.session_state: st.session_state.ext_sci = None
if "ext_sst" not in st.session_state: st.session_state.ext_sst = None
if "ext_eng" not in st.session_state: st.session_state.ext_eng = None
if "raw_extracted" not in st.session_state: st.session_state.raw_extracted = None

# --- LINEAR WELCOME / LANDING PAGE ---
if not st.session_state.app_started:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col_w1, col_w2, col_w3 = st.columns([1, 2, 1])
    with col_w2:
        st.markdown("""
            <div class="welcome-card">
                <div style="font-size: 2rem; margin-bottom: 16px; color: #5E6AD2;">⌘</div>
                <h4 style="color: #8A8F98; font-weight: 500; font-size: 0.85rem; margin-bottom: 8px;">Navy Children School, Goa</h4>
                <h1 style="color: #F4F5F8; font-size: 2.2rem; font-weight: 600; margin-bottom: 12px; letter-spacing: -0.03em;">EduPredict AI</h1>
                <p style="color: #8A8F98; font-size: 1rem; margin-bottom: 25px;">Standard 10 Workflow & Intelligence Platform</p>
                <hr style="margin: 1.5rem 0; border-color: #222326;">
                <p style="color: #6C7079; font-size: 0.9rem; line-height: 1.5; margin-bottom: 30px;">
                    Streamline classroom operations. Execute vision extraction, risk profiling, and diagnostic reporting with uncompromising speed.
                </p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Launch Workspace", use_container_width=True):
            st.session_state.app_started = True
            st.rerun()
    st.stop()

# --- SIDEBAR: AI ASSISTANT ---
with st.sidebar:
    st.markdown("<h3 style='font-size: 1rem; margin-bottom: 1rem;'>AI Assistant</h3>", unsafe_allow_html=True)
    
    chat_container = st.container(height=500)
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
col_head1, col_head2 = st.columns([4, 1])
with col_head1:
    st.markdown("<h3 style='font-size: 1.2rem; margin-bottom: 0;'>EduPredict AI <span style='color: #5E6AD2; font-weight: 500; font-size: 0.9rem; margin-left: 8px;'>NCS Goa • Std 10</span></h3>", unsafe_allow_html=True)
with col_head2:
    exam_phase = st.selectbox("Cycle", ["PT-1", "Half Yearly", "PT-2", "Preboards"], label_visibility="collapsed")
    max_marks = 40 if "PT" in exam_phase else 80

st.markdown("<hr style='margin: 1rem 0;'>", unsafe_allow_html=True)

# Command Menu / Instruction Bar
st.markdown("""
    <div class="nav-guide">
        <span style="color: #F4F5F8; border: 1px solid #27282B; padding: 2px 6px; border-radius: 4px; font-size: 0.75rem;">Tip</span>
        <span>Open the sidebar (top left) for the AI Assistant. Upload documents below to auto-fill metrics.</span>
    </div>
""", unsafe_allow_html=True)

# --- AI DOCUMENT INGESTION HUB ---
with st.expander("Document Vision Extraction", expanded=False):
    uploaded_paper = st.file_uploader("Upload test sheet (PNG, JPG)", type=["png", "jpg", "jpeg"], key="paper_up")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        extract_clicked = st.button("Run Extraction", use_container_width=True)
        
    if uploaded_paper and extract_clicked:
        with st.spinner("Processing image..."):
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
                st.toast('Extraction Complete', icon='✅')
            except Exception as e:
                st.error(f"Extraction failed: {e}")

    if st.session_state.raw_extracted:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='linear-panel'>", unsafe_allow_html=True)
        st.markdown("<h4 style='font-size: 1rem; margin-bottom: 1rem;'>Parsed Data</h4>", unsafe_allow_html=True)
        
        ext = st.session_state.raw_extracted
        p_name = ext.get("name") or "Not Detected"
        p_roll = ext.get("roll_no") or "N/A"
        p_math = ext.get("math") if ext.get("math") is not None else 0.0
        p_sci = ext.get("science") if ext.get("science") is not None else 0.0
        p_sst = ext.get("sst") if ext.get("sst") is not None else 0.0
        p_eng = ext.get("english") if ext.get("english") is not None else 0.0

        prev_col1, prev_col2, prev_col3 = st.columns(3)
        with prev_col1:
            st.metric("Student", p_name)
            st.metric("Roll No", p_roll)
        with prev_col2:
            st.metric("Mathematics", p_math)
            st.metric("Science", p_sci)
        with prev_col3:
            st.metric("Social Science", p_sst)
            st.metric("English", p_eng)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Apply to Editor", use_container_width=True):
            st.session_state.ext_name = p_name if p_name != "Not Detected" else ""
            st.session_state.ext_roll = p_roll if p_roll != "N/A" else ""
            st.session_state.ext_math = float(p_math)
            st.session_state.ext_sci = float(p_sci)
            st.session_state.ext_sst = float(p_sst)
            st.session_state.ext_eng = float(p_eng)
            
            st.toast("Form updated", icon="✓")
            time.sleep(0.3)
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# --- BATCH CLASS CSV UPLOAD HUB ---
with st.expander("Batch Dataset Analytics", expanded=False):
    uploaded_csv = st.file_uploader("Upload CSV Dataset", type=["csv"], key="batch_csv_up")
    if uploaded_csv:
        df_batch = pd.read_csv(uploaded_csv)
        st.dataframe(df_batch, use_container_width=True)
        if st.button("Generate Batch Analysis", use_container_width=True):
            with st.spinner("Analyzing dataset..."):
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
                    st.toast("Analysis Generated", icon="✓")
                    st.markdown("<div class='linear-panel'>", unsafe_allow_html=True)
                    st.markdown("<h4 style='font-size: 1rem;'>Batch Report</h4>", unsafe_allow_html=True)
                    st.markdown(batch_resp.text)
                    st.markdown("</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Analysis Failed: {e}")

st.markdown("<hr style='margin: 1rem 0;'>", unsafe_allow_html=True)

# --- SPLIT SCREEN LAYOUT ---
left_col, right_col = st.columns([4, 8], gap="large")

with left_col:
    st.markdown("<div class='linear-panel'>", unsafe_allow_html=True)
    st.markdown("<h4 style='font-size: 1rem; margin-bottom: 1rem;'>Identity</h4>", unsafe_allow_html=True)
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
        parent_email = st.text_input("Parent Email", placeholder="email@example.com")
    st.markdown("</div><br>", unsafe_allow_html=True)

    st.markdown("<div class='linear-panel'>", unsafe_allow_html=True)
    st.markdown("<h4 style='font-size: 1rem; margin-bottom: 1rem;'>Telemetry</h4>", unsafe_allow_html=True)
    attendance = st.slider("Attendance (%)", 0, 100, 88)
    assignments = st.slider("Assignments (%)", 0, 100, 92)
    participation = st.slider("Participation", 1, 10, 8)
    behavior = st.slider("Conduct", 1, 10, 9)
    st.markdown("</div><br>", unsafe_allow_html=True)

    st.markdown("<div class='linear-panel'>", unsafe_allow_html=True)
    st.markdown("<h4 style='font-size: 1rem; margin-bottom: 1rem;'>Subject Matrix</h4>", unsafe_allow_html=True)
    lang_opt = st.radio("Language", ["Hindi", "Sanskrit", "French"], horizontal=True)
    skill_opt = st.radio("Skill", ["Financial Literacy", "AI", "Computer"], horizontal=True)
    
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
        
    sc_math = st.number_input(f"Math (Max: {max_marks})", 0.0, float(max_marks), val_math, step=0.5)
    sc_sci = st.number_input(f"Science (Max: {max_marks})", 0.0, float(max_marks), val_sci, step=0.5)
    sc_sst = st.number_input(f"SST (Max: {max_marks})", 0.0, float(max_marks), val_sst, step=0.5)
    sc_eng = st.number_input(f"English (Max: {max_marks})", 0.0, float(max_marks), val_eng, step=0.5)
    sc_lang = st.number_input(f"{lang_opt} (Max: {max_marks})", 0.0, float(max_marks), min(float(int(max_marks*0.85)), float(max_marks)), step=0.5)
    sc_skill = st.number_input(f"{skill_opt} (Max: {max_skill_marks})", 0.0, float(max_skill_marks), min(float(int(max_skill_marks*0.90)), float(max_skill_marks)), step=0.5)
    st.markdown("</div>", unsafe_allow_html=True)

with right_col:
    scores = {
        "Math": (sc_math/max_marks)*100, "Science": (sc_sci/max_marks)*100, 
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
            <div class='linear-panel' style='padding: 20px;'>
                <p style='color: #8A8F98; font-size: 0.75rem; text-transform: uppercase; margin-bottom: 4px;'>Average</p>
                <h3 style='color: #F4F5F8; font-size: 1.8rem; margin: 0;'>{avg_score:.1f}%</h3>
            </div>
        """, unsafe_allow_html=True)
    with kpi2:
        risk_color = "#5E6AD2" if avg_score > 75 and attendance > 75 else "#E26F6F"
        risk_text = "Nominal" if avg_score > 75 and attendance > 75 else "At Risk"
        st.markdown(f"""
            <div class='linear-panel' style='padding: 20px;'>
                <p style='color: #8A8F98; font-size: 0.75rem; text-transform: uppercase; margin-bottom: 4px;'>Status</p>
                <h3 style='color: {risk_color}; font-size: 1.2rem; margin: 0; padding-top: 6px;'>{risk_text}</h3>
            </div>
        """, unsafe_allow_html=True)
    with kpi3:
        st.markdown(f"""
            <div class='linear-panel' style='padding: 20px;'>
                <p style='color: #8A8F98; font-size: 0.75rem; text-transform: uppercase; margin-bottom: 4px;'>Gain Pot.</p>
                <h3 style='color: #F4F5F8; font-size: 1.8rem; margin: 0;'>+{gain_potential}%</h3>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<h4 style='font-size: 1rem;'>Distribution</h4>", unsafe_allow_html=True)
    chart_data = pd.DataFrame({
        "Subject": list(scores.keys()),
        "Score (%)": list(scores.values())
    })
    st.bar_chart(chart_data, x="Subject", y="Score (%)", color="#5E6AD2", height=200)

    if avg_score < 50:
        st.error("Status Critical: Student average below 50%.")
        if st.button("Dispatch Parent Alert", use_container_width=True):
            if not parent_email:
                st.warning("Parent email required.")
            else:
                with st.spinner("Dispatching..."):
                    try:
                        sender_email = st.secrets.get("EMAIL_SENDER", "")
                        sender_password = st.secrets.get("EMAIL_PASSWORD", "")
                        
                        if not sender_email or not sender_password:
                            st.error("Credentials missing in Secrets.")
                        else:
                            msg = MIMEMultipart()
                            msg['From'] = sender_email
                            msg['To'] = parent_email
                            msg['Subject'] = f"NCS Goa Alert: {student_name} - {exam_phase}"
                            
                            body = f"Alert for {student_name}.\nAverage: {avg_score:.1f}%.\nPlease contact the school."
                            msg.attach(MIMEText(body, 'plain'))
                            
                            server = smtplib.SMTP('smtp.gmail.com', 587)
                            server.starttls()
                            server.login(sender_email, sender_password)
                            server.sendmail(sender_email, parent_email, msg.as_string())
                            server.quit()
                            
                            st.toast("Dispatched", icon="✓")
                            st.success(f"Alert sent to {parent_email}")
                    except Exception as e:
                        st.error(f"Failed: {e}")

    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("<h4 style='font-size: 1rem;'>Class Roster</h4>", unsafe_allow_html=True)
    if not st.session_state.class_portfolio.empty:
        st.dataframe(st.session_state.class_portfolio, use_container_width=True)
    else:
        st.info("Roster empty. Submit student data to populate.")

    btn_col1, btn_col2, btn_col3 = st.columns(3)
    with btn_col1:
        if st.button("Add to Roster", use_container_width=True):
            if not student_name:
                st.error("Name required.")
            else:
                new_student = pd.DataFrame({
                    "Name": [student_name], "Roll No": [roll_no], "Class": [class_sec], "Parent Phone": [parent_phone], "Parent Email": [parent_email],
                    "Exam": [exam_phase], "Attendance (%)": [attendance], "Assignments (%)": [assignments], "Average (%)": [round(avg_score, 1)]
                })
                st.session_state.class_portfolio = pd.concat([st.session_state.class_portfolio, new_student], ignore_index=True)
                st.toast("Saved", icon="✓")
                time.sleep(0.3)
                st.rerun()

    with btn_col2:
        if not st.session_state.class_portfolio.empty:
            csv_file = st.session_state.class_portfolio.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Export CSV", data=csv_file,
                file_name=f"Roster_{exam_phase}.csv", mime="text/csv", use_container_width=True
            )
        else:
            st.button("Export CSV", disabled=True, use_container_width=True)

    with btn_col3:
        if st.button("Clear Data", use_container_width=True):
            st.session_state.class_portfolio = pd.DataFrame(columns=["Name", "Roll No", "Class", "Parent Phone", "Parent Email", "Exam", "Attendance (%)", "Assignments (%)", "Average (%)"])
            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    
    action_col1, action_col2 = st.columns(2)
    
    with action_col1:
        if st.button("Generate Diagnostic Report", use_container_width=True):
            if not student_name:
                st.error("Student required.")
            else:
                with st.spinner("Generating..."):
                    try:
                        prompt = f"""Act as a CBSE Class 10 coordinator. Student: {student_name}, Avg: {avg_score:.1f}%. Provide a 4-bullet executive summary on board readiness."""
                        resp = client.models.generate_content(model="gemini-3.5-flash", contents=prompt)
                        st.markdown("<div class='linear-panel'>", unsafe_allow_html=True)
                        st.markdown("<h4 style='font-size: 1rem;'>Diagnostic Report</h4>", unsafe_allow_html=True)
                        st.write(resp.text)
                        st.markdown("</div>", unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Failed: {e}")

    with action_col2:
        if st.button("Generate Meeting Script", use_container_width=True):
            if not student_name:
                st.error("Student required.")
            else:
                with st.spinner("Drafting..."):
                    try:
                        script_prompt = f"""Draft a professional Parent-Teacher meeting script for {student_name}, Avg {avg_score:.1f}%. Include agenda and talking points."""
                        script_resp = client.models.generate_content(model="gemini-3.5-flash", contents=script_prompt)
                        st.markdown("<div class='linear-panel'>", unsafe_allow_html=True)
                        st.markdown("<h4 style='font-size: 1rem;'>Meeting Script</h4>", unsafe_allow_html=True)
                        st.markdown(script_resp.text)
                        st.markdown("</div>", unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Failed: {e}")
