import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# पेज सेटिंग
st.set_page_config(page_title="Shri Bihari Ji Cold Storage", layout="wide")

# भाषा चयन
lang = st.sidebar.radio("Language / भाषा", ["English", "Hindi"])

t = {
    "title": "🚜 SHRI BIHARI JI COLD STORAGE" if lang == "English" else "🚜 श्री बिहारी जी कोल्ड स्टोरेज",
    "addr": "Udaitapur, Manimau, Kannauj" if lang == "English" else "उदैतापुर, मानीमऊ, कन्नौज",
    "mob": "Mobile Number" if lang == "English" else "मोबाइल नंबर",
    "acc": "Account Number" if lang == "English" else "अकाउंट नंबर",
    "signin": "Sign In" if lang == "English" else "प्रवेश करें",
}

# हेडर (मानीमऊ के साथ)
st.markdown(f"""
    <div style='text-align: center; background-color: #1E3A8A; padding: 25px; border-radius: 15px; color: white;'>
        <h1 style='margin: 0; font-family: sans-serif;'>{t['title']}</h1>
        <h2 style='margin: 5px; font-size: 22px;'><b>{t['addr']}</b></h2>
        <p style='font-size: 15px; margin: 0;'>📞 9838646586, 9621996103, 7007490379</p>
    </div>
    <br>
""", unsafe_allow_html=True)

conn = st.connection("gsheets", type=GSheetsConnection)

choice = st.radio("", ["Home", "Farmer Login"], horizontal=True)

if choice == "Farmer Login":
    col1, col2 = st.columns(2)
    with col1: km = st.text_input(t['mob'])
    with col2: ka = st.text_input(t['acc'], type="password")
    
    if st.button(t['signin']):
        try:
            # मास्टर शीट पढ़ना
            m_df = conn.read(worksheet="Master", ttl=0)
            m_df.columns = m_df.columns.str.strip()
            
            # मिलान प्रक्रिया
            match = m_df[(m_df['Mobile_Number'].astype(str).str.strip() == str(km).strip()) & 
                         (m_df['Account_Number'].astype(str).str.strip() == str(ka).strip())]
            
            if not match.empty:
                f_name = match['Name'].iloc[0]
                st.success(f"नमस्ते, {f_name} जी!")
                
                # अमद (Amad) डाटा पढ़ना
                try:
                    a_df = conn.read(worksheet="Amad", ttl=0)
                    a_df.columns = a_df.columns.str.strip()
                    
                    # अब सीधे Account_Number से हिसाब ढूँढना (जो आपने अभी शीट में जोड़ा है)
                    f_a = a_df[a_df['Account_Number'].astype(str).str.strip() == str(ka).strip()]
                    
                    if not f_a.empty:
                        st.subheader("आपका आलू स्टॉक (Amad Record):")
                        # केवल काम के कॉलम दिखाना
                        show_cols = ['Date', 'Lot_Number', 'Packets', 'Type']
                        # अगर आपकी शीट में ये कॉलम हैं तो दिखाओ, वरना पूरी टेबल दिखाओ
                        valid_cols = [c for c in show_cols if c in f_a.columns]
                        st.table(f_a[valid_cols] if valid_cols else f_a)
                    else:
                        st.warning("कोई स्टॉक रिकॉर्ड नहीं मिला।")
                except Exception as e:
                    st.error(f"Amad शीट पढ़ने में समस्या: {e}")
            else:
                st.error("रिकॉर्ड नहीं मिला! कृपया मोबाइल और अकाउंट नंबर दोबारा देखें।")
        except Exception as e:
            st.error("कनेक्शन में समस्या! कृपया अपनी गूगल शीट चेक करें।")

else:
    st.info("स्वागत है! अपना हिसाब देखने के लिए Farmer Login पर क्लिक करें।")
