
import streamlit as st
import pandas as pd

st.title("🚜 श्री बिहारी जी कोल्ड स्टोरेज")
st.write("उदैतापुर, कन्नौज | क्षमता: 2,00,000 पैकेट")

name = st.text_input("किसान का नाम")
pkts = st.number_input("पैकेट", min_value=0)
rate = st.number_input("रेट", value=300)

if st.button("डाटा सेव करें"):
    st.success(f"{name} का {pkts * rate} रुपये का हिसाब दर्ज हुआ।")
