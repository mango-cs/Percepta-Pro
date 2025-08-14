# -*- coding: utf-8 -*-
"""
Minimal test app
"""

import streamlit as st

st.set_page_config(
    page_title="Minimal Test",
    layout="wide"
)

st.markdown("# 🧪 Minimal Test App")
st.success("✅ Streamlit is working!")

if st.button("Test Button"):
    st.balloons()
    st.success("Button clicked successfully!")

st.markdown("## System Info")
st.write("This is a minimal test to verify Streamlit functionality.") 