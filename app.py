import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# वेबसाइट की सेटिंग
st.set_page_config(page_title="Shri Bihari Ji Cold Storage", layout="wide")

# भाषा चयन
lang = st.sidebar.radio("Select Language / भाषा चुनें", ["English", "Hindi"])

# शब्दकोश
t = {
    "title": "🚜 SHRI BIHARI JI COLD STORAGE" if lang == "English" else "🚜 श्री बिहारी जी कोल्ड स्टोरेज",
    "addr": "Udaitapur, Manimau, Kannauj (U.P.)" if lang == "English" else "उदैतापुर, मनीमऊ, कन्नौज (उत्तर प्रदेश)",
    "home": "Home Page" if lang == "English" else "होम पेज",
    "k_login": "Farmer Login" if lang == "English" else "किसान लॉगिन",
    "a_login": "Admin (Management)" if lang == "English" else "एडमिन (मैनेजमेंट)",
    "welcome": "Welcome to Shri Bihari Ji Cold Storage" if lang == "English" else "श्री बिहारी जी कोल्ड स्टोरेज में स्वागत है",
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

# हेडर
st.markdown(f"""
    <div style='text-align: center; background-color: #1E3A8A; padding: 30px; border-radius: 15px; color: white;'>
        <h1 style='margin-bottom: 5px;'>{t['title']}</h1>
        <p style='font-size: 20px;'><b>{t['addr']}</b></p>
        <p>📧 shribiharijicoldstorage@gmail.com | 📞 9838646586</p>
    </div>
""", unsafe_allow_html=True)

conn = st.connection("gsheets", type=GSheetsConnection)

# साइडबार
st.sidebar.markdown(f"### 🔒 Login")
login_type = st.sidebar.selectbox("Options", [t['home'], t['k_login'], t['a_login']])

if login_type == t['home']:
    st.markdown(f"<br><h2 style='text-align: center;'>{t['welcome']}</h2>", unsafe_allow_html=True)
    st.info("आधुनिक तकनीक और सुरक्षित भंडारण।")

elif login_type == t['a_login']:
    pwd = st.sidebar.text_input("Password", type="password")
    if pwd == "bihariji123":
        task = st.sidebar.radio("Select Task", ["New Farmer Registration", "Amad Entry", "Loan Entry", "Bardana Entry"])
        
        # शीट लोड करना (आपके फोटो के अनुसार नाम बदले गए हैं)
        master_df = conn.read(worksheet="Master List")
        
        if "Registration" in task:
            st.subheader("🆕 New Registration")
            with st.form("m_form"):
                m_n = st.text_input(t['name']); m_fn = st.text_input(t['fname'])
                m_v = st.text_input(t['vill']); m_m = st.text_input(t['mob']); m_a = st.text_input(t['acc'])
                if st.form_submit_button(t['save']):
                    new_m = pd.DataFrame([{"Name": m_n, "Father Name": m_fn, "Village Name": m_v, "Mobile Number": m_m, "Account Number": m_a}])
                    conn.update(worksheet="Master List", data=pd.concat([master_df, new_m], ignore_index=True))
                    st.success(t['success'])

        else:
            st.subheader(f"📝 {task}")
            s_list = (master_df['Name'] + " s/o " + master_df['Father Name']).tolist()
            sel = st.selectbox(t['search'], [""] + s_list)
            
            with st.form("v_form"):
                f_d = master_df[s_list.index(sel)-1 == master_df.index] if sel else pd.DataFrame()
                
                # ऑटो-फिल जानकारी
                v_n = st.text_input(t['v_no'])
                dt = st.date_input(t['date'], datetime.now())
                nm = st.text_input(t['name'], value=f_d['Name'].iloc[0] if not f_d.empty else "")
                fn = st.text_input(t['fname'], value=f_d['Father Name'].iloc[0] if not f_d.empty else "")
                vi = st.text_input(t['vill'], value=f_d['Village Name'].iloc[0] if not f_d.empty else "")
                ac = f_d['Account Number'].iloc[0] if not f_d.empty else ""
                mb = f_d['Mobile Number'].iloc[0] if not f_d.empty else ""

                if "Amad" in task:
                    # --- Automatic Lot Number Logic ---
                    amad_data = conn.read(worksheet="Amad")
                    if not amad_data.empty and 'Lot Number' in amad_data.columns:
                        max_lot = pd.to_numeric(amad_data['Lot Number'], errors='coerce').max()
                        next_lot = int(max_lot + 1) if not pd.isna(max_lot) else 1
                    else:
                        next_lot = 1
                    
                    lot = st.number_input("Lot Number", value=next_lot) # Swata badhta rahega
                    pk = st.number_input("Packets", min_value=0)
                    tp = st.selectbox("Type", ["Oorja", "Lal", "Safed", "Halland", "Sindoori"])
                
                elif "Loan" in task:
                    ln = st.number_input("Amount (₹)", min_value=0)
                    rem = st.text_input("Remarks")

                if st.form_submit_button(t['save']):
                    sheet_name = task.split()[0] # Amad, Loan, or Bardana
                    current_df = conn.read(worksheet=sheet_name)
                    
                    row = {"Date": dt.strftime("%d-%m-%Y"), "Name": nm, "Father Name": fn, "Village Name": vi, "Account Number": ac}
                    
                    if "Amad" in task:
                        row.update({"Lot Number": lot, "Packet": pk, "Type": tp})
                    elif "Loan" in task:
                        row.update({"Voucher Number": v_n, "Amount": ln, "Remarks": rem})
                    
                    conn.update(worksheet=sheet_name, data=pd.concat([current_df, pd.DataFrame([row])], ignore_index=True))
                    st.success(t['success'])

elif login_type == t['k_login']:
    st.subheader(f"👨‍🌾 {t['k_login']}")
    k_m = st.text_input(t['mob'])
    k_a = st.text_input(t['acc'], type="password")
    
    if st.button(t['signin_btn']):
        a_df = conn.read(worksheet="Amad")
        l_df = conn.read(worksheet="Loan")
        
        # किसान का डेटा फिल्टर करना
        f_a = a_df[(a_df['Account Number'].astype(str) == str(k_a))]
        
        if not f_a.empty:
            st.success(f"Welcome, {f_a['Name'].iloc[0]} जी!")
            tab1, tab2 = st.tabs(["Stock (आवक)", "Loan (कर्ज)"])
            with tab1: st.dataframe(f_a)
            with tab2: 
                f_l = l_df[(l_df['Account Number'].astype(str) == str(k_a))]
                st.dataframe(f_l)
        else:
            st.error("Invalid Details / जानकारी नहीं मिली")
