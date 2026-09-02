import streamlit as st
from google import genai

# Connect to Gemini
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# Make the website wide for a dashboard feel
st.set_page_config(layout="wide")

st.title("📊 CBSE Class 10 Teacher AI Dashboard")
st.write("Enter student scores and select the exam syllabus to generate an AI performance analysis.")

# --- PRE-LOADED CBSE SYLLABUS ---
MATH_SYLLABUS = [
    "Real Numbers", "Polynomials", "Pair of Linear Equations", 
    "Quadratic Equations", "Arithmetic Progressions", "Triangles", 
    "Coordinate Geometry", "Introduction to Trigonometry", 
    "Some Applications of Trigonometry", "Circles", "Areas Related to Circles", 
    "Surface Areas and Volumes", "Statistics", "Probability"
]

SCIENCE_SYLLABUS = [
    "Chemical Reactions and Equations", "Acids, Bases and Salts", 
    "Metals and Non-metals", "Carbon and its Compounds", 
    "Life Processes", "Control and Coordination", "How do Organisms Reproduce?", 
    "Heredity", "Light - Reflection and Refraction", "The Human Eye", 
    "Electricity", "Magnetic Effects of Electric Current", "Our Environment"
]

# --- DASHBOARD LAYOUT ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Exam & Syllabus Details")
    exam_type = st.selectbox(
        "Select Exam Phase", 
        ["PT-1", "Half Yearly", "PT-2", "Preboards 1", "Preboards 2"]
    )
    
    # Checkboxes/dropdowns for the teacher to select what was on the test
    math_topics = st.multiselect("📚 Mathematics Syllabus Covered in this exam:", MATH_SYLLABUS)
    science_topics = st.multiselect("🔬 Science Syllabus Covered in this exam:", SCIENCE_SYLLABUS)

with col2:
    st.subheader("2. Student Performance Entry")
    student_name = st.text_input("Student Name")
    
    # Score inputs
    math_score = st.number_input("Mathematics Score (%)", 0, 100, 0)
    science_score = st.number_input("Science Score (%)", 0, 100, 0)

# --- AI ANALYSIS GENERATOR ---
if st.button("Generate AI Student Report"):
    if not math_topics and not science_topics:
        st.warning("⚠️ Please select at least one syllabus topic before generating the report.")
    elif not student_name:
        st.warning("⚠️ Please enter a student name.")
    else:
        with st.spinner("Gemini is analyzing the student's performance..."):
            
            # The instructions telling the AI how to behave
            prompt = f"""
            You are an expert CBSE Class 10 academic coordinator and data analyst assisting a teacher.
            
            Context:
            - Exam Phase: {exam_type}
            - Mathematics Syllabus Tested: {', '.join(math_topics)}
            - Science Syllabus Tested: {', '.join(science_topics)}
            
            Student Data:
            - Name: {student_name}
            - Math Score: {math_score}%
            - Science Score: {science_score}%
            
            Based on these scores and the specific topics tested, provide a structured report for the teacher:
            1. Overall Performance Overview for this phase.
            2. Subject-Specific Breakdown (Identify if they are strong or weak based on the scores).
            3. Targeted Practice Areas (Explicitly list WHICH topics from the provided syllabus they need to practice more).
            4. Actionable Teaching Strategy (What the teacher should do next for this student).
            """
            
            # Get the response from Gemini
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            
            st.success("Report Generated!")
            st.markdown("---")
            st.write(response.text)
