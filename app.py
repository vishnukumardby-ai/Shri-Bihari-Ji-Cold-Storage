import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. पेज सेटअप
st.set_page_config(page_title="Shri Bihari Ji Cold Storage", layout="wide")

# 2. गूगल शीट कनेक्शन
conn = st.connection("gsheets", type=GSheetsConnection)

# --- ऊपर दाईं ओर भाषा का स्विच (Kill Switch) ---
st.markdown('<style>div.row-widget.stRadio > div{flex-direction:row; justify-content: flex-end; padding-top: -50px;}</style>', unsafe_allow_html=True)
lang = st.radio("", ["English", "Hindi"], label_visibility="collapsed")

# 3. मुख्य हेडर (सिर्फ आपकी जानकारी)
st.markdown(f"""
    <div style='text-align: center; background-color: #1E3A8A; padding: 25px; border-radius: 10px; color: white;'>
        <h1 style='margin: 0;'>🚜 श्री बिहारी जी कोल्ड स्टोरेज</h1>
        <p style='font-size: 18px; margin: 5px 0;'>उदैतापुर, मनीमऊ, कन्नौज (उत्तर प्रदेश)</p>
        <p style='font-size: 14px; margin: 2px 0;'>📧 shribiharijicoldstorage@gmail.com</p>
        <p style='font-size: 14px; margin: 2px 0;'>📞 9838646586, 9621996103, 7007490379</p>
    </div>
""", unsafe_allow_html=True)

# 4. साइडबार मेन्यू
t_home = "Home" if lang == "English" else "होम"
t_admin = "Admin Login" if lang == "English" else "एडमिन लॉगिन"
t_farmer = "Farmer Login" if lang == "English" else "किसान लॉगिन"

menu = st.sidebar.selectbox("Main Menu", [t_home, t_admin, t_farmer])

# --- एडमिन सेक्शन (पंजीकरण और आमद) ---
if menu == t_admin:
    password = st.sidebar.text_input("Password", type="password")
    if password == "bihariji123":
        task = st.sidebar.radio("Task", ["Registration", "Amad Entry"])
        
        if task == "Registration":
            st.subheader("🆕 नया किसान पंजीकरण")
            try:
                m_df = conn.read(worksheet="Master", ttl=0)
            except:
                m_df = pd.DataFrame(columns=["Name", "Father Name", "Village", "Mobile Number", "Account Number"])
            
            with st.form("reg_form", clear_on_submit=True):
                n = st.text_input("किसान का नाम"); fn = st.text_input("पिता का नाम")
                v = st.text_input("गाँव"); m = st.text_input("मोबाइल नंबर"); ac = st.text_input("अकाउंट नंबर")
                if st.form_submit_button("सुरक्षित करें"):
                    if n and ac and m:
                        new_row = pd.DataFrame([{"Name": n, "Father Name": fn, "Village": v, "Mobile Number": m, "Account Number": ac}])
                        conn.create(worksheet="Master", data=pd.concat([m_df, new_row], ignore_index=True))
                        st.success("डाटा सुरक्षित हो गया!")
                        st.cache_data.clear()
                    else:
                        st.error("नाम, मोबाइल और अकाउंट नंबर भरना अनिवार्य है।")

        elif task == "Amad Entry":
            st.subheader("📦 नई आमद (Stock) एंट्री")
            try:
                m_df = conn.read(worksheet="Master", ttl=0)
                a_df = conn.read(worksheet="Amad", ttl=0)
                farmers = (m_df['Name'] + " (" + m_df['Father Name'] + ")").tolist()
                sel_f = st.selectbox("किसान चुनें", [""] + farmers)
                
                with st.form("amad_form", clear_on_submit=True):
                    d = st.date_input("तारीख", datetime.now()); p = st.number_input("पैकेट", min_value=1)
                    t = st.selectbox("किस्म", ["Oorja", "Lal", "Safed", "Halland", "Sindoori"])
                    if st.form_submit_button("एंट्री सेव करें") and sel_f != "":
                        row_f = m_df.iloc[farmers.index(sel_f)]
                        new_entry = pd.DataFrame([{
                            "Date": d.strftime("%d-%m-%Y"), "Packet": p, "Type": t,
                            "Name": row_f['Name'], "Account Number": row_f['Account Number'],
                            "Mobile Number": row_f['Mobile Number']
                        }])
                        conn.create(worksheet="Amad", data=pd.concat([a_df, new_entry], ignore_index=True))
                        st.success("आमद सुरक्षित हो गई!")
                        st.cache_data.clear()
            except:
                st.error("डेटा लोड नहीं हो सका।")

# --- किसान लॉगिन (Account + Mobile दोनों अनिवार्य) ---
elif menu == t_farmer:
    st.subheader("🌾 किसान लॉगिन / Farmer View")
    
    col1, col2 = st.columns(2)
    with col1:
        f_acc = st.text_input("अकाउंट नंबर (Account No.)")
    with col2:
        f_mob = st.text_input("मोबाइल नंबर (Mobile No.)")
    
    if st.button("विवरण देखें / View Details"):
        if f_acc and f_mob:
            try:
                amad_df = conn.read(worksheet="Amad", ttl=0)
                # दोनों शर्तों का मिलान अनिवार्य है
                user_data = amad_df[
                    (amad_df['Account Number'].astype(str) == str(f_acc)) & 
                    (amad_df['Mobile Number'].astype(str) == str(f_mob))
                ]
                
                if not user_data.empty:
                    st.write(f"नमस्ते, **{user_data['Name'].iloc[0]}** जी")
                    st.table(user_data[['Date', 'Packet', 'Type']])
                    st.metric("कुल जमा पैकेट", user_data['Packet'].sum())
                else:
                    st.error("अकाउंट और मोबाइल नंबर का मिलान नहीं हुआ। कृपया दोबारा जांचें।")
            except:
                st.error("अभी कोई डेटा उपलब्ध नहीं है।")
        else:
            st.warning("कृपया अकाउंट और मोबाइल नंबर दोनों भरें।")

else:
    # होम पेज खाली रहेगा जैसा आपने कहा था
    st.empty()
