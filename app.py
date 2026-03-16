# ============================================================
# M-PESA SCAM SMS DETECTOR - STREAMLIT APP
# File: app.py
# ============================================================

import streamlit as st
# streamlit: builds our entire website interface

import pickle
# pickle: loads our saved model files

import re
# re: for cleaning text (same as in Phase 3)

import time
# time: used to create a small animation effect

# ============================================================
# SECTION 1: PAGE CONFIGURATION
# This must be the VERY FIRST streamlit command in the file
# ============================================================

st.set_page_config(
    page_title="M-Pesa Scam Detector",
    # Sets the browser tab title

    page_icon="🛡️",
    # Sets the icon in the browser tab

    layout="centered",
    # Centers the content on the page

    initial_sidebar_state="collapsed"
    # Hides the sidebar by default
)

# ============================================================
# SECTION 2: LOAD THE TRAINED MODEL
# We use @st.cache_resource so it only loads ONCE
# Without this, it would reload every time a user clicks a button
# ============================================================

@st.cache_resource
def load_model():
    # This function loads both saved files from Phase 3
    with open('scam_model.pkl', 'rb') as f:
        model = pickle.load(f)
    # 'rb' means "read binary" — reading computer-formatted file

    with open('vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)

    return model, vectorizer
    # Returns both items so we can use them

model, vectorizer = load_model()
# Actually call the function and store results

# ============================================================
# SECTION 3: TEXT CLEANING FUNCTION
# Exact same function from Phase 3 — must match!
# ============================================================

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\d+', 'NUM', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# ============================================================
# SECTION 4: PREDICTION FUNCTION
# Takes an SMS, returns prediction + confidence
# ============================================================

def predict_sms(sms_text):
    cleaned = clean_text(sms_text)
    vectorized = vectorizer.transform([cleaned])
    prediction = model.predict(vectorized)[0]
    probability = model.predict_proba(vectorized)[0]
    confidence = max(probability) * 100
    return prediction, confidence

# ============================================================
# SECTION 5: CUSTOM STYLING (CSS)
# CSS = instructions that control how things look on screen
# You don't need to understand CSS — just keep it as is
# ============================================================

st.markdown("""
<style>
    /* Import a clean Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    /* Apply font to everything */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Style the main container */
    .main {
        background-color: #f8f9fa;
    }

    /* Style the header box */
    .header-box {
        background: linear-gradient(135deg, #1a7a4a, #25a562);
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(26, 122, 74, 0.3);
    }

    /* Header title */
    .header-title {
        color: white;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
    }

    /* Header subtitle */
    .header-subtitle {
        color: rgba(255,255,255,0.85);
        font-size: 1rem;
        margin-top: 0.5rem;
    }

    /* SCAM result box - red */
    .scam-box {
        background: linear-gradient(135deg, #ff4444, #cc0000);
        color: white;
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        margin: 1.5rem 0;
        box-shadow: 0 4px 20px rgba(255, 68, 68, 0.4);
        animation: pulse 0.5s ease-in-out;
    }

    /* LEGIT result box - green */
    .legit-box {
        background: linear-gradient(135deg, #1a7a4a, #25a562);
        color: white;
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        margin: 1.5rem 0;
        box-shadow: 0 4px 20px rgba(37, 165, 98, 0.4);
        animation: slideIn 0.5s ease-in-out;
    }

    /* Result title text */
    .result-title {
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
    }

    /* Result subtitle text */
    .result-subtitle {
        font-size: 1rem;
        margin-top: 0.5rem;
        opacity: 0.9;
    }

    /* Confidence percentage display */
    .confidence-text {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }

    /* The tips/warning box below result */
    .tips-box {
        background: white;
        border-left: 4px solid #ff4444;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }

    .tips-box-legit {
        background: white;
        border-left: 4px solid #25a562;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }

    /* Fade-in animation */
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(20px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    @keyframes pulse {
        0%   { transform: scale(0.95); }
        50%  { transform: scale(1.02); }
        100% { transform: scale(1); }
    }

    /* Hide Streamlit default menu and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Style the Check SMS button */
    div.stButton > button {
        background: linear-gradient(135deg, #1a7a4a, #25a562);
        color: white;
        border: none;
        padding: 0.75rem 3rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 50px;
        width: 100%;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(26, 122, 74, 0.3);
    }

    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(26, 122, 74, 0.4);
    }

    /* Style the text area */
    .stTextArea textarea {
        border-radius: 12px;
        border: 2px solid #e0e0e0;
        font-size: 0.95rem;
        padding: 1rem;
        transition: border 0.3s ease;
    }

    .stTextArea textarea:focus {
        border-color: #25a562;
    }
</style>
""", unsafe_allow_html=True)
# unsafe_allow_html=True lets us use custom HTML/CSS
# Without it, Streamlit would ignore our styling

# ============================================================
# SECTION 6: APP HEADER
# ============================================================

st.markdown("""
<div class="header-box">
    <p class="header-title">🛡️ M-Pesa Scam Detector</p>
    <p class="header-subtitle">
        Linda pesa yako · Protect your money<br>
        Paste any M-Pesa SMS to instantly check if it's a scam
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# SECTION 7: LANGUAGE SELECTOR
# Allows switching between English and Swahili
# ============================================================

col1, col2, col3 = st.columns([1, 2, 1])
# This creates 3 columns. We use the middle one (col2) for centering

with col2:
    language = st.radio(
        "Language / Lugha:",
        ["English", "Kiswahili"],
        horizontal=True
        # horizontal=True puts options side by side
    )

# Based on language, set the text for the whole app
if language == "English":
    placeholder_text = "Paste your M-Pesa SMS here...\n\nExample: M-PESA: You have received KSh 2,500.00 from JOHN KAMAU..."
    button_text = "🔍 Check SMS"
    input_label = "📱 Paste your SMS message below:"
    clear_label = "🗑️ Clear"
    examples_title = "💡 Try these example messages:"
else:
    placeholder_text = "Weka ujumbe wako wa M-Pesa hapa...\n\nMfano: M-PESA: Umepokea KSh 2,500.00 kutoka kwa JOHN KAMAU..."
    button_text = "🔍 Angalia SMS"
    input_label = "📱 Weka ujumbe wako wa SMS hapa chini:"
    clear_label = "🗑️ Futa"
    examples_title = "💡 Jaribu mifano hii:"

# ============================================================
# SECTION 8: EXAMPLE MESSAGES (QUICK TEST BUTTONS)
# ============================================================

st.markdown(f"**{examples_title}**")

# Create 2 columns for the example buttons
ex_col1, ex_col2 = st.columns(2)

with ex_col1:
    if st.button("⚠️ Example Scam SMS"):
        st.session_state['sms_input'] = "Umeshinda KSh 50,000! Tuma KSh 500 sasa kupokea zawadi yako. Piga simu: 0712345678"
        # session_state stores data between button clicks

with ex_col2:
    if st.button("✅ Example Legit SMS"):
        st.session_state['sms_input'] = "M-PESA: You have received KSh 2,500.00 from JOHN KAMAU 0722111000. New balance: KSh 4,320.00"

# ============================================================
# SECTION 9: THE SMS INPUT TEXT BOX
# ============================================================

sms_input = st.text_area(
    label=input_label,
    height=150,
    # Height in pixels — tall enough to show a full SMS

    placeholder=placeholder_text,
    # Greyed-out hint text when the box is empty

    value=st.session_state.get('sms_input', ''),
    # Load any pre-filled example text from the buttons above
    # .get('sms_input', '') means: get saved value, or use empty string

    key="sms_text_area"
)

# ============================================================
# SECTION 10: BUTTONS ROW
# ============================================================

btn_col1, btn_col2 = st.columns([3, 1])
# 3:1 ratio — Check SMS button is wider, Clear button is narrow

with btn_col1:
    check_button = st.button(button_text, type="primary")
    # type="primary" makes it the main highlighted button

with btn_col2:
    clear_button = st.button(clear_label)

if clear_button:
    st.session_state['sms_input'] = ''
    # Clears the saved text and refreshes the page
    st.rerun()

# ============================================================
# SECTION 11: RESULTS — THE MAIN EVENT
# ============================================================

if check_button:
    # Only run this block when user clicks "Check SMS"

    if not sms_input.strip():
        # .strip() removes spaces — checks if box is truly empty
        st.warning("⚠️ Please paste an SMS message first!" if language == "English"
                   else "⚠️ Tafadhali weka ujumbe wa SMS kwanza!")

    else:
        # Show a loading spinner while processing
        with st.spinner("Analyzing SMS..." if language == "English" else "Inachambua SMS..."):
            time.sleep(0.8)
            # Small 0.8 second pause — makes the app feel more responsive
            prediction, confidence = predict_sms(sms_input)

        # ---- DISPLAY SCAM RESULT ----
        if prediction == 0:
            st.markdown(f"""
            <div class="scam-box">
                <p class="result-title">⚠️ SCAM DETECTED</p>
                <p class="confidence-text">{confidence:.1f}%</p>
                <p class="result-subtitle">Confidence Score</p>
            </div>
            """, unsafe_allow_html=True)

            # Warning tips for scam
            if language == "English":
                st.markdown("""
                <div class="tips-box">
                    <strong>🚨 Safety Tips:</strong><br><br>
                    ❌ Do NOT send any money to numbers in this SMS<br>
                    ❌ Do NOT share your M-Pesa PIN with anyone<br>
                    ❌ Do NOT call back unknown numbers in suspicious SMS<br>
                    ✅ Report to Safaricom: Call <strong>0722 000 000</strong><br>
                    ✅ Report scams to <strong>DCI Kenya: 0800 722 203</strong>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="tips-box">
                    <strong>🚨 Tahadhari:</strong><br><br>
                    ❌ USITUME pesa yoyote kwa nambari zilizo katika SMS hii<br>
                    ❌ USISHIRIKI PIN yako ya M-Pesa na mtu yeyote<br>
                    ❌ USIPIGIE simu nambari zisizojulikana<br>
                    ✅ Ripoti kwa Safaricom: Piga simu <strong>0722 000 000</strong><br>
                    ✅ Ripoti ulaghai kwa <strong>DCI Kenya: 0800 722 203</strong>
                </div>
                """, unsafe_allow_html=True)

        # ---- DISPLAY LEGIT RESULT ----
        else:
            st.markdown(f"""
            <div class="legit-box">
                <p class="result-title">✅ LEGIT MESSAGE</p>
                <p class="confidence-text">{confidence:.1f}%</p>
                <p class="result-subtitle">Confidence Score</p>
            </div>
            """, unsafe_allow_html=True)

            if language == "English":
                st.markdown("""
                <div class="tips-box-legit">
                    <strong>✅ This looks like a genuine M-Pesa message.</strong><br><br>
                    💡 Always double-check that amounts and names match your transaction<br>
                    💡 Real M-Pesa messages come from sender ID: <strong>MPESA</strong><br>
                    💡 When in doubt, check your M-Pesa statement in the app
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="tips-box-legit">
                    <strong>✅ Ujumbe huu unaonekana kuwa wa kweli wa M-Pesa.</strong><br><br>
                    💡 Daima thibitisha kwamba kiasi na majina yanafanana na muamala wako<br>
                    💡 Ujumbe wa kweli wa M-Pesa hutoka kwa mtumaji: <strong>MPESA</strong><br>
                    💡 Ukishuku, angalia taarifa yako ya M-Pesa katika programu
                </div>
                """, unsafe_allow_html=True)

        # ---- CONFIDENCE METER ----
        st.markdown("---")
        st.markdown("**📊 Confidence Meter:**" if language == "English"
                    else "**📊 Kipimo cha Uhakika:**")
        st.progress(confidence / 100)
        # progress() shows a visual bar from 0 to 100%
        # We divide by 100 because it expects a value between 0 and 1

        # ---- ANALYZED MESSAGE PREVIEW ----
        with st.expander("🔎 View Analyzed Message" if language == "English"
                         else "🔎 Ona Ujumbe Uliochunguzwa"):
            st.text(sms_input)
            # st.expander creates a collapsible section
            # Users can click to see the original message

# ============================================================
# SECTION 12: HOW TO USE + FOOTER
# ============================================================

st.markdown("---")

with st.expander("ℹ️ How to use this app" if language == "English"
                 else "ℹ️ Jinsi ya kutumia programu hii"):
    if language == "English":
        st.markdown("""
        **How to use the M-Pesa Scam Detector:**

        1. **Copy** any SMS message from your phone
        2. **Paste** it into the text box above
        3. **Click** the "Check SMS" button
        4. The app will instantly tell you if it's a SCAM or LEGIT

        **What the Confidence Score means:**
        - **90–100%** → Very confident in the result
        - **70–89%** → Fairly confident
        - **Below 70%** → Uncertain — treat with caution

        **Limitations:** This app is trained on a starter dataset.
        It gets smarter as more data is added. Always use your judgment
        alongside the app's result.
        """)
    else:
        st.markdown("""
        **Jinsi ya kutumia M-Pesa Scam Detector:**

        1. **Nakili** ujumbe wowote wa SMS kutoka kwa simu yako
        2. **Bandika** kwenye kisanduku cha maandishi hapo juu
        3. **Bonyeza** kitufe cha "Angalia SMS"
        4. Programu itakuambia mara moja kama ni UDANGANYIFU au HALISI

        **Maana ya Alama ya Uhakika:**
        - **90–100%** → Uhakika mkubwa sana
        - **70–89%** → Uhakika wa wastani
        - **Chini ya 70%** → Shaka — kuwa makini

        **Mipaka:** Programu hii imefunzwa kwa dataset ndogo.
        Inakuwa na akili zaidi kadri data inavyoongezwa.
        """)

# Footer
st.markdown("""
<div style='text-align: center; color: #888; font-size: 0.8rem; margin-top: 2rem;'>
    🛡️ M-Pesa Scam Detector · Built for Kenya · Powered by Machine Learning<br>
    <em>Protect yourself. Share with friends and family.</em>
</div>
""", unsafe_allow_html=True)