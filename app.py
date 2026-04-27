import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# पेज सेटिंग
st.set_page_config(page_title="Shri Bihari Ji Cold Storage", layout="wide")

# भाषा चयन
lang = st.sidebar.radio("Language / भाषा", ["English", "Hindi"])

# शब्दकोश
t = {
    "title": "🚜 SHRI BIHARI JI COLD STORAGE" if lang == "English" else "🚜 श्री बिहारी जी कोल्ड स्टोरेज",
    "addr": "Udaitapur, Manimau, Kannauj" if lang == "English" else "उदैतापुर, मानीमऊ, कन्नौज",
    "home": "Home" if lang == "English" else "मुख्य पेज",
    "k_login": "Farmer Login" if lang == "English" else "किसान लॉगिन",
    "a_login": "Admin" if lang == "English" else "एडमिन",
    "mob": "Mobile Number" if lang == "English" else "मोबाइल नंबर",
    "acc": "Account Number" if lang == "English" else "अकाउंट नंबर",
    "signin_btn": "Sign In" if lang == "English" else "प्रवेश करें",
}

# हेडर डिजाइन
st.markdown(f"""
    <div style='text-align: center; background-color: #1E3A8A; padding: 25px; border-radius: 15px; color: white;'>
        <h1 style='margin: 0;'>{t['title']}</h1>
        <h2 style='margin: 5px; font-size: 24px;'><b>{t['addr']}</b></h2>
        <p style='font-size: 16px; margin: 0;'>📞 9838646586, 9621996103, 7007490379</p>
    </div>
    <br>
""", unsafe_allow_html=True)

conn = st.connection("gsheets", type=GSheetsConnection)
choice = st.radio("", [t['home'], t['k_login'], t['a_login']], horizontal=True)
st.markdown("---")

if choice == t['k_login']:
    st.subheader(t['k_login'])
    col1, col2 = st.columns(2)
    with col1: km = st.text_input(t['mob'], key="k_mob")
    with col2: ka = st.text_input(t['acc'], type="password", key="k_acc")
    
    if st.button(t['signin_btn']):
        try:
            # मास्टर शीट से मिलान
            m_df = conn.read(worksheet="Master", ttl=0)
            match = m_df[(m_df['Mobile_Number'].astype(str).str.strip() == str(km).strip()) & 
                         (m_df['Account_Number'].astype(str).str.strip() == str(ka).strip())]
            
            if not match.empty:
                f_name = match['Name'].iloc[0]
                st.success(f"नमस्ते, {f_name} जी!")
                tab1, tab2, tab3 = st.tabs(["आलू स्टॉक (Amad)", "लोन (Loan)", "बारदाना (Bags)"])
                
                # 1. Amad Data (Account_Number के आधार पर)
                with tab1:
                    try:
                        a_df = conn.read(worksheet="Amad", ttl=0)
                        f_a = a_df[a_df['Account_Number'].astype(str).str.strip() == str(ka).strip()]
                        if not f_a.empty: st.table(f_a[['Date', 'Lot_Number', 'Packets', 'Type']])
                        else: st.write("कोई स्टॉक रिकॉर्ड नहीं मिला।")
                    except: st.warning("Amad शीट में Account_Number कॉलम जोड़ें।")

                # 2. Loan Data (Account_Number के आधार पर)
                with tab2:
                    try:
                        l_df = conn.read(worksheet="Loan", ttl=0)
                        f_l = l_df[l_df['Account_Number'].astype(str).str.strip() == str(ka).strip()]
                        if not f_l.empty: st.table(f_l[['Date', 'Voucher_Number', 'Amount']])
                        else: st.write("कोई लोन रिकॉर्ड नहीं मिला।")
                    except: st.warning("Loan शीट के कॉलम चेक करें।")

                # 3. Bardana Data
                with tab3:
                    st.write("बारदाना रिकॉर्ड अभी उपलब्ध नहीं है।")
            else:
                st.error("रिकॉर्ड नहीं मिला। कृपया सही जानकारी डालें।")
        except Exception as e:
            st.error("कनेक्शन में समस्या।")
else:
    st.info("स्वागत है! कृपया अपना हिसाब देखने के लिए लॉगिन करें।")
