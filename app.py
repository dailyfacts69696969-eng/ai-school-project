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
                if raw_text.startswith("```json"): raw_text = raw_text[7:-3]
                elif raw_text.startswith("
