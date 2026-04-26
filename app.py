import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# वेबसाइट की सेटिंग
st.set_page_config(page_title="Shri Bihari Ji Cold Storage", layout="wide")

# मुख्य हेडर
st.markdown("""
    <div style='text-align: center; background-color: #f8fafc; padding: 25px; border: 2px solid #1E3A8A; border-radius: 15px;'>
        <h1 style='color: #1E3A8A; margin-bottom: 5px; font-family: "Arial", sans-serif;'>🚜 SHRI BIHARI JI COLD STORAGE</h1>
        <p style='font-size: 20px; color: #1e293b; margin: 0;'><b>Udaitapur, Manimau, Kannauj (Uttar Pradesh)</b></p>
        <p style='font-size: 16px; margin: 8px 0;'>📧 shribiharijicoldstorage@gmail.com</p>
        <p style='font-size: 16px; margin: 0;'>📞 9838646586, 9621996103, 7007490379</p>
    </div>
    <br>
""", unsafe_allow_html=True)

conn = st.connection("gsheets", type=GSheetsConnection)

# साइडबार लॉगिन
login_type = st.sidebar.selectbox("लॉगिन चुनें", ["किसान लॉगिन", "एडमिन (मैनेजमेंट)"])

if login_type == "एडमिन (मैनेजमेंट)":
    pwd = st.sidebar.text_input("पासवर्ड", type="password")
    if pwd == "bihariji123":
        st.sidebar.success("लॉगिन सफल")
        task = st.sidebar.radio("काम चुनें", ["नया किसान जोड़ें (Master)", "आमद (Amad)", "लोन (Loan)", "बारदाना (Bardana)"])
        
        master_df = conn.read(worksheet="Farmers_Master")
        
        if task == "नया किसान जोड़ें (Master)":
            st.subheader("🆕 नए किसान का रजिस्ट्रेशन")
            with st.form("master_form"):
                m_name = st.text_input("किसान का नाम")
                m_fname = st.text_input("पिता का नाम")
                m_vill = st.text_input("गाँव")
                m_acc = st.text_input("अकाउंट नंबर (A/c No.)")
                m_mob = st.text_input("मोबाइल नंबर")
                if st.form_submit_button("मास्टर लिस्ट में सेव करें"):
                    new_m = pd.DataFrame([{"Name": m_name, "Father_Name": m_fname, "Village": m_vill, "Account_No": m_acc, "Mobile": m_mob}])
                    updated_master = pd.concat([master_df, new_m], ignore_index=True)
                    conn.update(worksheet="Farmers_Master", data=updated_master)
                    st.success("किसान मास्टर लिस्ट में जुड़ गया!")

        else:
            st.subheader(f"📝 {task} वाउचर एंट्री")
            # सर्च फीचर
            search_list = (master_df['Name'] + " s/o " + master_df['Father_Name'] + " (" + master_df['Village'] + ")").tolist()
            selected_farmer = st.selectbox("किसान खोजें (नाम लिखना शुरू करें...)", [""] + search_list)
            
            with st.form("voucher_form"):
                col1, col2 = st.columns(2)
                f_data = master_df[search_list.index(selected_farmer)-1 == master_df.index] if selected_farmer else pd.DataFrame()
                
                with col1:
                    v_no = st.text_input("वाउचर नंबर")
                    name = st.text_input("नाम", value=f_data['Name'].iloc[0] if not f_data.empty else "")
                    f_name = st.text_input("पिता का नाम", value=f_data['Father_Name'].iloc[0] if not f_data.empty else "")
                    acc_no = f_data['Account_No'].iloc[0] if not f_data.empty else ""
                    st.info(f"Account No: {acc_no}")
                with col2:
                    date = st.date_input("तारीख", datetime.now())
                    village = st.text_input("गाँव", value=f_data['Village'].iloc[0] if not f_data.empty else "")
                    mobile = f_data['Mobile'].iloc[0] if not f_data.empty else ""

                if task == "Amad":
                    lot = st.text_input("लॉट नंबर")
                    pkts = st.number_input("पैकेट संख्या", min_value=0, step=1)
                elif task == "Loan":
                    loan = st.number_input("लोन राशि (₹)", min_value=0, step=100)
                elif task == "Bardana":
                    jute = st.number_input("जूट बैग", min_value=0)
                    plastic = st.number_input("प्लास्टिक बैग", min_value=0)
                    cost = st.number_input("कुल कीमत (₹)", min_value=0)

                if st.form_submit_button("वाउचर सुरक्षित करें"):
                    df = conn.read(worksheet=task)
                    row = {"Date": date.strftime("%d-%m-%Y"), "Voucher_No": v_no, "Name": name, "Father_Name": f_name, 
                           "Village": village, "Account_No": acc_no, "Mobile": mobile}
                    if task == "Amad": row.update({"Lot_No": lot, "Packets": pkts})
                    elif task == "Loan": row.update({"Loan_Amount": loan})
                    elif task == "Bardana": row.update({"Jute_Bags": jute, "Plastic_Bags": plastic, "Total_Bags_Cost": cost})
                    
                    updated_df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
                    conn.update(worksheet=task, data=updated_df)
                    st.success(f"{task} एंट्री सुरक्षित!")

elif login_type == "किसान लॉगिन":
    st.subheader("👨‍🌾 किसान भाई अपना रिकॉर्ड देखें")
    col_k1, col_k2 = st.columns(2)
    with col_k1:
        k_mob = st.text_input("अपना रजिस्टर्ड मोबाइल नंबर")
    with col_k2:
        k_acc = st.text_input("अपना अकाउंट नंबर (A/c No.)", type="password")

    if st.button("हिसाब देखें"):
        amad_df = conn.read(worksheet="Amad")
        loan_df = conn.read(worksheet="Loan")
        bard_df = conn.read(worksheet="Bardana")
        
        # मोबाइल और अकाउंट नंबर दोनों का मिलान
        f_amad = amad_df[(amad_df['Mobile'].astype(str) == str(k_mob)) & (amad_df['Account_No'].astype(str) == str(k_acc))]
        f_loan = loan_df[(loan_df['Mobile'].astype(str) == str(k_mob)) & (loan_df['Account_No'].astype(str) == str(k_acc))]
        f_bard = bard_df[(bard_df['Mobile'].astype(str) == str(k_mob)) & (bard_df['Account_No'].astype(str) == str(k_acc))]
        
        if not f_amad.empty or not f_loan.empty or not f_bard.empty:
            name_val = f_amad['Name'].iloc[0] if not f_amad.empty else (f_loan['Name'].iloc[0] if not f_loan.empty else f_bard['Name'].iloc[0])
            st.success(f"नमस्ते {name_val} जी!")
            
            t1, t2, t3 = st.tabs(["आलू स्टॉक (Amad)", "लोन विवरण", "बारदाना"])
            with t1: st.dataframe(f_amad[['Date', 'Voucher_No', 'Lot_No', 'Packets']])
            with t2: st.dataframe(f_loan[['Date', 'Voucher_No', 'Loan_Amount']])
            with t3: st.dataframe(f_bard[['Date', 'Voucher_No', 'Jute_Bags', 'Plastic_Bags', 'Total_Bags_Cost']])
            
            st.markdown(f"""
            ### 📊 कुल सारांश:
            * **कुल पैकेट जमा:** {f_amad['Packets'].sum()}
            * **कुल लोन बकाया:** ₹{f_loan['Loan_Amount'].sum()}
            * **बारदाना खर्च:** ₹{f_bard['Total_Bags_Cost'].sum()}
            """)
        else:
            st.error("रिकॉर्ड नहीं मिला। कृपया अपना मोबाइल नंबर और अकाउंट नंबर जाँचें।")
