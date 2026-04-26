import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. पेज की सेटिंग
st.set_page_config(page_title="Shri Bihari Ji Cold Storage", layout="wide")

# 2. कनेक्शन सेटअप
conn = st.connection("gsheets", type=GSheetsConnection)

# 3. भाषा स्विच (Top Corner Design)
col1, col2 = st.columns([8, 2])
with col2:
    lang = st.radio("Language / भाषा", ["English", "Hindi"], horizontal=True, label_visibility="collapsed")

# 4. हेडर (ईमेल और मोबाइल नंबर के साथ)
st.markdown(f"""
    <div style='text-align: center; background-color: #1E3A8A; padding: 25px; border-radius: 10px; color: white;'>
        <h1 style='margin: 0;'>🚜 श्री बिहारी जी कोल्ड स्टोरेज</h1>
        <p style='font-size: 18px; margin: 5px 0;'>उदैतापुर, मनीमऊ, कन्नौज (उत्तर प्रदेश)</p>
        <p style='font-size: 15px; margin: 5px 0;'>📧 shribiharijicoldstorage@gmail.com</p>
        <p style='font-size: 15px; margin: 5px 0;'>📞 9838646586, 9621996103, 7007490379</p>
    </div>
""", unsafe_allow_html=True)

# 5. साइडबार मेन्यू
t_home = "Home" if lang == "English" else "होम"
t_admin = "Admin Login" if lang == "English" else "एडमिन लॉगिन"
t_farmer = "Farmer Login" if lang == "English" else "किसान लॉगिन"

menu = st.sidebar.selectbox("Menu", [t_home, t_admin, t_farmer])

# --- एडमिन लॉगिन ---
if menu == t_admin:
    password = st.sidebar.text_input("Password", type="password")
    if password == "bihariji123":
        task = st.sidebar.radio("Work", ["Registration", "Amad Entry"])
        
        S_MASTER = "Master"
        S_AMAD = "Amad"

        if task == "Registration":
            st.subheader("🆕 नया पंजीकरण")
            m_df = conn.read(worksheet=S_MASTER, ttl=0)
            with st.form("reg_form", clear_on_submit=True):
                n = st.text_input("Name"); fn = st.text_input("Father Name")
                v = st.text_input("Village"); m = st.text_input("Mobile"); ac = st.text_input("Account No")
                if st.form_submit_button("Save"):
                    new_data = pd.DataFrame([{"Name": n, "Father Name": fn, "Village": v, "Mobile Number": m, "Account Number": ac}])
                    conn.create(worksheet=S_MASTER, data=pd.concat([m_df, new_data], ignore_index=True))
                    st.success("Success!")

        elif task == "Amad Entry":
            st.subheader("📦 आमद एंट्री")
            m_df = conn.read(worksheet=S_MASTER, ttl=0)
            a_df = conn.read(worksheet=S_AMAD, ttl=0)
            farmers = (m_df['Name'] + " (" + m_df['Father Name'] + ")").tolist()
            sel_f = st.selectbox("Farmer", [""] + farmers)
            with st.form("amad_form", clear_on_submit=True):
                d = st.date_input("Date", datetime.now()); p = st.number_input("Packets", min_value=1)
                t = st.selectbox("Type", ["Oorja", "Lal", "Safed", "Halland", "Sindoori"])
                if st.form_submit_button("Save Entry") and sel_f != "":
                    row = m_df.iloc[farmers.index(sel_f)]
                    amad_row = pd.DataFrame([{"Date": d.strftime("%d-%m-%Y"), "Packet": p, "Type": t, "Name": row['Name'], "Account Number": row['Account Number']}])
                    conn.create(worksheet=S_AMAD, data=pd.concat([a_df, amad_row], ignore_index=True))
                    st.success("Saved!")

# --- किसान लॉगिन ---
elif menu == t_farmer:
    st.subheader("🌾 किसान भाई अपना विवरण देखें")
    acc_no = st.text_input("अपना अकाउंट नंबर दर्ज करें (Enter Account Number)")
    if acc_no:
        try:
            a_df = conn.read(worksheet="Amad", ttl=0)
            result = a_df[a_df['Account Number'].astype(str) == acc_no]
            if not result.empty:
                st.write(f"नमस्ते, **{result['Name'].iloc[0]}** जी")
                st.dataframe(result[['Date', 'Packet', 'Type']], hide_index=True)
                total_packets = result['Packet'].sum()
                st.metric("कुल पैकेट (Total Packets)", total_packets)
            else:
                st.error("इस अकाउंट नंबर पर कोई डाटा नहीं मिला।")
        except:
            st.error("डाटा लोड करने में समस्या आई।")

else:
    st.info("स्वागत है! कृपया कार्य शुरू करने के लिए मेन्यू से लॉगिन करें।")
