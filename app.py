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

# --- CYBER-DEV / NEON FORGE DESIGN SYSTEM ---
st.set_page_config(page_title="EduPredict AI | NCS Goa", layout="wide", initial_sidebar_state="expanded")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');

    @keyframes cyberFadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes neonPulse {
        0% { box-shadow: 0 0 5px rgba(0, 229, 255, 0.2); }
        50% { box-shadow: 0 0 20px rgba(0, 229, 255, 0.6), 0 0 40px rgba(112, 0, 255, 0.4); }
        100% { box-shadow: 0 0 5px rgba(0, 229, 255, 0.2); }
    }

    @keyframes dataStream {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }

    @keyframes rotateTips {
        0% { opacity: 0; transform: translateY(15px); filter: blur(5px); }
        8% { opacity: 1; transform: translateY(0); filter: blur(0px); }
        18% { opacity: 1; transform: translateY(0); filter: blur(0px); }
        24% { opacity: 0; transform: translateY(-15px); filter: blur(5px); }
        100% { opacity: 0; transform: translateY(-15px); filter: blur(5px); }
    }

    /* Animated Cyber Divider */
    .gradient-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #00E5FF, #7000FF, #00E5FF, transparent);
        background-size: 200% 100%;
        animation: dataStream 4s infinite linear;
        margin: 2rem 0;
        opacity: 0.8;
    }

    /* Pro-Dev Cursor Spotlight */
    #cursor-glow {
        position: fixed;
        top: 0;
        left: 0;
        width: 500px;
        height: 500px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(0, 229, 255, 0.12) 0%, rgba(112, 0, 255, 0.08) 30%, rgba(0, 0, 0, 0) 70%);
        pointer-events: none;
        transform: translate(-50%, -50%);
        z-index: 99999;
        mix-blend-mode: screen;
        transition: transform 0.08s ease-out;
    }

    .tip-item {
        position: absolute;
        width: 100%;
        opacity: 0;
        will-change: transform, opacity, filter;
        animation: rotateTips 35s cubic-bezier(0.2, 0.8, 0.2, 1) infinite;
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
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
    }

    /* Base Theme */
    .stApp { 
        background-color: #050505; 
        color: #e2e8f0; 
        font-family: 'Inter', sans-serif; 
        animation: cyberFadeIn 0.8s ease-out;
        background-image: radial-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px);
        background-size: 30px 30px;
    }
    
    /* Inputs & Labels */
    .stTextInput label p, .stNumberInput label p, .stSlider label p, .stRadio label p, .stSelectbox label p {
        color: #94a3b8 !important; font-weight: 600 !important; font-size: 0.7rem !important; text-transform: uppercase; letter-spacing: 0.15em; font-family: 'JetBrains Mono', monospace;
    }
    
    .stTextInput input, .stNumberInput input, .stChatInput textarea {
        background-color: #0B0C10 !important; color: #00E5FF !important; border: 1px solid #1f2937 !important; border-radius: 6px !important;
        font-family: 'JetBrains Mono', monospace;
        transition: all 0.3s ease;
    }
    
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #00E5FF !important; box-shadow: 0 0 12px rgba(0, 229, 255, 0.3);
    }
    
    /* Cyber Buttons */
    .stButton button, .stDownloadButton button {
        background: linear-gradient(135deg, #7000FF 0%, #00E5FF 100%) !important;
        color: #ffffff !important; border: none !important; border-radius: 6px !important;
        font-weight: 800 !important; letter-spacing: 0.05em; padding: 0.6rem 1.5rem; text-transform: uppercase;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(0, 229, 255, 0.2);
    }
    
    .stButton button:hover {
        transform: translateY(-3px) scale(1.01);
        animation: neonPulse 1.5s infinite;
    }
    
    /* Razor-Sharp Glass Panels */
    .glass-panel { 
        background: rgba(15, 15, 20, 0.7); 
        border: 1px solid rgba(255, 255, 255, 0.05); 
        border-top: 1px solid rgba(0, 229, 255, 0.4); /* Neon Top Highlight */
        padding: 24px; border-radius: 12px; backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
        animation: cyberFadeIn 0.6s ease-out;
        transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
    }
    
    .glass-panel:hover {
        border-top-color: #7000FF;
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(112, 0, 255, 0.15);
    }

    /* Terminal Nav Guide */
    .nav-guide {
        background: linear-gradient(90deg, rgba(112, 0, 255, 0.1), rgba(0, 229, 255, 0.05));
        border-left: 4px solid #00E5FF;
        padding: 16px 24px;
        border-radius: 4px;
        color: #cbd5e1;
        margin-bottom: 1.5rem;
        box-shadow: inset 0 0 20px rgba(0, 229, 255, 0.05);
    }
    
    hr { display: none; }
    </style>

    <!-- Cursor follower DOM element & script -->
    <div id="cursor-glow"></div>
    <script>
    const cursorGlow = document.getElementById('cursor-glow');
    document.addEventListener('mousemove', (e) => {
        cursorGlow.style.left = e.clientX + 'px';
        cursorGlow.style.top = e.clientY + 'px';
    });
    </script>
""", unsafe_allow_html=True)

# --- SESSION STATES ---
if "app_started" not in st.session_state:
    st.session_state.app_started = False

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "> SYSTEM ONLINE. Standard 10th AI capabilities initialized. How can I assist you?"}]

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
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    # Split layout mirroring the architectural reference design
    col_text, col_img = st.columns([1.1, 1])
    
    with col_text:
        st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
        st.markdown("""
            <div style="padding-right: 20px;">
                <div style="color: #00E5FF; font-family: 'JetBrains Mono', monospace; font-weight: 700; letter-spacing: 2px; margin-bottom: 15px;">NAVY CHILDREN SCHOOL, GOA</div>
                <h1 style="font-size: 4.5rem; font-weight: 800; color: #ffffff; line-height: 1.1; margin-bottom: 25px; text-shadow: 0 0 20px rgba(0, 229, 255, 0.2);">We Build<br><span style="color: #7000FF;">Future.</span></h1>
                <p style="color: #94a3b8; font-size: 1.1rem; line-height: 1.7; margin-bottom: 40px; max-width: 90%;">
                    Welcome to EduPredict AI: Standard 10th Core Edition. Executing advanced computer vision extraction, macro-trend risk profiling, and diagnostic parent communication workflows.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        btn_c1, btn_c2 = st.columns([0.5, 0.5])
        with btn_c1:
            if st.button("Explore Now >", use_container_width=True):
                st.session_state.app_started = True
                st.rerun()
                
    with col_img:
        # Overlapping architectural image (NCS Goa photo)
        ncs_placeholder_url = "https://drive.scientificstudy.co/preview/eyJQYXRoIjoiV2ViU2l0ZUNvbnRlbnQvTUVESUFDT05URU5ULzMwMTYvMTMwMTYvMjgwNTciLCJOYW1lIjoiTWVkaWFfMjUwNDMwMTMxNDU3NDA4LmpwZyJ9.Lso2JNxIJM5mPFWSMxOxybFbKN1H2sYFGJ%2FONjGlcJo"
        
        st.markdown(f"""
            <img src="{ncs_placeholder_url}" 
                 style="width: 125%; height: 500px; object-fit: cover; border-radius: 16px; margin-left: -25%; 
                        box-shadow: -20px 20px 60px rgba(0,0,0,0.9); border: 1px solid rgba(0, 229, 255, 0.3); position: relative; z-index: 10;">
        """, unsafe_allow_html=True)
        
    st.stop()

# --- SIDEBAR: AI TEACHER ASSISTANT PANEL ---
with st.sidebar:
    st.markdown("### ⚡ SYSTEM TERMINAL")
    st.caption("Standard 10th Guidance & Workflows.")
    
    chat_container = st.container(height=450)
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if chat_prompt := st.chat_input("Execute command or prompt AI..."):
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
                    st.error(f"Execution Error: {e}")
        st.rerun()

# --- HEADER BAR ---
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.markdown("### EDUPREDICT AI <span style='color:#00E5FF; font-size: 0.9rem; font-weight: 600; font-family: \"JetBrains Mono\", monospace;'>// NCS_GOA : STD_10</span>", unsafe_allow_html=True)
with col_head2:
    exam_phase = st.selectbox("EVALUATION PHASE", ["PT-1", "Half Yearly", "PT-2", "Preboards"])
    max_marks = 40 if "PT" in exam_phase else 80

st.markdown("<div class='gradient-divider'></div>", unsafe_allow_html=True)

# Unified Single Box with Rotating Navigation & Pro Tips Ticker
st.markdown("""
    <div class="nav-guide">
        <div class="tips-container">
            <div class="tip-item"><span style="color: #00E5FF;">> SYS_NOTICE:</span> Click the >> arrow in the top-left corner to access the hidden AI System Terminal.</div>
            <div class="tip-item"><span style="color: #7000FF;">> PRO_TIP:</span> Upload clear Standard 10 test sheets into the Extraction Hub for instant score auto-fill.</div>
            <div class="tip-item"><span style="color: #00E5FF;">> PRO_TIP:</span> Leverage the AI to track advanced student competencies in national exams like Vidyarthi Vigyan Manthan (VVM) or NFO.</div>
            <div class="tip-item"><span style="color: #7000FF;">> PRO_TIP:</span> Use the Batch Class CSV Upload to analyze entire Standard 10 datasets and identify outliers in milliseconds.</div>
            <div class="tip-item"><span style="color: #00E5FF;">> PRO_TIP:</span> Generate professional, diagnostic Parent-Teacher Conference scripts for board readiness with a single click.</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- AI DOCUMENT INGESTION HUB ---
with st.expander("📂 VISION INGESTION & EXTRACTION HUB", expanded=False):
    st.markdown("#### 📄 Upload Standard 10 Test Sheet Image")
    uploaded_paper = st.file_uploader("Accepts PNG, JPG, JPEG", type=["png", "jpg", "jpeg"], key="paper_up")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        extract_clicked = st.button("RUN VISION EXTRACTION //", use_container_width=True)
        
    if uploaded_paper and extract_clicked:
        with st.spinner("Executing Gemini Vision Core..."):
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
                st.toast('Vision Extraction Complete!', icon='👁️')
            except Exception as e:
                st.error(f"Extraction failed: {e}")

    if st.session_state.raw_extracted:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown("#### 📋 EXTRACTED DATA MATRIX", unsafe_allow_html=True)
        
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
            st.metric("Mathematics", p_math, "+2.5 ∆")
            st.metric("Science", p_sci, "-1.2 ∆")
        with prev_col3:
            st.metric("Social Science", p_sst, "+4.0 ∆")
            st.metric("English", p_eng, "+0.5 ∆")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("OVERRIDE FORM DATA //", use_container_width=True):
            st.session_state.ext_name = p_name if p_name != "Not Detected" else ""
            st.session_state.ext_roll = p_roll if p_roll != "N/A" else ""
            st.session_state.ext_math = float(p_math)
            st.session_state.ext_sci = float(p_sci)
            st.session_state.ext_sst = float(p_sst)
            st.session_state.ext_eng = float(p_eng)
            
            st.toast("Form overwritten with vision data!", icon="⚡")
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
        if st.button("EXECUTE BATCH ANALYSIS //", use_container_width=True):
            with st.spinner("Processing macro trends with Gemini..."):
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
                    st.toast("Macro Analysis Complete", icon="📊")
                    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
                    st.markdown("#### 📑 DIAGNOSTIC BATCH REPORT")
                    st.markdown(batch_resp.text)
                    st.markdown("</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Batch Analysis Failed: {e}")

st.markdown("<div class='gradient-divider'></div>", unsafe_allow_html=True)

# --- SPLIT SCREEN LAYOUT ---
left_col, right_col = st.columns([4, 8], gap="large")

with left_col:
    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#ffffff; font-size: 1rem; margin-bottom: 1rem;'>👤 IDENTITY CREDENTIALS</h4>", unsafe_allow_html=True)
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
    st.markdown("<h4 style='color:#ffffff; font-size: 1rem; margin-bottom: 1rem;'>🏫 BEHAVIORAL TELEMETRY</h4>", unsafe_allow_html=True)
    attendance = st.slider("Attendance Rate (%)", 0, 100, 88)
    assignments = st.slider("Assignment Completion (%)", 0, 100, 92)
    participation = st.slider("Participation Score", 1, 10, 8)
    behavior = st.slider("Conduct Index", 1, 10, 9)
    st.markdown("</div><br>", unsafe_allow_html=True)

    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#ffffff; font-size: 1rem; margin-bottom: 1rem;'>📚 SUBJECT SCORE MATRIX</h4>", unsafe_allow_html=True)
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
                <p style='color: #94a3b8; font-family: "JetBrains Mono", monospace; font-size: 0.75rem; text-transform: uppercase;'>SYS_AVG</p>
                <h3 style='color: #00E5FF; font-family: "JetBrains Mono", monospace; font-size: 1.8rem; margin: 0; text-shadow: 0 0 10px rgba(0,229,255,0.4);'>{avg_score:.1f}%</h3>
            </div>
        """, unsafe_allow_html=True)
    with kpi2:
        risk_color = "#10b981" if avg_score > 75 and attendance > 75 else "#ef4444"
        risk_text = "NOMINAL 🟢" if avg_score > 75 and attendance > 75 else "CRITICAL 🔴"
        st.markdown(f"""
            <div class='glass-panel' style='text-align: center; padding: 15px;'>
                <p style='color: #94a3b8; font-family: "JetBrains Mono", monospace; font-size: 0.75rem; text-transform: uppercase;'>RISK_PROFILE</p>
                <h3 style='color: {risk_color}; font-family: "JetBrains Mono", monospace; font-size: 1.2rem; margin-top: 5px; text-shadow: 0 0 10px {risk_color}80;'>{risk_text}</h3>
            </div>
        """, unsafe_allow_html=True)
    with kpi3:
        st.markdown(f"""
            <div class='glass-panel' style='text-align: center; padding: 15px;'>
                <p style='color: #94a3b8; font-family: "JetBrains Mono", monospace; font-size: 0.75rem; text-transform: uppercase;'>GAIN_POTENTIAL</p>
                <h3 style='color: #7000FF; font-family: "JetBrains Mono", monospace; font-size: 1.8rem; margin: 0; text-shadow: 0 0 10px rgba(112,0,255,0.4);'>+{gain_potential}%</h3>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("#### 📈 PERFORMANCE DISTRIBUTION")
    chart_data = pd.DataFrame({
        "Subject": list(scores.keys()),
        "Score (%)": list(scores.values())
    })
    # Native Streamlit chart using the primary accent color
    st.bar_chart(chart_data, x="Subject", y="Score (%)", color="#00E5FF", height=250)

    if avg_score < 50:
        st.error("⚠️ CRITICAL ALERT: Student's overall average is below 50%. Immediate board intervention required.")
        if st.button("DISPATCH SECURE EMAIL ALERT //", use_container_width=True):
            if not parent_email:
                st.warning("Please enter a valid Parent Email Address on the left panel.")
            else:
                with st.spinner("Encrypting and dispatching alert..."):
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
                            
                            st.toast("Email Dispatched Securely!", icon="📧")
                            st.success(f"✅ Alert successfully dispatched to {parent_email}")
                    except Exception as e:
                        st.error(f"Failed to send email: {e}")

    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("#### 📊 LIVE ROSTER DATABASE")
    if not st.session_state.class_portfolio.empty:
        st.dataframe(st.session_state.class_portfolio, use_container_width=True)
    else:
        st.info("💡 Database is empty. Input parameters on the left and append to roster.")

    btn_col1, btn_col2, btn_col3 = st.columns(3)
    with btn_col1:
        if st.button("APPEND TO ROSTER //", use_container_width=True):
            if not student_name:
                st.error("⚠️ Invalid student name.")
            else:
                new_student = pd.DataFrame({
                    "Name": [student_name], "Roll No": [roll_no], "Class": [class_sec], "Parent Phone": [parent_phone], "Parent Email": [parent_email],
                    "Exam": [exam_phase], "Attendance (%)": [attendance], "Assignments (%)": [assignments], "Average (%)": [round(avg_score, 1)]
                })
                st.session_state.class_portfolio = pd.concat([st.session_state.class_portfolio, new_student], ignore_index=True)
                st.balloons()
                st.toast(f"Data appended for {student_name}!", icon="📋")
                time.sleep(1)
                st.rerun()

    with btn_col2:
        if not st.session_state.class_portfolio.empty:
            csv_file = st.session_state.class_portfolio.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="EXPORT DATASET //", data=csv_file,
                file_name=f"NCS_Goa_Std10_Portfolio_{exam_phase}.csv", mime="text/csv", use_container_width=True
            )
        else:
            st.button("EXPORT DATASET //", disabled=True, use_container_width=True)

    with btn_col3:
        if st.button("PURGE DATABASE //", use_container_width=True):
            st.session_state.class_portfolio = pd.DataFrame(columns=["Name", "Roll No", "Class", "Parent Phone", "Parent Email", "Exam", "Attendance (%)", "Assignments (%)", "Average (%)"])
            st.rerun()

    st.markdown("<div class='gradient-divider'></div>", unsafe_allow_html=True)
    
    action_col1, action_col2 = st.columns(2)
    
    with action_col1:
        if st.button("EXECUTE AI DIAGNOSTICS //", use_container_width=True):
            if not student_name:
                st.error("⚠️ Specify a target student before execution.")
            else:
                with st.spinner("Synthesizing metrics..."):
                    try:
                        prompt = f"""
                        Act as an elite CBSE Class 10 academic coordinator at Navy Children School, Goa.
                        Student: {student_name} ({class_sec}, Roll: {roll_no}). Phase: {exam_phase}
                        Telemetry: {attendance}% attendance, {assignments}% assignments.
                        Scores (%): Math {scores['Maths']:.1f}, Sci {scores['Science']:.1f}, SST {scores['SST']:.1f}, Eng {scores['English']:.1f}.
                        Provide an executive 4-bullet assessment covering board exam trajectory and tactical intervention steps.
                        """
                        resp = client.models.generate_content(model="gemini-3.5-flash", contents=prompt)
                        st.toast("Diagnostic Complete", icon="🧠")
                        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
                        st.markdown("#### 📑 DIAGNOSTIC OUTPUT MATRIX")
                        st.write(resp.text)
                        st.markdown("</div>", unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"❌ Execution Failed: {e}")

    with action_col2:
        if st.button("GENERATE MEETING SCRIPT //", use_container_width=True):
            if not student_name:
                st.error("⚠️ Specify a target student before execution.")
            else:
                with st.spinner("Drafting professional script..."):
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
                        st.toast("Script Synthesized", icon="🎙️")
                        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
                        st.markdown("#### 🎙️ CONFERENCE SCRIPT & AGENDA")
                        st.markdown(script_resp.text)
                        st.markdown("</div>", unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"❌ Execution Failed: {e}")
