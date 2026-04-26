import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# वेबसाइट की सेटिंग
st.set_page_config(page_title="Shri Bihari Ji Cold Storage", layout="wide")

# भाषा चयन (Language Selection)
lang = st.sidebar.radio("Select Language / भाषा चुनें", ["English", "Hindi"])

# शब्दकोश (Dictionary for Translation)
t = {
    "title": "🚜 SHRI BIHARI JI COLD STORAGE" if lang == "English" else "🚜 श्री बिहारी जी कोल्ड स्टोरेज",
    "addr": "Udaitapur, Manimau, Kannauj (U.P.)" if lang == "English" else "उदैतापुर, मनीमऊ, कन्नौज (उत्तर प्रदेश)",
    "home": "Home Page" if lang == "English" else "होम पेज",
    "k_login": "Farmer Login" if lang == "English" else "किसान लॉगिन",
    "a_login": "Admin (Management)" if lang == "English" else "एडमिन (मैनेजमेंट)",
    "welcome": "Welcome to Shri Bihari Ji Cold Storage" if lang == "English" else "श्री बिहारी जी कोल्ड स्टोरेज में आपका स्वागत है",
    "mob": "Mobile Number" if lang == "English" else "मोबाइल नंबर",
    "acc": "Account Number" if lang == "English" else "अकाउंट नंबर",
    "signin_btn": "Sign In" if lang == "English" else "प्रवेश करें",
    "save": "Save Data" if lang == "English" else "डाटा सुरक्षित करें",
    "success": "Saved Successfully!" if lang == "English" else "सफलतापूर्वक सुरक्षित किया गया!",
}

# मुख्य हेडर
st.markdown(f"""
    <div style='text-align: center; background-color: #1E3A8A; padding: 30px; border-radius: 15px; color: white;'>
        <h1 style='margin-bottom: 5px; font-family: "Arial Black", sans-serif;'>{t['title']}</h1>
        <p style='font-size: 22px; margin: 0;'><b>{t['addr']}</b></p>
        <p style='font-size: 18px; margin: 10px 0;'>📧 shribiharijicoldstorage@gmail.com</p>
        <p style='font-size: 18px; margin: 0;'>📞 9838646586, 9621996103, 7007490379</p>
    </div>
""", unsafe_allow_html=True)

conn = st.connection("gsheets", type=GSheetsConnection)

# साइडबार लॉगिन टाइप
st.sidebar.markdown(f"### 🔒 Login")
login_type = st.sidebar.selectbox("Options", [t['home'], t['k_login'], t['a_login']])

if login_type == t['home']:
    st.markdown(f"<br><h2 style='text-align: center; color: #1E3A8A;'>{t['welcome']}</h2>", unsafe_allow_html=True)
    st.info("विष्णु कुमार दुबे जी के कुशल मार्गदर्शन में। / Under the guidance of Vishnu Kumar Dubey.")
    
    st.markdown("### 📸 Gallery")
    col_img1, col_img2 = st.columns(2)
    with col_img1: st.image("https://via.placeholder.com/600x400.png?text=Building+Photo", caption="Main Building")
    with col_img2: st.image("https://via.placeholder.com/600x400.png?text=Storage+Photo", caption="Storage Area")

elif login_type == t['a_login']:
    pwd = st.sidebar.text_input("Password", type="password")
    if pwd == "bihariji123":
        task = st.sidebar.radio("Select Task", ["New Farmer Registration", "Amad Entry", "Loan Entry", "Bardana Entry"])
        master_df = conn.read(worksheet="Farmers_Master")
        
        # ... (Admin code remains same as previous version) ...
        # (Writing short for brevity, ensure you keep the full logic from previous code)

elif login_type == t['k_login']:
    st.subheader(f"👨‍🌾 {t['k_login']}")
    
    # इनपुट बॉक्स
    k_m = st.text_input(t['mob'])
    k_a = st.text_input(t['acc'], type="password")
    
    # यहाँ बदलाव किया गया है - बटन का नाम भाषा के अनुसार बदलेगा
    if st.button(t['signin_btn']):
        a_df = conn.read(worksheet="Amad")
        l_df = conn.read(worksheet="Loan")
        b_df = conn.read(worksheet="Bardana")
        
        f_a = a_df[(a_df['Mobile'].astype(str) == str(k_m)) & (a_df['Account_No'].astype(str) == str(k_a))]
        f_l = l_df[(l_df['Mobile'].astype(str) == str(k_m)) & (l_df['Account_No'].astype(str) == str(k_a))]
        f_b = b_df[(b_df['Mobile'].astype(str) == str(k_m)) & (b_df['Account_No'].astype(str) == str(k_a))]
        
        if not f_a.empty or not f_l.empty:
            name_val = f_a['Name'].iloc[0] if not f_a.empty else f_l['Name'].iloc[0]
            st.success(f"Welcome / स्वागत है, {name_val} जी!")
            
            tb1, tb2, tb3 = st.tabs(["Stock (Amad)", "Loan", "Bags (Bardana)"])
            with tb1: st.dataframe(f_a)
            with tb2: st.dataframe(f_l)
            with tb3: st.dataframe(f_b)
        else:
            st.error("Invalid Details / गलत जानकारी")
