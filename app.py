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
    "search": "Search Farmer..." if lang == "English" else "किसान खोजें...",
    "v_no": "Voucher No." if lang == "English" else "वाउचर नंबर",
    "name": "Name" if lang == "English" else "नाम",
    "fname": "Father's Name" if lang == "English" else "पिता का नाम",
    "vill": "Village" if lang == "English" else "गाँव",
    "date": "Date" if lang == "English" else "तारीख",
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
    st.info("आधुनिक तकनीक और सुरक्षित भंडारण। / Modern Technology & Secure Storage.")
    
    st.markdown("### 📸 Gallery")
    col_img1, col_img2 = st.columns(2)
    with col_img1: st.image("https://via.placeholder.com/600x400.png?text=Building+Photo", caption="Main Building")
    with col_img2: st.image("https://via.placeholder.com/600x400.png?text=Storage+Photo", caption="Storage Area")

elif login_type == t['a_login']:
    pwd = st.sidebar.text_input("Password", type="password")
    if pwd == "bihariji123":
        task = st.sidebar.radio("Select Task", ["New Farmer Registration", "Amad Entry", "Loan Entry", "Bardana Entry"])
        master_df = conn.read(worksheet="Farmers_Master")
        
        if "Registration" in task:
            st.subheader("🆕 Registration")
            with st.form("m_form"):
                m_n = st.text_input(t['name']); m_fn = st.text_input(t['fname']); m_v = st.text_input(t['vill'])
                m_a = st.text_input(t['acc']); m_m = st.text_input(t['mob'])
                if st.form_submit_button(t['save']):
                    new_m = pd.DataFrame([{"Name": m_n, "Father_Name": m_fn, "Village": m_v, "Account_No": m_a, "Mobile": m_m}])
                    conn.update(worksheet="Farmers_Master", data=pd.concat([master_df, new_m], ignore_index=True))
                    st.success(t['success'])
        else:
            st.subheader(f"📝 {task}")
            s_list = (master_df['Name'] + " s/o " + master_df['Father_Name'] + " (" + master_df['Village'] + ")").tolist()
            sel = st.selectbox(t['search'], [""] + s_list)
            with st.form("v_form"):
                f_d = master_df[s_list.index(sel)-1 == master_df.index] if sel else pd.DataFrame()
                v_n = st.text_input(t['v_no']); dt = st.date_input(t['date'], datetime.now())
                nm = st.text_input(t['name'], value=f_d['Name'].iloc[0] if not f_d.empty else "")
                fn = st.text_input(t['fname'], value=f_d['Father_Name'].iloc[0] if not f_d.empty else "")
                ac = f_d['Account_No'].iloc[0] if not f_d.empty else ""; st.info(f"A/c: {ac}")
                vi = st.text_input(t['vill'], value=f_d['Village'].iloc[0] if not f_d.empty else "")
                mb = f_d['Mobile'].iloc[0] if not f_d.empty else ""
                
                if "Amad" in task:
                    lot = st.text_input("Lot No"); pk = st.number_input("Packets", min_value=0)
                elif "Loan" in task:
                    ln = st.number_input("Amount (₹)", min_value=0)
                elif "Bardana" in task:
                    jt = st.number_input("Jute", min_value=0); pl = st.number_input("Plastic", min_value=0); ct = st.number_input("Cost", min_value=0)

                if st.form_submit_button(t['save']):
                    sheet = "Amad" if "Amad" in task else ("Loan" if "Loan" in task else "Bardana")
                    df = conn.read(worksheet=sheet)
                    row = {"Date": dt.strftime("%d-%m-%Y"), "Voucher_No": v_n, "Name": nm, "Father_Name": fn, "Village": vi, "Account_No": ac, "Mobile": mb}
                    if "Amad" in task: row.update({"Lot_No": lot, "Packets": pk})
                    elif "Loan" in task: row.update({"Loan_Amount": ln})
                    elif "Bardana" in task: row.update({"Jute_Bags": jt, "Plastic_Bags": pl, "Total_Bags_Cost": ct})
                    conn.update(worksheet=sheet, data=pd.concat([df, pd.DataFrame([row])], ignore_index=True))
                    st.success(t['success'])

elif login_type == t['k_login']:
    st.subheader(f"👨‍🌾 {t['k_login']}")
    k_m = st.text_input(t['mob']); k_a = st.text_input(t['acc'], type="password")
    
    if st.button(t['signin_btn']):
        a_df = conn.read(worksheet="Amad"); l_df = conn.read(worksheet="Loan"); b_df = conn.read(worksheet="Bardana")
        f_a = a_df[(a_df['Mobile'].astype(str) == str(k_m)) & (a_df['Account_No'].astype(str) == str(k_a))]
        f_l = l_df[(l_df['Mobile'].astype(str) == str(k_m)) & (l_df['Account_No'].astype(str) == str(k_a))]
        f_b = b_df[(b_df['Mobile'].astype(str) == str(k_m)) & (b_df['Account_No'].astype(str) == str(k_a))]
        
        if not f_a.empty or not f_l.empty:
            nm_v = f_a['Name'].iloc[0] if not f_a.empty else f_l['Name'].iloc[0]
            st.success(f"Welcome / स्वागत है, {nm_v} जी!")
            tb1, tb2, tb3 = st.tabs(["Stock", "Loan", "Bags"])
            with tb1: st.dataframe(f_a[['Date', 'Voucher_No', 'Lot_No', 'Packets']])
            with tb2: st.dataframe(f_l[['Date', 'Voucher_No', 'Loan_Amount']])
            with tb3: st.dataframe(f_b[['Date', 'Voucher_No', 'Jute_Bags', 'Plastic_Bags', 'Total_Bags_Cost']])
        else:
            st.error("Invalid Details / गलत जानकारी")
