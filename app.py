import streamlit as st
from google import genai

# Setup your Gemini Client using the hidden API key
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

st.title("🎓 Student Performance Predictor")
st.write("Adjust your study habits below to see your real-time AI grade prediction.")

# We use a form so the AI only runs when the user clicks submit
with st.form("prediction_form"):
    # Interactive sliders and inputs
    study_hours = st.slider("Daily Study Hours", 0, 10, 3)
    math_science_score = st.number_input("Current Mathematics & Science Average (%)", 0, 100, 75)
    mock_score = st.number_input("Recent Mock Test Score", 0, 100, 60)
    
    submitted = st.form_submit_button("Predict My Performance")

if submitted:
    with st.spinner("Analyzing your academic profile..."):
        prompt = f"""
        Act as an expert academic counselor.
        The student studies {study_hours} hours a day.
        They have a {math_science_score}% average in secondary mathematics and science.
        Their recent mock test score is {mock_score}%.
        Provide a brief prediction of their final performance and 2 actionable study tips.
        """
        
        # Send the variables to Gemini
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        st.success("Analysis Complete!")
        st.write(response.text)
