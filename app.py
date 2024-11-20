import streamlit as st
import pandas as pd
import sqlite3
import logging
import base64

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

# Dictionary for multilingual content
TRANSLATIONS = {
    'en': {
        'main_title': 'South Western Railway',
        'sub_title': 'Bengaluru Division - Personnel Department',
        'election_title': 'Secret Ballot Election 2024',
        'search_placeholder': 'Enter PF/HRMS ID',
        'search_instruction': 'Enter PF Number or HRMS ID to view details',
        'personal_details': 'Personal Details',
        'name': 'Name',
        'designation': 'Designation',
        'working_under': 'Working Under',
        'station_place': 'Station/Place',
        'booth_details': 'Booth Details',
        'booth_serial': 'Booth Serial Number',
        'booth_number': 'Booth Number',
        'booth_location': 'Booth Location',
        'remarks': 'Remarks',
        'no_records': '❌ No records found. Please check the PF Number or HRMS ID.',
        'footer_text': 'Initiative by Team Personnel | © 2024 South Western Railway, Bengaluru Division'
    },
    'hi': {
        'main_title': 'दक्षिण पश्चिम रेलवे',
        'sub_title': 'बेंगलुरु मंडल - कार्मिक विभाग',
        'election_title': 'गुप्त मतदान चुनाव २०२४',
        'search_placeholder': 'पीएफ/एचआरएमएस आईडी दर्ज करें',
        'search_instruction': 'विवरण देखने के लिए पीएफ नंबर या एचआरएमएस आईडी दर्ज करें',
        'personal_details': 'व्यक्तिगत विवरण',
        'name': 'नाम',
        'designation': 'पद',
        'working_under': 'अधीन कार्यरत',
        'station_place': 'स्टेशन/स्थान',
        'booth_details': 'मतदान केंद्र विवरण',
        'booth_serial': 'मतदान केंद्र क्रम संख्या',
        'booth_number': 'मतदान केंद्र संख्या',
        'booth_location': 'मतदान केंद्र स्थान',
        'remarks': 'टिप्पणियां',
        'no_records': '❌ कोई रिकॉर्ड नहीं मिला। कृपया पीएफ नंबर या एचआरएमएस आईडी की जांच करें।',
        'footer_text': 'कार्मिक टीम द्वारा पहल | © 2024 दक्षिण पश्चिम रेलवे, बेंगलुरु मंडल'
    },
    'kn': {
        'main_title': 'ದಕ್ಷಿಣ ಪಶ್ಚಿಮ ರೈಲ್ವೆ',
        'sub_title': 'ಬೆಂಗಳೂರು ವಿಭಾಗ - ಸಿಬ್ಬಂದಿ ವಿಭಾಗ',
        'election_title': 'ರಹಸ್ಯ ಮತದಾನ ಚುನಾವಣೆ ೨೦೨೪',
        'search_placeholder': 'ಪಿಎಫ್/ಎಚ್ಆರ್ಎಂಎಸ್ ಐಡಿ ನಮೂದಿಸಿ',
        'search_instruction': 'ವಿವರಗಳನ್ನು ವೀಕ್ಷಿಸಲು ಪಿಎಫ್ ಸಂಖ್ಯೆ ಅಥವಾ ಎಚ್ಆರ್ಎಂಎಸ್ ಐಡಿ ನಮೂದಿಸಿ',
        'personal_details': 'ವೈಯಕ್ತಿಕ ವಿವರಗಳು',
        'name': 'ಹೆಸರು',
        'designation': 'ಹುದ್ದೆ',
        'working_under': 'ಅಡಿಯಲ್ಲಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಿರುವ',
        'station_place': 'ನಿಲ್ದಾಣ/ಸ್ಥಳ',
        'booth_details': 'ಮತಗಟ್ಟೆ ವಿವರಗಳು',
        'booth_serial': 'ಮತಗಟ್ಟೆ ಕ್ರಮ ಸಂಖ್ಯೆ',
        'booth_number': 'ಮತಗಟ್ಟೆ ಸಂಖ್ಯೆ',
        'booth_location': 'ಮತಗಟ್ಟೆ ಸ್ಥಳ',
        'remarks': 'ಟಿಪ್ಪಣಿಗಳು',
        'no_records': '❌ ದಾಖಲೆಗಳು ಕಂಡುಬಂದಿಲ್ಲ. ದಯವಿಟ್ಟು ಪಿಎಫ್ ಸಂಖ್ಯೆ ಅಥವಾ ಎಚ್ಆರ್ಎಂಎಸ್ ಐಡಿ ಪರಿಶೀಲಿಸಿ.',
        'footer_text': 'ಸಿಬ್ಬಂದಿ ತಂಡದ ಮೂಲಕ ಉಪಕ್ರಮ | © 2024 ದಕ್ಷಿಣ ಪಶ್ಚಿಮ ರೈಲ್ವೆ, ಬೆಂಗಳೂರು ವಿಭಾಗ'
    }
}

def get_base64_encoded_image(image_path):
    """Get base64 encoded image"""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        logging.error(f"Error encoding image: {e}")
        return None

def query_db(id_number):
    """Query SQLite database for PF number or HRMS ID."""
    try:
        conn = sqlite3.connect("staff_data.db")
        query = f"SELECT * FROM staff WHERE PF_No='{id_number}' OR HRMS_ID='{id_number}'"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        logging.error(f"Database query error: {e}")
        return pd.DataFrame()
def display_record(record, lang):
    """Display a single staff record in a compact card format."""
    st.markdown(f"""
        <div class="record-card">
            <div class="section-title">
                {TRANSLATIONS[lang]['personal_details']}
            </div>
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">{TRANSLATIONS[lang]['name']}</div>
                    <div class="info-value">{record['Name']}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">PF/HRMS</div>
                    <div class="info-value">{record['PF_No']} / {record['HRMS_ID']}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">{TRANSLATIONS[lang]['designation']}</div>
                    <div class="info-value">{record['Post_Designation']}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">{TRANSLATIONS[lang]['working_under']}</div>
                    <div class="info-value">{record['Working_Under']}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">{TRANSLATIONS[lang]['station_place']}</div>
                    <div class="info-value">{record['Station_Place']}</div>
                </div>
            </div>
        </div>

        <div class="booth-card">
            <div class="booth-title">
                {TRANSLATIONS[lang]['booth_details']}
            </div>
            <div class="booth-content">
                <div class="booth-item">
                    <div class="booth-label">{TRANSLATIONS[lang]['booth_serial']}</div>
                    <div class="booth-value">{record['Booth_Sl_No']}</div>
                </div>
                <div class="booth-item">
                    <div class="booth-label">{TRANSLATIONS[lang]['booth_number']}</div>
                    <div class="booth-value">{record['Booth_No']}</div>
                </div>
                <div class="booth-item">
                    <div class="booth-label">{TRANSLATIONS[lang]['booth_location']}</div>
                    <div class="booth-value">{record['Booth_Name']}</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if pd.notna(record['Remarks']):
        st.markdown(f"""
            <div class="remarks-card">
                <span class="remarks-label">{TRANSLATIONS[lang]['remarks']}:</span>
                <span class="remarks-value">{record['Remarks']}</span>
            </div>
        """, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="SWR Secret Ballot Election 2024",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Initialize session state for language
    if 'language' not in st.session_state:
        st.session_state.language = 'en'

    # Load CSS
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    # Language Switcher and Header
    col1, col2 = st.columns([0.85, 0.15])
    with col2:
        selected_lang = st.selectbox(
            '',
            options=['en', 'hi', 'kn'],
            format_func=lambda x: {'en': 'English', 'hi': 'हिंदी', 'kn': 'ಕನ್ನಡ'}[x],
            key='language_selector',
            label_visibility='collapsed'
        )
        st.session_state.language = selected_lang

    # Header with Logo
    try:
        logo_base64 = get_base64_encoded_image("logo.png")
        header_html = f"""
            <div class="header">
                <div class="logo-container">
                    <img src="data:image/png;base64,{logo_base64}" class="logo-img" alt="SWR Logo">
                </div>
                <div class="title-container">
                    <div class="main-title">
                        <div class="title-text">
                            {TRANSLATIONS[st.session_state.language]['main_title']}
                        </div>
                    </div>
                    <div class="sub-title">
                        <div class="title-text">
                            {TRANSLATIONS[st.session_state.language]['sub_title']}
                        </div>
                    </div>
                    <div class="election-title">
                        <div class="subtitle-text">
                            {TRANSLATIONS[st.session_state.language]['election_title']}
                        </div>
                    </div>
                </div>
            </div>
        """
        st.markdown(header_html, unsafe_allow_html=True)
    except Exception as e:
        logging.error(f"Error in header rendering: {e}")

    # Search Container with Instructions
    st.markdown(f"""
        <div class="search-container">
            <div class="search-instruction">
                {TRANSLATIONS[st.session_state.language]['search_instruction']}
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Search Input
    id_number = st.text_input(
        "🔍 Search",
        placeholder=TRANSLATIONS[st.session_state.language]['search_placeholder'],
        label_visibility="collapsed",
        max_chars=13
    )

    if id_number:
        with st.spinner(''):
            staff_details = query_db(id_number)
            if not staff_details.empty:
                for _, record in staff_details.iterrows():
                    display_record(record, st.session_state.language)
            else:
                st.markdown(f"""
                    <div class="error-msg">
                        {TRANSLATIONS[st.session_state.language]['no_records']}
                    </div>
                """, unsafe_allow_html=True)

    # Footer
    st.markdown(f"""
        <div class="footer-container">
            <div class="footer-text">
                {TRANSLATIONS[st.session_state.language]['footer_text']}
            </div>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()