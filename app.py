import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# पेज सेटिंग
st.set_page_config(page_title="Shri Bihari Ji Cold Storage", layout="wide")

# कनेक्शन
conn = st.connection("gsheets", type=GSheetsConnection)

# हेडर (सिर्फ नाम और पता)
st.markdown(f"""
    <div style='text-align: center; background-color: #1E3A8A; padding: 20px; border-radius: 10px; color: white;'>
        <h1 style='margin: 0;'>🚜 श्री बिहारी जी कोल्ड स्टोरेज</h1>
        <p style='font-size: 18px;'>उदैतापुर, मनीमऊ, कन्नौज (उत्तर प्रदेश)</p>
    </div>
""", unsafe_allow_html=True)

# साइडबार लॉगिन
st.sidebar.title("Menu")
login_type = st.sidebar.selectbox("विकल्प चुनें", ["Home", "Admin Login"])

if login_type == "Admin Login":
    pwd = st.sidebar.text_input("Password", type="password")
    if pwd == "bihariji123":
        task = st.sidebar.radio("कार्य चुनें", ["Registration", "Amad Entry", "Loan Entry"])
        
        # शीट के नाम (जो आपने अब बदल दिए हैं)
        S_MASTER = "Master"
        S_AMAD = "Amad"
        S_LOAN = "Loan"

        if task == "Registration":
            st.subheader("🆕 नया किसान पंजीकरण")
            try:
                master_df = conn.read(worksheet=S_MASTER, ttl=5)
            except:
                master_df = pd.DataFrame(columns=["Name", "Father Name", "Village Name", "Mobile Number", "Account Number"])

            with st.form("reg_form"):
                n = st.text_input("किसान का नाम"); fn = st.text_input("पिता का नाम")
                v = st.text_input("गाँव"); m = st.text_input("मोबाइल नंबर"); ac = st.text_input("अकाउंट नंबर")
                if st.form_submit_button("डाटा सुरक्षित करें"):
                    new_row = pd.DataFrame([{"Name": n, "Father Name": fn, "Village Name": v, "Mobile Number": m, "Account Number": ac}])
                    updated_df = pd.concat([master_df, new_row], ignore_index=True)
                    conn.update(worksheet=S_MASTER, data=updated_df)
                    st.success("सफलतापूर्वक रजिस्टर किया गया!")

        elif task == "Amad Entry":
            st.subheader("📦 आमद (Stock) एंट्री")
            try:
                # डेटा लोड करना
                master_df = conn.read(worksheet=S_MASTER, ttl=5)
                amad_df = conn.read(worksheet=S_AMAD, ttl=5)
                
                # ऑटो लॉट नंबर (Highest + 1)
                max_lot = pd.to_numeric(amad_df['Lot Number'], errors='coerce').max()
                next_lot = int(max_lot + 1) if not pd.isna(max_lot) else 1

                # किसान चुनने के लिए लिस्ट
                s_list = (master_df['Name'] + " s/o " + master_df['Father Name']).tolist()
                sel = st.selectbox("किसान खोजें", [""] + s_list)

                with st.form("amad_form"):
                    dt = st.date_input("तारीख", datetime.now())
                    lot = st.number_input("लॉट नंबर (Lot No.)", value=next_lot)
                    pk = st.number_input("पैकेट की संख्या", min_value=1)
                    tp = st.selectbox("किस्म (Type)", ["Oorja", "Lal", "Safed", "Halland", "Sindoori"])
                    
                    if st.form_submit_button("एंट्री सेव करें") and sel != "":
                        f_idx = s_list.index(sel)
                        f_row = master_df.iloc[f_idx]
                        new_amad = pd.DataFrame([{
                            "Date": dt.strftime("%d-%m-%Y"),
                            "Lot Number": lot,
                            "Packet": pk,
                            "Type": tp,
                            "Name": f_row['Name'],
                            "Father Name": f_row['Father Name'],
                            "Account Number": f_row['Account Number']
                        }])
                        conn.update(worksheet=S_AMAD, data=pd.concat([amad_df, new_amad], ignore_index=True))
                        st.success(f"लॉट नंबर {lot} सुरक्षित कर लिया गया है!")
            except Exception as e:
                st.error("शीट लोड नहीं हो रही। कृपया पक्का करें कि गूगल शीट में टैब का नाम 'Master' और 'Amad' ही है।")

else:
    st.info("स्वागत है! कृपया काम शुरू करने के लिए साइडबार से एडमिन लॉगिन करें।")
