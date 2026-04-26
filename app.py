import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. पेज की सेटिंग
st.set_page_config(page_title="Shri Bihari Ji Cold Storage", layout="wide")

# 2. कनेक्शन सेटअप
conn = st.connection("gsheets", type=GSheetsConnection)

# 3. हेडर (ईमेल और मोबाइल नंबर के साथ, बिना वेलकम मैसेज के)
st.markdown(f"""
    <div style='text-align: center; background-color: #1E3A8A; padding: 25px; border-radius: 10px; color: white;'>
        <h1 style='margin: 0;'>🚜 श्री बिहारी जी कोल्ड स्टोरेज</h1>
        <p style='font-size: 18px; margin: 5px 0;'>उदैतापुर, मनीमऊ, कन्नौज (उत्तर प्रदेश)</p>
        <p style='font-size: 15px; margin: 5px 0;'>📧 shribiharijicoldstorage@gmail.com</p>
        <p style='font-size: 15px; margin: 5px 0;'>📞 9838646586, 9621996103, 7007490379</p>
    </div>
""", unsafe_allow_html=True)

# 4. साइडबार मेन्यू
menu = st.sidebar.selectbox("Main Menu", ["Home", "Admin Login"])

if menu == "Admin Login":
    password = st.sidebar.text_input("Password", type="password")
    if password == "bihariji123":
        task = st.sidebar.radio("Select Task", ["Registration", "Amad Entry"])
        
        # शीट के नाम
        S_MASTER = "Master"
        S_AMAD = "Amad"

        # --- किसान पंजीकरण ---
        if task == "Registration":
            st.subheader("🆕 नया किसान पंजीकरण")
            try:
                m_df = conn.read(worksheet=S_MASTER, ttl=0)
            except:
                m_df = pd.DataFrame(columns=["Name", "Father Name", "Village", "Mobile Number", "Account Number"])

            with st.form("reg_form", clear_on_submit=True):
                n = st.text_input("किसान का नाम"); fn = st.text_input("पिता का नाम")
                v = st.text_input("गाँव"); m = st.text_input("मोबाइल"); ac = st.text_input("अकाउंट नंबर")
                
                if st.form_submit_button("सुरक्षित करें"):
                    if n and ac:
                        new_data = pd.DataFrame([{"Name": n, "Father Name": fn, "Village": v, "Mobile Number": m, "Account Number": ac}])
                        updated_df = pd.concat([m_df, new_data], ignore_index=True)
                        # एरर से बचने के लिए create का इस्तेमाल
                        conn.create(worksheet=S_MASTER, data=updated_df)
                        st.success("डाटा सुरक्षित हो गया!")
                        st.cache_data.clear()

        # --- आमद एंट्री ---
        elif task == "Amad Entry":
            st.subheader("📦 नई आमद एंट्री")
            try:
                m_df = conn.read(worksheet=S_MASTER, ttl=0)
                a_df = conn.read(worksheet=S_AMAD, ttl=0)

                # ऑटो लॉट नंबर
                max_l = pd.to_numeric(a_df['Lot Number'], errors='coerce').max()
                next_l = int(max_l + 1) if not pd.isna(max_l) else 1

                farmers = (m_df['Name'] + " (" + m_df['Father Name'] + ")").tolist()
                sel_f = st.selectbox("किसान चुनें", [""] + farmers)

                with st.form("amad_form", clear_on_submit=True):
                    d = st.date_input("तारीख", datetime.now()); l = st.number_input("लॉट नंबर", value=next_l)
                    p = st.number_input("पैकेट", min_value=1); t = st.selectbox("किस्म", ["Oorja", "Lal", "Safed", "Halland", "Sindoori"])
                    
                    if st.form_submit_button("सेव करें") and sel_f != "":
                        row = m_df.iloc[farmers.index(sel_f)]
                        amad_row = pd.DataFrame([{
                            "Date": d.strftime("%d-%m-%Y"), "Lot Number": l, "Packet": p, "Type": t,
                            "Name": row['Name'], "Account Number": row['Account Number']
                        }])
                        conn.create(worksheet=S_AMAD, data=pd.concat([a_df, amad_row], ignore_index=True))
                        st.success(f"लॉट {l} सुरक्षित!")
                        st.cache_data.clear()
            except:
                st.error("शीट लोड नहीं हुई। टैब के नाम चेक करें।")

else:
    # वेलकम मैसेज हटा दिया गया है, सिर्फ खाली जगह दिखेगी
    st.write("") 

