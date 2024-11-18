import streamlit as st
import pandas as pd
import sqlite3
from fuzzywuzzy import process
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

def query_db(staff_number):
    """Query SQLite database for exact Staff number."""
    conn = sqlite3.connect("staff_data.db")
    query = f"SELECT * FROM staff WHERE `Staff number`='{staff_number}'"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def fuzzy_search(query):
    """Perform a fuzzy search on the 'Name' column."""
    conn = sqlite3.connect("staff_data.db")
    df = pd.read_sql_query("SELECT * FROM staff", conn)
    conn.close()
    
    matches = process.extract(query, df['Name'], limit=5)
    matched_names = [match[0] for match in matches]
    return df[df['Name'].isin(matched_names)]

def display_record(record):
    """Display a single staff record in a user-friendly format."""
    st.markdown("---")
    st.markdown(f"**Staff Number:** {record[0]}")
    st.markdown(f"**Name:** {record[1]}")
    st.markdown(f"**Designation:** {record[2]}")
    st.markdown(f"**Working Under:** {record[3]}")
    st.markdown(f"**Station / Place Where Posted:** {record[4]}")
    st.markdown(f"**Booth No.:** {record[5]}")
    st.markdown(f"**Booth Name:** {record[6]}")
    st.markdown("---")

def main():
    st.set_page_config(page_title="Staff Information Search", layout="wide")
    st.title("🔍 Staff Information Search")
    st.write("Search for staff details efficiently using the options below.")
    
    # Search options
    st.sidebar.header("Search Options")
    search_type = st.sidebar.radio("Search by:", ["Staff Number", "Name (Fuzzy Search)"])
    
    if search_type == "Staff Number":
        staff_number = st.sidebar.text_input("Enter Staff Number")
        if staff_number:
            staff_details = query_db(staff_number)
            if not staff_details.empty:
                st.success(f"### Details for Staff Number: {staff_number}")
                for _, record in staff_details.iterrows():
                    display_record(record.tolist())
            else:
                st.error("No records found for this Staff Number.")
    
    elif search_type == "Name (Fuzzy Search)":
        name_query = st.sidebar.text_input("Enter Name")
        if name_query:
            fuzzy_results = fuzzy_search(name_query)
            if not fuzzy_results.empty:
                st.success(f"### Fuzzy Search Results for Name: {name_query}")
                for _, record in fuzzy_results.iterrows():
                    display_record(record.tolist())
            else:
                st.error("No records found for this Name.")

if __name__ == "__main__":
    main()
