import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="श्री बिहारी जी कोल्ड स्टोरेज", layout="wide")

st.title("🚜 श्री बिहारी जी कोल्ड स्टोरेज")
st.write("📍 उदैतापुर, कन्नौज | **पार्टनरशिप फर्म**")

# गूगल शीट कनेक्शन
conn = st.connection("gsheets", type=GSheetsConnection)

menu = st.sidebar.selectbox("लॉगिन चुनें", ["किसान लॉगिन", "एडमिन (मैनेजमेंट)"])

if menu == "एडमिन (मैनेजमेंट)":
    password = st.sidebar.text_input("पासवर्ड दर्ज करें", type="password")
    if password == "bihariji123":
        st.subheader("📝 नया स्टॉक रजिस्टर एंट्री")
        with st.form("entry_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("किसान का नाम")
                f_name = st.text_input("पिता का नाम")
                village = st.text_input("गाँव")
            with col2:
                lot_no = st.text_input("लॉट नंबर (Lot No.)")
                pkts = st.number_input("पैकेट की संख्या", min_value=1, step=1)
            
            submitted = st.form_submit_button("डाटा सेव करें")
            
            if submitted:
                if name and village:
                    new_data = pd.DataFrame([{
                        "Date": datetime.now().strftime("%d-%m-%Y"),
                        "Name": name,
                        "Father Name": f_name,
                        "Village": village,
                        "Lot No.": lot_no,
                        "Packet": pkts
                    }])
                    df = conn.read()
                    updated_df = pd.concat([df, new_data], ignore_index=True)
                    conn.update(data=updated_df)
                    st.success(f"बधाई हो! {name} का डाटा सुरक्षित हो गया है।")
                else:
                    st.error("कृपया नाम और गाँव ज़रूर भरें।")
        
        st.write("---")
        st.subheader("📊 लाइव स्टॉक रजिस्टर (Excel View)")
        data = conn.read()
        st.dataframe(data)

elif menu == "किसान लॉगिन":
    st.subheader("👨‍🌾 किसान भाई अपना रिकॉर्ड देखें")
    search = st.text_input("अपना नाम या गाँव लिखकर खोजें")
    if st.button("खोजें"):
        data = conn.read()
        result = data[(data['Name'].str.contains(search, case=False, na=False)) | 
                      (data['Village'].str.contains(search, case=False, na=False))]
        if not result.empty:
            st.write(result)
        else:
            st.warning("कोई रिकॉर्ड नहीं मिला।")
