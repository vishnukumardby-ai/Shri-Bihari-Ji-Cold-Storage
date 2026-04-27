import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# पेज सेटिंग
st.set_page_config(page_title="Shri Bihari Ji Cold Storage", layout="wide")

# हेडर
st.markdown("""
    <div style='text-align: center; background-color: #1E3A8A; padding: 20px; border-radius: 15px; color: white;'>
        <h1 style='margin: 0;'>🚜 श्री बिहारी जी कोल्ड स्टोरेज</h1>
        <h3 style='margin: 5px;'><b>उदैतापुर, मानीमऊ, कन्नौज (U.P.)</b></h3>
    </div>
    <br>
""", unsafe_allow_html=True)

# कनेक्शन
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    st.error("शीट से कनेक्शन नहीं हो पा रहा।")

choice = st.sidebar.radio("Main Menu", ["Home", "Farmer Login"])

if choice == "Farmer Login":
    st.subheader("किसान लॉगिन")
    km = st.text_input("अपना रजिस्टर्ड मोबाइल नंबर डालें")
    
    if st.button("विवरण देखें"):
        if not km:
            st.warning("कृपया मोबाइल नंबर भरें।")
        else:
            try:
                # 1. 'Master' पन्ने से किसान का नाम ढूँढना
                m_df = conn.read(worksheet="Master", ttl=0)
                m_df.columns = m_df.columns.str.strip()
                
                # 'Mobile' कॉलम से मैच करना
                match = m_df[m_df['Mobile'].astype(str).str.strip() == str(km).strip()]
                
                if not match.empty:
                    f_name = match['Name'].iloc[0]
                    st.success(f"नमस्ते, {f_name} जी!")
                    
                    # अलग-अलग पन्नों के लिए बटन (Tabs)
                    tab1, tab2, tab3 = st.tabs(["आलू स्टॉक (Amad)", "लोन (Loan)", "बारदाना (Bardana)"])
                    
                    with tab1:
                        try:
                            a_df = conn.read(worksheet="Amad", ttl=0)
                            a_df.columns = a_df.columns.str.strip()
                            res = a_df[a_df['Mobile'].astype(str).str.strip() == str(km).strip()]
                            st.table(res) if not res.empty else st.info("स्टॉक का कोई रिकॉर्ड नहीं मिला।")
                        except: st.error("Amad पन्ने में गड़बड़ है।")

                    with tab2:
                        try:
                            l_df = conn.read(worksheet="Loan", ttl=0)
                            l_df.columns = l_df.columns.str.strip()
                            res_l = l_df[l_df['Mobile'].astype(str).str.strip() == str(km).strip()]
                            st.table(res_l) if not res_l.empty else st.info("लोन का कोई रिकॉर्ड नहीं है।")
                        except: st.info("Loan पन्ना अभी खाली है।")

                    with tab3:
                        try:
                            b_df = conn.read(worksheet="Bardana", ttl=0)
                            b_df.columns = b_df.columns.str.strip()
                            res_b = b_df[b_df['Mobile'].astype(str).str.strip() == str(km).strip()]
                            st.table(res_b) if not res_b.empty else st.info("बारदाना का कोई रिकॉर्ड नहीं है।")
                        except: st.info("Bardana पन्ना अभी खाली है।")
                else:
                    st.error("यह मोबाइल नंबर हमारे रिकॉर्ड में नहीं है।")
            except Exception as e:
                st.error("शीट पढ़ने में समस्या है। पक्का करें कि मास्टर पन्ने का नाम 'Master' ही है।")
else:
    st.info("स्वागत है! अपना हिसाब देखने के लिए 'Farmer Login' चुनें।")
