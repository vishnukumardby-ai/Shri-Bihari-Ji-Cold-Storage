import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# पेज सेटिंग
st.set_page_config(page_title="Shri Bihari Ji Cold Storage", layout="wide")

# भाषा चयन
lang = st.sidebar.radio("Select Language / भाषा चुनें", ["English", "Hindi"])

# शब्दकोश (Translation Dictionary)
t = {
    "title": "🚜 SHRI BIHARI JI COLD STORAGE" if lang == "English" else "🚜 श्री बिहारी जी कोल्ड स्टोरेज",
    "addr": "Udaitapur, Manimau, Kannauj (U.P.)" if lang == "English" else "उदैतापुर, मानीमऊ, कन्नौज (उत्तर प्रदेश)",
    "home": "Home" if lang == "English" else "मुख्य पेज",
    "k_login": "Farmer Login" if lang == "English" else "किसान लॉगिन",
    "a_login": "Admin" if lang == "English" else "एडमिन",
    "mob": "Mobile Number" if lang == "English" else "मोबाइल नंबर",
    "acc": "Account Number" if lang == "English" else "अकाउंट नंबर",
    "signin_btn": "Sign In" if lang == "English" else "प्रवेश करें",
    "save": "Save Data" if lang == "English" else "सुरक्षित करें",
}

# मुख्य हेडर डिजाइन (यहाँ मानीमऊ को अपडेट किया गया है)
st.markdown(f"""
    <div style='text-align: center; background-color: #1E3A8A; padding: 25px; border-radius: 15px; color: white;'>
        <h1 style='margin: 0; font-family: "Arial Black", sans-serif;'>{t['title']}</h1>
        <p style='font-size: 20px; margin: 5px;'><b>{t['addr']}</b></p>
        <p style='font-size: 15px; margin: 0;'>📞 9838646586, 9621996103, 7007490379</p>
    </div>
    <br>
""", unsafe_allow_html=True)

conn = st.connection("gsheets", type=GSheetsConnection)

# मुख्य विकल्प
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
            # ttl=0 का मतलब है कि हर बार नयी जानकारी लोड होगी
            m_df = conn.read(worksheet="Master", ttl=0)
            a_df = conn.read(worksheet="Amad", ttl=0)
            l_df = conn.read(worksheet="Loan", ttl=0)
            b_df = conn.read(worksheet="Bardana", ttl=0)
            
            # Master शीट में Mobile_Number और Account_Number से मिलान
            match = m_df[(m_df['Mobile_Number'].astype(str).str.strip() == str(km).strip()) & 
                         (m_df['Account_Number'].astype(str).str.strip() == str(ka).strip())]
            
            if not match.empty:
                name = match['Name'].iloc[0]
                st.success(f"नमस्ते, {name} जी!")
                
                # Account_Number के आधार पर बाकी डाटा फ़िल्टर करना
                f_a = a_df[a_df['Account_Number'].astype(str).str.strip() == str(ka).strip()]
                f_l = l_df[l_df['Account_Number'].astype(str).str.strip() == str(ka).strip()]
                f_b = b_df[b_df['Account_Number'].astype(str).str.strip() == str(ka).strip()]
                
                t1, t2, t3 = st.tabs(["आलू स्टॉक", "लोन विवरण", "बारदाना"])
                with t1: st.table(f_a) if not f_a.empty else st.write("कोई स्टॉक रिकॉर्ड नहीं मिला।")
                with t2: st.table(f_l) if not f_l.empty else st.write("कोई लोन रिकॉर्ड नहीं मिला।")
                with t3: st.table(f_b) if not f_b.empty else st.write("कोई बारदाना रिकॉर्ड नहीं मिला।")
            else:
                st.error("Invalid Details / रिकॉर्ड नहीं मिला। कृपया सही मोबाइल और अकाउंट नंबर डालें।")
        except Exception as e:
            st.error("डाटा कनेक्शन में समस्या।")

elif choice == t['a_login']:
    pwd = st.text_input("Admin Password", type="password")
    if pwd == "bihariji123":
        task = st.selectbox("काम चुनें", ["New Farmer Registration", "Amad Entry", "Loan Entry", "Bardana Entry"])
        m_df = conn.read(worksheet="Master", ttl=0)
        
        if "Registration" in task:
            with st.form("reg_form"):
                n = st.text_input("Name"); fn = st.text_input("Father Name"); v = st.text_input("Village")
                mn = st.text_input("Mobile_Number"); an = st.text_input("Account_Number")
                if st.form_submit_button(t['save']):
                    new = pd.DataFrame([{"Name": n, "Father_Name": fn, "Village": v, "Mobile_Number": mn, "Account_Number": an}])
                    conn.update(worksheet="Master", data=pd.concat([m_df, new], ignore_index=True))
                    st.success("किसान सुरक्षित हो गया!")
