import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import urllib.parse

# वेबसाइट सेटिंग
st.set_page_config(page_title="Shri Bihari Ji Cold Storage", layout="wide")

# कनेक्शन
conn = st.connection("gsheets", type=GSheetsConnection)

# हेडर
st.markdown(f"""
    <div style='text-align: center; background-color: #1E3A8A; padding: 20px; border-radius: 10px; color: white;'>
        <h1 style='margin: 0;'>🚜 श्री बिहारी जी कोल्ड स्टोरेज</h1>
        <p style='font-size: 18px;'>उदैतापुर, मनीमऊ, कन्नौज (उत्तर प्रदेश)</p>
    </div>
""", unsafe_allow_html=True)

# साइडबार
login_type = st.sidebar.selectbox("Menu", ["Home Page", "Farmer Login", "Admin Login"])

if login_type == "Admin Login":
    pwd = st.sidebar.text_input("Password", type="password")
    if pwd == "bihariji123":
        task = st.sidebar.radio("Task", ["Registration", "Amad Entry", "Loan Entry", "Bardana Entry"])
        
        # URL सुरक्षित तरीके से शीट पढ़ना (Error Fix)
        def get_data(sheet_name):
            return conn.read(worksheet=sheet_name, ttl=10)

        master_df = get_data("Master List")
        
        if task == "Registration":
            st.subheader("🆕 New Farmer Registration")
            with st.form("reg_form"):
                n = st.text_input("नाम (Name)"); fn = st.text_input("पिता का नाम (Father Name)")
                v = st.text_input("गाँव (Village)"); m = st.text_input("Mobile"); ac = st.text_input("Account No")
                if st.form_submit_button("सुरक्षित करें"):
                    new_row = pd.DataFrame([{"Name": n, "Father Name": fn, "Village Name": v, "Mobile Number": m, "Account Number": ac}])
                    conn.update(worksheet="Master List", data=pd.concat([master_df, new_row], ignore_index=True))
                    st.success("डाटा सुरक्षित हो गया!")

        elif task == "Amad Entry":
            st.subheader("📦 Amad Entry")
            amad_df = get_data("Amad")
            next_lot = int(pd.to_numeric(amad_df['Lot Number'], errors='coerce').max() + 1) if not amad_df.empty else 1
            
            s_list = (master_df['Name'] + " s/o " + master_df['Father Name']).tolist()
            sel = st.selectbox("Search Farmer", [""] + s_list)
            
            with st.form("amad_form"):
                dt = st.date_input("Date", datetime.now()); lot = st.number_input("Lot Number", value=next_lot)
                pk = st.number_input("Packets", min_value=1); tp = st.selectbox("Type", ["Oorja", "Lal", "Safed", "Halland", "Sindoori"])
                if st.form_submit_button("Save"):
                    f_row = master_df.iloc[s_list.index(sel)-1]
                    new_data = pd.DataFrame([{"Date": dt.strftime("%d-%m-%Y"), "Lot Number": lot, "Packet": pk, "Type": tp, "Name": f_row['Name'], "Account Number": f_row['Account Number']}])
                    conn.update(worksheet="Amad", data=pd.concat([amad_df, new_data], ignore_index=True))
                    st.success("Success!")

elif login_type == "Farmer Login":
    st.info("किसान भाई अपना विवरण यहाँ देख सकेंगे।")
else:
    st.write("कृपया एडमिन लॉगिन का उपयोग करें।")
