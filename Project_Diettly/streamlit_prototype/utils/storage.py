import streamlit as st
from datetime import datetime

def save_consent_log(message):
    if 'consent_log' not in st.session_state:
        st.session_state.consent_log = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.consent_log.append(f"[{timestamp}] {message}")