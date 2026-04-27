import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# वेबसाइट की सेटिंग
st.set_page_config(page_title="Shri Bihari Ji Cold Storage", layout="wide")

# भाषा चयन (Language Selection) - केवल भाषा साइडबार में रखी है
lang = st.sidebar.radio("Select Language / भाषा चुनें", ["English", "Hindi"])

# शब्दकोश
t = {
    "title": "🚜 SHRI BIHARI JI COLD STORAGE" if lang == "English" else "🚜 श्री बिहारी जी कोल्ड स्टोरेज",
    "addr": "Udaitapur, Manimau, Kannauj (U.P.)" if lang == "English" else "उदैतापुर, मनीमऊ, कन्नौज (उत्तर प्रदेश)",
    "home": "Home" if lang == "English" else "मुख्य पेज",
    "k_login": "Farmer Login" if lang == "English" else "किसान लॉगिन",
    "a_login": "Admin" if lang == "English" else "एडमिन",
    "mob": "Mobile Number" if lang == "English" else "मोबाइल नंबर",
    "acc": "Account Number" if lang == "English" else "अकाउंट नंबर",
    "signin_btn": "Sign In" if lang == "English" else "प्रवेश करें",
    "save": "Save Data" if lang == "English" else "सुरक्षित करें",
    "success": "Saved!" if lang == "English" else "सुरक्षित हो गया!",
}

# मुख्य हेडर
st.markdown(f"""
    <div style='text-align: center; background-color: #1E3A8A; padding: 25px; border-radius: 15px; color: white;'>
        <h1 style='margin: 0; font-family: "Arial Black", sans-serif;'>{t['title']}</h1>
        <p style='font-size: 18px; margin: 5px;'><b>{t['addr']}</b></p>
        <p style='font-size: 14px; margin: 0;'>📞 9838646586, 9621996103</p>
    </div>
    <br>
""", unsafe_allow_html=True)

conn = st.connection("gsheets", type=GSheetsConnection)

# मुख्य पेज पर बड़े टैब/बटन
choice = st.radio("", [t['home'], t['k_login'], t['a_login']], horizontal=True)

st.markdown("---")

if choice == t['home']:
    st.markdown(f"### {t['home']}")
    st.info("आधुनिक तकनीक और सुरक्षित भंडारण। / Modern Technology & Secure Storage.")
    col1, col2 = st.columns(2)
    with col1: st.image("https://via.placeholder.com/600x400.png?text=Building", caption="Main Building")
    with col2: st.image("https://via.placeholder.com/600x400.png?text=Storage", caption="Storage Area")

elif choice == t['a_login']:
    pwd = st.text_input("Admin Password", type="password")
    if pwd == "bihariji123":
        task = st.selectbox("Select Work", ["New Farmer Registration", "Amad Entry", "Loan Entry", "Bardana Entry"])
        master_df = conn.read(worksheet="Farmers_Master")
        
        if "Registration" in task:
            with st.form("m_form"):
                n = st.text_input("Name"); fn = st.text_input("Father Name"); v = st.text_input("Village")
                a = st.text_input("Account No"); m = st.text_input("Mobile")
                if st.form_submit_button(t['save']):
                    new = pd.DataFrame([{"Name": n, "Father_Name": fn, "Village": v, "Account_No": a, "Mobile": m}])
                    conn.update(worksheet="Farmers_Master", data=pd.concat([master_df, new], ignore_index=True))
                    st.success(t['success'])
        else:
            s_list = (master_df['Name'] + " s/o " + master_df['Father_Name'] + " (" + master_df['Village'] + ")").tolist()
            sel = st.selectbox("Search Farmer", [""] + s_list)
            if sel:
                with st.form("v_form"):
                    f_d = master_df[s_list.index(sel)-1 == master_df.index]
                    v_n = st.text_input("Voucher No"); dt = st.date_input("Date", datetime.now())
                    if "Amad" in task:
                        lot = st.text_input("Lot No"); pk = st.number_input("Packets", min_value=0)
                    elif "Loan" in task:
                        ln = st.number_input("Loan Amount", min_value=0)
                    elif "Bardana" in task:
                        jt = st.number_input("Jute", 0); pl = st.number_input("Plastic", 0); ct = st.number_input("Total Cost", 0)
                    
                    if st.form_submit_button(t['save']):
                        sh = "Amad" if "Amad" in task else ("Loan" if "Loan" in task else "Bardana")
                        df = conn.read(worksheet=sh)
                        row = {"Date": dt.strftime("%d-%m-%Y"), "Voucher_No": v_n, "Name": f_d['Name'].iloc[0], "Account_No": f_d['Account_No'].iloc[0], "Mobile": f_d['Mobile'].iloc[0]}
                        if "Amad" in task: row.update({"Lot_No": lot, "Packets": pk})
                        elif "Loan" in task: row.update({"Loan_Amount": ln})
                        elif "Bardana" in task: row.update({"Jute_Bags": jt, "Plastic_Bags": pl, "Total_Bags_Cost": ct})
                        conn.update(worksheet=sh, data=pd.concat([df, pd.DataFrame([row])], ignore_index=True))
                        st.success(t['success'])

elif choice == t['k_login']:
    st.subheader(t['k_login'])
    col1, col2 = st.columns(2)
    with col1: km = st.text_input(t['mob'])
    with col2: ka = st.text_input(t['acc'], type="password")
    
    if st.button(t['signin_btn']):
        a_df = conn.read(worksheet="Amad"); l_df = conn.read(worksheet="Loan"); b_df = conn.read(worksheet="Bardana")
        f_a = a_df[(a_df['Mobile'].astype(str) == str(km)) & (a_df['Account_No'].astype(str) == str(ka))]
        f_l = l_df[(l_df['Mobile'].astype(str) == str(km)) & (l_df['Account_No'].astype(str) == str(ka))]
        f_b = b_df[(b_df['Mobile'].astype(str) == str(km)) & (b_df['Account_No'].astype(str) == str(ka))]
        
        if not f_a.empty or not f_l.empty:
            st.success(f"Welcome, {f_a['Name'].iloc[0] if not f_a.empty else f_l['Name'].iloc[0]}!")
            t1, t2, t3 = st.tabs(["Stock", "Loan", "Bardana"])
            with t1: st.dataframe(f_a)
            with t2: st.dataframe(f_l)
            with t3: st.dataframe(f_b)
        else: st.error("Record Not Found / रिकॉर्ड नहीं मिला")
