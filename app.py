
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="श्री बिहारी जी कोल्ड स्टोरेज", layout="wide")
st.title("🚜 श्री बिहारी जी कोल्ड स्टोरेज - डिजिटल मुनीम")

conn = st.connection("gsheets", type=GSheetsConnection)

# साइडबार - लॉगिन टाइप
login_type = st.sidebar.selectbox("लॉगिन चुनें", ["किसान लॉगिन", "एडमिन (मैनेजमेंट)"])

if login_type == "एडमिन (मैनेजमेंट)":
    pwd = st.sidebar.text_input("पासवर्ड", type="password")
    if pwd == "bihariji123":
        st.sidebar.success("लॉगिन सफल")
        task = st.sidebar.radio("वाउचर चुनें", ["आमद (Stock)", "लोन (Loan)", "बारदाना (Bags)"])
        
        st.subheader(f"📝 {task} वाउचर एंट्री")
        with st.form("admin_form"):
            col1, col2 = st.columns(2)
            with col1:
                v_no = st.text_input("वाउचर नंबर")
                acc_no = st.text_input("किसान अकाउंट नंबर (A/c No.)")
                name = st.text_input("किसान का नाम")
                f_name = st.text_input("पिता का नाम")
            with col2:
                date = st.date_input("तारीख", datetime.now())
                village = st.text_input("गाँव")
                mobile = st.text_input("मोबाइल नंबर")
                
                if task == "आमद (Stock)":
                    lot = st.text_input("लॉट नंबर")
                    pkts = st.number_input("पैकेट की संख्या", min_value=0, step=1)
                elif task == "लोन (Loan)":
                    loan = st.number_input("लोन राशि (₹)", min_value=0, step=100)
                elif task == "बारदाना (Bags)":
                    jute = st.number_input("जूट बैग गिनती", min_value=0, step=1)
                    plastic = st.number_input("प्लास्टिक बैग गिनती", min_value=0, step=1)
                    rate = st.number_input("कुल कीमत (₹)", min_value=0, step=10)

            submitted = st.form_submit_button("डाटा सुरक्षित करें")
            if submitted:
                df = conn.read()
                new_row = {
                    "Voucher_Type": task, "Date": date.strftime("%d-%m-%Y"), "Voucher_No": v_no,
                    "Name": name, "Father_Name": f_name, "Village": village, 
                    "Account_No": acc_no, "Mobile": mobile,
                    "Lot_No": lot if task=="आमद (Stock)" else "",
                    "Packets": pkts if task=="आमद (Stock)" else 0,
                    "Loan_Amount": loan if task=="लोन (Loan)" else 0,
                    "Jute_Bags": jute if task=="बारदाना (Bags)" else 0,
                    "Plastic_Bags": plastic if task=="बारदाना (Bags)" else 0,
                    "Total_Bags_Cost": rate if task=="बारदाना (Bags)" else 0
                }
                updated_df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                conn.update(data=updated_df)
                st.success(f"बधाई हो! {task} वाउचर सफलतापूर्वक सेव हो गया।")

elif login_type == "किसान लॉगिन":
    st.subheader("👨‍🌾 किसान भाई अपना रिकॉर्ड देखें")
    st.info("विवरण देखने के लिए अपनी सही जानकारी भरें")
    
    col_k1, col_k2 = st.columns(2)
    with col_k1:
        k_name = st.text_input("अपना नाम लिखें")
        k_fname = st.text_input("पिता का नाम लिखें")
    with col_k2:
        k_village = st.text_input("गाँव का नाम")
        k_acc = st.text_input("अपना अकाउंट नंबर (Account No.) डालें", type="password")
    
    if st.button("अपना हिसाब देखें"):
        data = conn.read()
        # सुरक्षा फिल्टर
        result = data[
            (data['Name'].str.contains(k_name, case=False, na=False)) & 
            (data['Father_Name'].str.contains(k_fname, case=False, na=False)) & 
            (data['Village'].str.contains(k_village, case=False, na=False)) & 
            (data['Account_No'].astype(str) == str(k_acc))
        ]
        
        if not result.empty:
            st.success(f"नमस्ते {k_name} जी! आपका रिकॉर्ड नीचे है:")
            st.dataframe(result[["Date", "Voucher_Type", "Voucher_No", "Lot_No", "Packets", "Loan_Amount", "Total_Bags_Cost"]])
            
            # कुल हिसाब
            t_pkts = result['Packets'].sum()
            t_loan = result['Loan_Amount'].sum()
            t_bags = result['Total_Bags_Cost'].sum()
            st.markdown(f"### 📊 कुल बैलेंस रिपोर्ट:")
            st.write(f"📦 कुल पैकेट: **{t_pkts}** | 💰 कुल लोन: **₹{t_loan}** | 🎒 बारदाना खर्च: **₹{t_bags}**")
        else:
            st.error("जानकारी मेल नहीं खा रही है। कृपया अपना विवरण और अकाउंट नंबर सही भरें।")
