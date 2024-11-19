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

def display_record(record):
    """Display a single staff record in a compact card format."""
    st.markdown(f"""
        <div class="record-card">
            <div class="section-title">Personal Details</div>
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">Name</div>
                    <div class="info-value">{record['Name']}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">PF/HRMS</div>
                    <div class="info-value">{record['PF_No']} / {record['HRMS_ID']}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Designation</div>
                    <div class="info-value">{record['Post_Designation']}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Working Under</div>
                    <div class="info-value">{record['Working_Under']}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Station/Place</div>
                    <div class="info-value">{record['Station_Place']}</div>
                </div>
            </div>
        </div>

        <div class="booth-card">
            <div class="booth-title">Booth Details</div>
            <div class="booth-content">
                <div class="booth-item">
                    <div class="booth-label">Booth Slno</div>
                    <div class="booth-value">{record['Booth_No']}</div>
                </div>
                <div class="booth-item">
                    <div class="booth-label">Booth Name</div>
                    <div class="booth-value">{record['Booth_Name']}</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if pd.notna(record['Remarks']):
        st.markdown(f"""
            <div class="remarks-card">
                <span class="remarks-label">Remarks:</span>
                <span class="remarks-value">{record['Remarks']}</span>
            </div>
        """, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="SWR Secret Ballot Election 2024",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Load CSS
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

  

    # Header with Logo
    try:
        logo_base64 = get_base64_encoded_image("logo.png")
        header_html = f"""
            <div class="header">
                <div class="logo-container">
                    <img src="data:image/png;base64,{logo_base64}" class="logo-img" alt="SWR Logo">
                </div>
                <h1 class="title">South Western Railway</h1>
                <h2 class="subtitle">Secret Ballot Election 2024 - Bengaluru Division</h2>
            </div>
        """ if logo_base64 else """
            <div class="header">
                <h1 class="title">South Western Railway</h1>
                <h2 class="subtitle">Secret Ballot Election 2024 - Bengaluru Division</h2>
            </div>
        """
        st.markdown(header_html, unsafe_allow_html=True)
    except Exception as e:
        logging.error(f"Error in header rendering: {e}")
        st.markdown("""
            <div class="header">
                <h1 class="title">South Western Railway</h1>
                <h2 class="subtitle">Secret Ballot Election 2024 - Bengaluru Division</h2>
            </div>
        """, unsafe_allow_html=True)
  # Initial Footer
    st.markdown("""
        <div class="footer-container">
            <div class="footer-text">
                Enter PF Number or HRMS ID to view details
            </div>
        </div>
    """, unsafe_allow_html=True)
    # Search Container
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    id_number = st.text_input(
        "🔍 Search",
        placeholder="Enter PF/HRMS ID",
        label_visibility="collapsed",
        max_chars=13
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if id_number:
        with st.spinner(''):
            staff_details = query_db(id_number)
            if not staff_details.empty:
                for _, record in staff_details.iterrows():
                    display_record(record)
            else:
                st.markdown("""
                    <div class="error-msg">
                        ❌ No records found. Please check the PF Number or HRMS ID.
                    </div>
                """, unsafe_allow_html=True)

    # Final Footer
    st.markdown("""
        <div class="footer-container">
            <div class="footer-text">
                 Initiative by Team Personnel
            </div>
            <div class="footer-divider"></div>
            <div class="footer-copyright">
               Handcrafted by Anil B H |  © 2024 South Western Railway, Bengaluru Division
            </div>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()