import pandas as pd
import sqlite3
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("conversion.log"),
        logging.StreamHandler()
    ]
)

def csv_to_sqlite(file_path):
    """Convert updated CSV structure to SQLite database for efficient querying."""
    try:
        logging.info("Loading CSV data...")
        df = pd.read_csv(file_path)
        
        # Debug: Print column names to identify exact names
        logging.info(f"Columns in CSV: {df.columns.tolist()}")
        
        # Create a mapping of old to new column names
        column_mapping = {
            'Sl.No.': 'Sl_No',
            'Booth_Sl.No.': 'Booth_Sl_No',
            'Post/ Designation': 'Post_Designation',
            'PF_No': 'PF_No',
            'HRMS ID': 'HRMS_ID',
            'Working Under': 'Working_Under',
            'Station / Place where posted': 'Station_Place',
            'Booth No.': 'Booth_No',
            'Booth Name': 'Booth_Name'
        }
        
        # Rename columns using the mapping
        df = df.rename(columns=column_mapping)
        
        # Optimize memory usage by setting appropriate types
        type_mapping = {
            'Sl_No': 'Int64',
            'Booth_Sl_No': 'string',
            'Name': 'string',
            'Post_Designation': 'category',
            'PF_No': 'string',
            'HRMS_ID': 'string',
            'Working_Under': 'category',
            'Station_Place': 'category',
            'Booth_No': 'Int64',
            'Booth_Name': 'string',
            'Remarks': 'string'
        }
        
        # Apply type conversions
        for column, dtype in type_mapping.items():
            if column in df.columns:
                if dtype == 'Int64':
                    df[column] = pd.to_numeric(df[column], errors='coerce').astype('Int64')
                else:
                    df[column] = df[column].astype(dtype)

        # Create SQLite database and save data
        with sqlite3.connect("staff_data.db") as conn:
            df.to_sql("staff", conn, if_exists='replace', index=False)

        logging.info("CSV data successfully loaded into SQLite database.")
        return True
    except Exception as e:
        logging.error("Error converting CSV to SQLite", exc_info=True)
        return False

def main():
    """Main entry point for data conversion."""
    file_path = input("Enter the path to your updated CSV file: ")
    if csv_to_sqlite(file_path):
        print("Data successfully loaded into SQLite database!")
    else:
        print("Failed to load data.")

if __name__ == "__main__":
    main()