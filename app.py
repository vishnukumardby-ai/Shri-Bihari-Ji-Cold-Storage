import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# पेज सेटिंग
st.set_page_config(page_title="Shri Bihari Ji Cold Storage", layout="wide")

# भाषा चयन
lang = st.sidebar.radio("Language / भाषा", ["English", "Hindi"])

t = {
    "title": "🚜 SHRI BIHARI JI COLD STORAGE" if lang == "English" else "🚜 श्री बिहारी जी कोल्ड स्टोरेज",
    "addr": "Udaitapur, Manimau, Kannauj" if lang == "English" else "उदैतापुर, मानीमऊ, कन्नौज",
    "mob": "Mobile Number" if lang == "English" else "मोबाइल नंबर",
    "acc": "Account Number" if lang == "English" else "अकाउंट नंबर",
    "signin": "Sign In" if lang == "English" else "प्रवेश करें",
}

# हेडर
st.markdown(f"""
    <div style='text-align: center; background-color: #1E3A8A; padding: 20px; border-radius: 15px; color: white;'>
        <h1 style='margin: 0;'>{t['title']}</h1>
        <h3 style='margin: 5px;'><b>{t['addr']}</b></h3>
    </div>
""", unsafe_allow_html=True)

conn = st.connection("gsheets", type=GSheetsConnection)

choice = st.radio("", ["Home", "Farmer Login", "Admin"], horizontal=True)

if choice == "Farmer Login":
    col1, col2 = st.columns(2)
    with col1: km = st.text_input(t['mob'])
    with col2: ka = st.text_input(t['acc'], type="password")
    
    if st.button(t['signin']):
        try:
            m_df = conn.read(worksheet="Master", ttl=0)
            # यहाँ हमने .str.strip() लगाया है ताकि फालतू स्पेस से एरर न आए
            m_df.columns = m_df.columns.str.strip()
            
            match = m_df[(m_df['Mobile_Number'].astype(str).str.strip() == str(km).strip()) & 
                         (m_df['Account_Number'].astype(str).str.strip() == str(ka).strip())]
            
            if not match.empty:
                f_name = match['Name'].iloc[0]
                st.success(f"नमस्ते, {f_name} जी!")
                
                # हिसाब दिखाना
                tab1, tab2 = st.tabs(["Stock", "Loan"])
                with tab1:
                    try:
                        a_df = conn.read(worksheet="Amad", ttl=0)
                        a_df.columns = a_df.columns.str.strip()
                        f_a = a_df[a_df['Account_Number'].astype(str).str.strip() == str(ka).strip()]
                        st.table(f_a) if not f_a.empty else st.write("रिकॉर्ड नहीं है।")
                    except: st.error("Amad शीट में Account_Number कॉलम नहीं मिला।")
            else:
                st.error("गलत विवरण! कृपया सही मोबाइल और अकाउंट नंबर डालें।")
        except Exception as e:
            st.error("कनेक्शन में समस्या! कृपया अपनी गूगल शीट के कॉलम चेक करें।")

elif choice == "Home":
    st.info("स्वागत है! अपना हिसाब देखने के लिए Farmer Login पर क्लिक करें।")
