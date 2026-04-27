import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# पेज सेटिंग
st.set_page_config(page_title="Shri Bihari Ji Cold Storage", layout="wide")

# हेडर (मानीमऊ और सही पते के साथ)
st.markdown("""
    <div style='text-align: center; background-color: #1E3A8A; padding: 20px; border-radius: 15px; color: white;'>
        <h1 style='margin: 0;'>🚜 श्री बिहारी जी कोल्ड स्टोरेज</h1>
        <h3 style='margin: 5px;'><b>उदैतापुर, मानीमऊ, कन्नौज (U.P.)</b></h3>
    </div>
    <br>
""", unsafe_allow_html=True)

# गूगल शीट से कनेक्शन
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    st.error("शीट से कनेक्शन नहीं हो पा रहा। कृपया 'Secrets' चेक करें।")

choice = st.radio("", ["Home", "Farmer Login"], horizontal=True)

if choice == "Farmer Login":
    km = st.text_input("मोबाइल नंबर (Mobile Number)")
    ka = st.text_input("अकाउंट नंबर (Account Number)", type="password")
    
    if st.button("प्रवेश करें / Sign In"):
        try:
            # मास्टर शीट पढ़ना
            m_df = conn.read(worksheet="Master", ttl=0)
            m_df.columns = m_df.columns.str.strip() # कॉलम के नाम से स्पेस हटाना
            
            # लॉगिन मिलान
            match = m_df[(m_df['Mobile_Number'].astype(str).str.strip() == str(km).strip()) & 
                         (m_df['Account_Number'].astype(str).str.strip() == str(ka).strip())]
            
            if not match.empty:
                f_name = match['Name'].iloc[0]
                st.success(f"नमस्ते, {f_name} जी!")
                
                # अमद (Amad) डाटा पढ़ना
                try:
                    a_df = conn.read(worksheet="Amad", ttl=0)
                    a_df.columns = a_df.columns.str.strip()
                    
                    # अकाउंट नंबर से हिसाब ढूंढना
                    f_a = a_df[a_df['Account_Number'].astype(str).str.strip() == str(ka).strip()]
                    
                    if not f_a.empty:
                        st.subheader("आपका आलू स्टॉक रिकॉर्ड:")
                        # जो कॉलम आपकी शीट में हैं
                        st.table(f_a[['Date', 'Lot_Number', 'Packets', 'Type']])
                    else:
                        st.warning("इस अकाउंट नंबर का कोई स्टॉक रिकॉर्ड नहीं मिला।")
                except Exception as e:
                    st.error(f"Amad शीट के कॉलम में गड़बड़ है: {e}")
            else:
                st.error("विवरण गलत हैं। कृपया दोबारा चेक करें।")
        except Exception as e:
            st.error("मास्टर शीट पढ़ने में समस्या आ रही है।")
else:
    st.info("स्वागत है! अपना हिसाब देखने के लिए 'Farmer Login' पर जाएँ।")
