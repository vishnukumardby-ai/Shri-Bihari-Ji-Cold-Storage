import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# पेज सेटिंग
st.set_page_config(page_title="Shri Bihari Ji Cold Storage", layout="wide")

# हेडर डिजाइन - मानीमऊ के साथ
st.markdown("""
    <div style='text-align: center; background-color: #1E3A8A; padding: 20px; border-radius: 15px; color: white;'>
        <h1 style='margin: 0;'>🚜 श्री बिहारी जी कोल्ड स्टोरेज</h1>
        <h3 style='margin: 5px;'><b>उदैतापुर, मानीमऊ, कन्नौज (U.P.)</b></h3>
    </div>
    <br>
""", unsafe_allow_html=True)

# कनेक्शन की कोशिश
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as conn_err:
    st.error(f"शीट से कनेक्शन फेल! कृपया Secrets चेक करें। एरर: {conn_err}")

choice = st.radio("", ["Home", "Farmer Login"], horizontal=True)

if choice == "Farmer Login":
    # लॉगिन बॉक्स
    km = st.text_input("मोबाइल नंबर (Mobile Number)")
    ka = st.text_input("अकाउंट नंबर (Account Number)", type="password")
    
    if st.button("प्रवेश करें / Sign In"):
        if not km or not ka:
            st.warning("कृपया मोबाइल और अकाउंट नंबर दोनों भरें।")
        else:
            try:
                # मास्टर शीट पढ़ना
                m_df = conn.read(worksheet="Master", ttl=0)
                m_df.columns = m_df.columns.str.strip()
                
                # मिलान करना
                match = m_df[(m_df['Mobile_Number'].astype(str).str.strip() == str(km).strip()) & 
                             (m_df['Account_Number'].astype(str).str.strip() == str(ka).strip())]
                
                if not match.empty:
                    f_name = match['Name'].iloc[0]
                    st.success(f"नमस्ते, {f_name} जी!")
                    
                    # अमद (Amad) डाटा पढ़ना
                    try:
                        a_df = conn.read(worksheet="Amad", ttl=0)
                        a_df.columns = a_df.columns.str.strip()
                        f_a = a_df[a_df['Account_Number'].astype(str).str.strip() == str(ka).strip()]
                        
                        if not f_a.empty:
                            st.table(f_a[['Date', 'Lot_Number', 'Packets', 'Type']])
                        else:
                            st.info("अभी आपका कोई आलू स्टॉक जमा नहीं है।")
                    except Exception as amad_err:
                        st.error(f"Amad शीट में गड़बड़ है। कृपया चेक करें कि 'Account_Number' लिखा है या नहीं।")
                else:
                    st.error("रिकॉर्ड नहीं मिला! मोबाइल या अकाउंट नंबर गलत है।")
            except Exception as master_err:
                st.error(f"मास्टर शीट नहीं मिल रही। क्या आपने गूगल शीट में 'Master' नाम का टैब बनाया है?")
else:
    st.info("स्वागत है! अपना आलू का हिसाब देखने के लिए 'Farmer Login' चुनें।")
