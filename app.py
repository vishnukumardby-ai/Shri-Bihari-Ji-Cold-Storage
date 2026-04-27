import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Page settings
st.set_page_config(page_title="Shri Bihari Ji Cold Storage", layout="wide")

# Header
st.markdown("""
    <div style='text-align: center; background-color: #1E3A8A; padding: 20px; border-radius: 15px; color: white;'>
        <h1 style='margin: 0;'>🚜 श्री बिहारी जी कोल्ड स्टोरेज</h1>
        <h3 style='margin: 5px;'><b>उदैतापुर, मानीमऊ, कन्नौज (U.P.)</b></h3>
    </div>
    <br>
""", unsafe_allow_html=True)

# Connection
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    st.error("Sheet se connection nahi ho pa raha.")

choice = st.sidebar.radio("Main Menu", ["Home", "Farmer Login"])

if choice == "Farmer Login":
    st.subheader("किसान लॉगिन")
    km = st.text_input("अपना रजिस्टर्ड मोबाइल नंबर डालें")
    
    if st.button("विवरण देखें"):
        if not km:
            st.warning("कृपया मोबाइल नंबर भरें।")
        else:
            try:
                # Aapki nayi settings ke hisaab se panno ke naam:
                # Sheet1 = Master, Sheet2 = Amad, Sheet3 = Loan, Sheet4 = Bardana
                
                # 1. Master (Sheet1) se kisan ka naam dhoondhna
                m_df = conn.read(worksheet="Sheet1", ttl=0)
                m_df.columns = m_df.columns.str.strip()
                
                match = m_df[m_df['Mobile'].astype(str).str.strip() == str(km).strip()]
                
                if not match.empty:
                    f_name = match['Name'].iloc[0]
                    st.success(f"नमस्ते, {f_name} जी!")
                    
                    tab1, tab2, tab3 = st.tabs(["आलू स्टॉक (Amad)", "लोन (Loan)", "बारदाना (Bardana)"])
                    
                    with tab1: # Amad (Sheet2)
                        try:
                            df2 = conn.read(worksheet="Sheet2", ttl=0)
                            df2.columns = df2.columns.str.strip()
                            res = df2[df2['Mobile'].astype(str).str.strip() == str(km).strip()]
                            st.table(res) if not res.empty else st.info("स्टॉक रिकॉर्ड नहीं मिला।")
                        except: st.error("Sheet2 (Amad) load nahi ho rahi.")

                    with tab2: # Loan (Sheet3)
                        try:
                            df3 = conn.read(worksheet="Sheet3", ttl=0)
                            df3.columns = df3.columns.str.strip()
                            res_l = df3[df3['Mobile'].astype(str).str.strip() == str(km).strip()]
                            st.table(res_l) if not res_l.empty else st.info("लोन का रिकॉर्ड नहीं है।")
                        except: st.info("Sheet3 (Loan) khali hai.")

                    with tab3: # Bardana (Sheet4)
                        try:
                            df4 = conn.read(worksheet="Sheet4", ttl=0)
                            df4.columns = df4.columns.str.strip()
                            res_b = df4[df4['Mobile'].astype(str).str.strip() == str(km).strip()]
                            st.table(res_b) if not res_b.empty else st.info("बारदाना का रिकॉर्ड नहीं है।")
                        except: st.info("Sheet4 (Bardana) khali hai.")
                else:
                    st.error("यह मोबाइल नंबर हमारे रिकॉर्ड में नहीं है।")
            except Exception as e:
                st.error("Sheet1 milne mein samasya hai. Ek baar Reboot karke dekhein.")
else:
    st.info("स्वागत है! अपना हिसाब देखने के लिए 'Farmer Login' चुनें।")
