import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# पेज की बुनियादी सेटिंग
st.set_page_config(page_title="Shri Bihari Ji Cold Storage", layout="wide")

# भाषा चयन
lang = st.sidebar.radio("Language / भाषा", ["English", "Hindi"])

# शब्दकोश - मानीमऊ और सही पते के साथ
t = {
    "title": "🚜 SHRI BIHARI JI COLD STORAGE" if lang == "English" else "🚜 श्री बिहारी जी कोल्ड स्टोरेज",
    "addr": "Udaitapur, Manimau, Kannauj" if lang == "English" else "उदैतापुर, मानीमऊ, कन्नौज",
    "home": "Home" if lang == "English" else "मुख्य पेज",
    "k_login": "Farmer Login" if lang == "English" else "किसान लॉगिन",
    "a_login": "Admin" if lang == "English" else "एडमिन",
    "mob": "Mobile Number" if lang == "English" else "मोबाइल नंबर",
    "acc": "Account Number" if lang == "English" else "अकाउंट नंबर",
    "signin_btn": "Sign In" if lang == "English" else "प्रवेश करें",
    "save": "Save" if lang == "English" else "सुरक्षित करें",
}

# मुख्य हेडर (Blue Box)
st.markdown(f"""
    <div style='text-align: center; background-color: #1E3A8A; padding: 25px; border-radius: 15px; color: white;'>
        <h1 style='margin: 0; font-family: "Arial Black", sans-serif;'>{t['title']}</h1>
        <h2 style='margin: 5px; font-size: 24px;'><b>{t['addr']}</b></h2>
        <p style='font-size: 16px; margin: 0;'>📞 9838646586, 9621996103, 7007490379</p>
    </div>
    <br>
""", unsafe_allow_html=True)

# गूगल शीट से कनेक्शन
conn = st.connection("gsheets", type=GSheetsConnection)

# मुख्य विकल्प (Tabs)
choice = st.radio("", [t['home'], t['k_login'], t['a_login']], horizontal=True)
st.markdown("---")

if choice == t['home']:
    st.info("आधुनिक तकनीक और सुरक्षित भंडारण। / Modern Technology & Secure Storage.")
    st.image("https://via.placeholder.com/800x300.png?text=Shri+Bihari+Ji+Cold+Storage", use_column_width=True)

elif choice == t['k_login']:
    st.subheader(t['k_login'])
    col1, col2 = st.columns(2)
    with col1: km = st.text_input(t['mob'], key="k_mob")
    with col2: ka = st.text_input(t['acc'], type="password", key="k_acc")
    
    if st.button(t['signin_btn']):
        try:
            # ताज़ा डाटा पढ़ना (ttl=0)
            m_df = conn.read(worksheet="Master", ttl=0)
            a_df = conn.read(worksheet="Amad", ttl=0)
            
            # मास्टर शीट में मोबाइल और अकाउंट नंबर से मिलान
            match = m_df[(m_df['Mobile_Number'].astype(str).str.strip() == str(km).strip()) & 
                         (m_df['Account_Number'].astype(str).str.strip() == str(ka).strip())]
            
            if not match.empty:
                farmer_name = match['Name'].iloc[0]
                st.success(f"नमस्ते, {farmer_name} जी!")
                
                # अमद (Amad) शीट में नाम के आधार पर डाटा दिखाना
                f_a = a_df[a_df['Name'].astype(str).str.strip() == str(farmer_name).strip()]
                
                tab1, tab2, tab3 = st.tabs(["आलू स्टॉक (Stock)", "लोन (Loan)", "बारदाना (Bags)"])
                with tab1:
                    if not f_a.empty:
                        # आपकी शीट के नए कॉलम के नाम (Lot_Number, Packets, Type)
                        st.table(f_a[['Date', 'Lot_Number', 'Packets', 'Type']])
                    else:
                        st.write("कोई स्टॉक रिकॉर्ड नहीं मिला।")
                with tab2: st.write("लोन का विवरण यहाँ दिखेगा।")
                with tab3: st.write("बारदाना का विवरण यहाँ दिखेगा।")
            else:
                st.error("रिकॉर्ड नहीं मिला। कृपया सही जानकारी डालें।")
        except Exception as e:
            st.error("डाटा लोड करने में समस्या। शीट के कॉलम चेक करें।")

elif choice == t['a_login']:
    pwd = st.text_input("Admin Password", type="password")
    if pwd == "bihariji123":
        st.success("एडमिन पैनल चालू है")
        # यहाँ आप भविष्य में एंट्री फॉर्म जोड़ सकते हैं
