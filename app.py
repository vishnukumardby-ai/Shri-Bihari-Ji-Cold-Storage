import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import time

# 1. पेज सेटअप
st.set_page_config(page_title="Shri Bihari Ji Cold Storage", layout="wide")

# 2. गूगल शीट कनेक्शन
conn = st.connection("gsheets", type=GSheetsConnection)

# --- ऊपर दाईं ओर भाषा का स्विच (Kill Switch) ---
st.markdown('<style>div.row-widget.stRadio > div{flex-direction:row; justify-content: flex-end;}</style>', unsafe_allow_html=True)
lang = st.radio("", ["English", "Hindi"], label_visibility="collapsed")

# 3. मुख्य हेडर
st.markdown(f"""
    <div style='text-align: center; background-color: #1E3A8A; padding: 20px; border-radius: 10px; color: white;'>
        <h1 style='margin: 0;'>🚜 श्री बिहारी जी कोल्ड स्टोरेज</h1>
        <p style='font-size: 18px; margin: 5px 0;'>उदैतापुर, मनीमऊ, कन्नौज (उत्तर प्रदेश)</p>
        <p style='font-size: 14px; margin: 2px 0;'>📧 shribiharijicoldstorage@gmail.com</p>
        <p style='font-size: 14px; margin: 2px 0;'>📞 9838646586, 9621996103, 7007490379</p>
    </div>
""", unsafe_allow_html=True)

# 4. ऑटोमेटिक फोटो गैलरी (Slideshow)
# नोट: यहाँ आप अपनी असली फोटो के लिंक डाल सकते हैं
photos = [
    "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=800", # आलू की फोटो
    "https://images.unsplash.com/photo-1590165482129-1b8b27698780?w=800", # कोल्ड स्टोरेज जैसा दृश्य
    "https://images.unsplash.com/photo-1523348837708-15d4a09cfac2?w=800"  # खेत की फोटो
]

st.markdown("---") # एक हल्की लाइन

# फोटो को अपने आप बदलने के लिए छोटा सा लॉजिक
if 'photo_index' not in st.session_state:
    st.session_state.photo_index = 0

# फोटो डिस्प्ले बॉक्स (हेडर के बराबर चौड़ा)
placeholder = st.empty()
with placeholder.container():
    st.image(photos[st.session_state.photo_index], use_container_width=True)

# 5 सेकंड बाद फोटो बदलने का सेटअप
time.sleep(5)
st.session_state.photo_index = (st.session_state.photo_index + 1) % len(photos)
st.rerun()

# 5. साइडबार मेन्यू
t_home = "Home" if lang == "English" else "होम"
t_admin = "Admin Login" if lang == "English" else "एडमिन लॉगिन"
t_farmer = "Farmer Login" if lang == "English" else "किसान लॉगिन"

menu = st.sidebar.selectbox("Main Menu", [t_home, t_admin, t_farmer])

# --- एडमिन सेक्शन ---
if menu == t_admin:
    password = st.sidebar.text_input("Password", type="password")
    if password == "bihariji123":
        task = st.sidebar.radio("Task", ["Registration", "Amad Entry"])
        if task == "Registration":
            st.subheader("🆕 नया पंजीकरण")
        elif task == "Amad Entry":
            st.subheader("📦 आमद एंट्री")

# --- किसान लॉगिन ---
elif menu == t_farmer:
    st.subheader("🌾 किसान लॉगिन / Farmer Login")
    col1, col2 = st.columns(2)
    with col1:
        f_acc = st.text_input("अकाउंट नंबर")
    with col2:
        f_mob = st.text_input("मोबाइल नंबर")
    
    if st.button("विवरण देखें"):
        st.info("डेटा देखने के लिए लॉगिन करें।")

else:
    st.write("") 
