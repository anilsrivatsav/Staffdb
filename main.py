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
    """Convert CSV to SQLite database for efficient querying."""
    try:
        logging.info("Loading CSV data...")
        df = pd.read_csv(file_path)

        # Optimize memory usage
        df['Staff number'] = df['Staff number'].astype('str')
        df['Designation'] = df['Designation'].astype('category')
        df['Station / Place where posted'] = df['Station / Place where posted'].astype('category')

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
    file_path = input("Enter the path to your CSV file: ")  # You can remove this line if you're using the hardcoded file path
    if csv_to_sqlite(file_path):
        print("Data successfully loaded into SQLite database!")
    else:
        print("Failed to load data.")

if __name__ == "__main__":
    main()
