import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import sys

# Unicode Error fix
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# वेबसाइट सेटिंग
st.set_page_config(page_title="Shri Bihari Ji Cold Storage", layout="wide")

# कनेक्शन
conn = st.connection("gsheets", type=GSheetsConnection)

# भाषा चयन
lang = st.sidebar.radio("Language / भाषा", ["Hindi", "English"])

t = {
    "title": "🚜 श्री बिहारी जी कोल्ड स्टोरेज" if lang == "Hindi" else "🚜 SHRI BIHARI JI COLD STORAGE",
    "addr": "उदैतापुर, मनीमऊ, कन्नौज (उत्तर प्रदेश)" if lang == "Hindi" else "Udaitapur, Manimau, Kannauj (U.P.)",
    "home": "होम पेज" if lang == "Hindi" else "Home Page",
    "k_login": "किसान लॉगिन" if lang == "Hindi" else "Farmer Login",
    "a_login": "एडमिन लॉगिन" if lang == "Hindi" else "Admin Login",
    "save": "सुरक्षित करें" if lang == "Hindi" else "Save Data",
    "success": "सफलतापूर्वक सुरक्षित!" if lang == "Hindi" else "Saved Successfully!",
    "name": "नाम" if lang == "Hindi" else "Name",
    "fname": "पिता का नाम" if lang == "Hindi" else "Father Name",
    "vill": "गाँव" if lang == "Hindi" else "Village",
}

# हेडर (ईमेल और मोबाइल नंबर हटा दिया गया है)
st.markdown(f"""
    <div style='text-align: center; background-color: #1E3A8A; padding: 25px; border-radius: 10px; color: white;'>
        <h1 style='margin: 0;'>{t['title']}</h1>
        <p style='font-size: 18px; margin: 5px 0;'><b>{t['addr']}</b></p>
    </div>
""", unsafe_allow_html=True)

# साइडबार
login_type = st.sidebar.selectbox("Menu", [t['home'], t['k_login'], t['a_login']])

if login_type == t['home']:
    # वेलकम मैसेज हटा दिया गया है, यहाँ आप फोटो या जनरल जानकारी दे सकते हैं
    st.info("कोल्ड स्टोरेज मैनेजमेंट सिस्टम में आपका स्वागत है। कृपया मेन्यू से विकल्प चुनें।")

elif login_type == t['a_login']:
    pwd = st.sidebar.text_input("Password", type="password")
    if pwd == "bihariji123":
        task = st.sidebar.radio("Task", ["Registration", "Amad Entry", "Loan Entry", "Bardana Entry"])
        master_df = conn.read(worksheet="Master List", ttl=60)
        
        if task == "Registration":
            st.subheader("🆕 New Farmer Registration")
            with st.form("reg_form"):
                n = st.text_input(t['name']); fn = st.text_input(t['fname'])
                v = st.text_input(t['vill']); m = st.text_input("Mobile Number"); ac = st.text_input("Account Number")
                if st.form_submit_button(t['save']):
                    new_row = pd.DataFrame([{"Name": n, "Father Name": fn, "Village Name": v, "Mobile Number": m, "Account Number": ac}])
                    conn.update(worksheet="Master List", data=pd.concat([master_df, new_row], ignore_index=True))
                    st.success(t['success'])

        elif task == "Amad Entry":
            st.subheader("📦 Amad (Stock) Entry")
            amad_df = conn.read(worksheet="Amad", ttl=10)
            next_lot = 1
            if not amad_df.empty:
                max_lot = pd.to_numeric(amad_df['Lot Number'], errors='coerce').max()
                next_lot = int(max_lot + 1) if not pd.isna(max_lot) else 1
            
            s_list = (master_df['Name'] + " s/o " + master_df['Father Name']).tolist()
            sel = st.selectbox("Search Farmer", [""] + s_list)
            
            with st.form("amad_form"):
                dt = st.date_input("Date", datetime.now())
                lot = st.number_input("Lot Number", value=next_lot)
                pk = st.number_input("Packets", min_value=1)
                tp = st.selectbox("Type", ["Oorja", "Lal", "Safed", "Halland", "Sindoori"])
                if st.form_submit_button(t['save']) and sel != "":
                    f_row = master_df.iloc[s_list.index(sel)]
                    new_data = pd.DataFrame([{"Date": dt.strftime("%d-%m-%Y"), "Lot Number": lot, "Packet": pk, "Name": f_row['Name'], "Father Name": f_row['Father Name'], "Village Name": f_row['Village Name'], "Type": tp, "Account Number": f_row['Account Number']}])
                    conn.update(worksheet="Amad", data=pd.concat([amad_df, new_data], ignore_index=True))
                    st.success(t['success'])

        elif task == "Loan Entry":
            st.subheader("💰 Loan Entry")
            loan_df = conn.read(worksheet="Loan", ttl=10)
            s_list = (master_df['Name'] + " s/o " + master_df['Father Name']).tolist()
            sel = st.selectbox("Search Farmer", [""] + s_list)
            with st.form("loan_form"):
                dt = st.date_input("Date", datetime.now())
                vn = st.text_input("Voucher Number")
                amt = st.number_input("Amount (₹)", min_value=0)
                rem = st.text_input("Remarks")
                if st.form_submit_button(t['save']) and sel != "":
                    f_row = master_df.iloc[s_list.index(sel)]
                    new_loan = pd.DataFrame([{"Date": dt.strftime("%d-%m-%Y"), "Voucher Number": vn, "Name": f_row['Name'], "Father Name": f_row['Father Name'], "Village Name": f_row['Village Name'], "Amount": amt, "Remarks": rem, "Account Number": f_row['Account Number']}])
                    conn.update(worksheet="Loan", data=pd.concat([loan_df, new_loan], ignore_index=True))
                    st.success(t['success'])

        elif task == "Bardana Entry":
            st.subheader("🎒 Bardana Entry")
            bardana_df = conn.read(worksheet="Bardana", ttl=10)
            s_list = (master_df['Name'] + " s/o " + master_df['Father Name']).tolist()
            sel = st.selectbox("Search Farmer", [""] + s_list)
            with st.form("bardana_form"):
                dt = st.date_input("Date", datetime.now())
                qty = st.number_input("Bags Quantity", min_value=0)
                b_type = st.selectbox("Bag Type", ["Jute", "Plastic"])
                if st.form_submit_button(t['save']) and sel != "":
                    f_row = master_df.iloc[s_list.index(sel)]
                    new_b = pd.DataFrame([{"Date": dt.strftime("%d-%m-%Y"), "Name": f_row['Name'], "Father Name": f_row['Father Name'], "Quantity": qty, "Type": b_type, "Account Number": f_row['Account Number']}])
                    conn.update(worksheet="Bardana", data=pd.concat([bardana_df, new_b], ignore_index=True))
                    st.success(t['success'])

else:
    st.write("मेन्यू से लॉगिन करें।")
