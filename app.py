import streamlit as st
from groq import Groq

# --- INITIALIZATION ---
st.set_page_config(page_title="RHTWIN AI", page_icon="🤖", layout="wide")

# Replace with your actual Groq API Key
if "GROQ_KEY" in st.secrets:
    GROQ_API_KEY = st.secrets["GROQ_KEY"]
else:
    st.error("API Key not found in Streamlit Secrets!")
    st.stop()
client = Groq(api_key=GROQ_API_KEY)

def generate_code(prompt, lang):
    system_msg = f"You are RHTWIN, an elite programming AI. Output ONLY the source code for {lang}. No explanations, no markdown backticks."
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# --- API LOGIC FOR POWERSHELL ---
# This part allows your restricted system to get RAW text via WiFi
query_params = st.query_params
if "prompt" in query_params:
    prompt = query_params["prompt"]
    lang = query_params.get("lang", "python")
    code_output = generate_code(prompt, lang)
    st.text(code_output) # Returns raw text to PowerShell
    st.stop()

# --- WEB UI FOR PHONE/BROWSER ---
st.markdown("<h1 style='text-align: center; color: #00FFCC;'>RHTWIN PROGRAMMING AI</h1>", unsafe_allow_html=True)
st.divider()

col1, col2 = st.columns([1, 3])

with col1:
    language = st.selectbox("Select Language", ["Python", "JavaScript", "C++", "PowerShell", "SQL", "Java"])
    st.info("RHTWIN is ready for deployment. Connect via WiFi to use this as an API.")

with col2:
    user_prompt = st.text_area("What should RHTWIN build for you?", placeholder="e.g. Create a socket server in Python")
    if st.button("RUN RHTWIN ENGINE"):
        if user_prompt:
            with st.spinner("RHTWIN is thinking..."):
                result = generate_code(user_prompt, language)
                st.code(result, language=language.lower())
        else:
            st.warning("Please enter a prompt.")
