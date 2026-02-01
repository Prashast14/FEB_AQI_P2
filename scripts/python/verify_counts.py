"""
AirPure AQI Analytics - Data Verification Script
=================================================
Compares row counts between source files and MySQL tables.
"""

import pymysql
import os

# Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'admin',
    'database': 'airpure_aqi_db'
}

BASE_PATH = r'd:\FEB_AQI_P2\AQI_dataset_Original\Dataful_Datasets'

FILES = {
    'aqi_daily': 'day-wise-state-wise-air-quality-index-aqi-of-major-cities-and-towns-in-india.csv',
    'disease_outbreak': 'master-data-state-district-and-disease-wise-cases-and-death-reported-due-to-outbreak-of-diseases-as-per-weekly-reports-under-idsp.csv',
    'vehicle_registration': 'master-data-state-vehicle-class-and-fuel-type-wise-total-number-of-vehicles-registered-in-each-month-in-india.csv',
    'population': 'population-projection-of-india-state-and-gender-wise-yearly-projected-urban-population-2011-2036.xlsx'
}

def count_file_rows(file_path):
    """Count rows in a file (excluding header)"""
    try:
        if file_path.endswith('.xlsx'):
            import pandas as pd
            df = pd.read_excel(file_path)
            return len(df)
        else:
            with open(file_path, 'rb') as f:
                return sum(1 for _ in f) - 1
    except Exception as e:
        return f"Error: {e}"

def count_db_rows(table_name):
    """Count rows in a database table"""
    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        conn.close()
        return count
    except Exception as e:
        return f"Error: {e}"

def main():
    print("=" * 80)
    print("DATA VERIFICATION REPORT")
    print("=" * 80)
    print(f"{'Table Name':<25} | {'Source Rows':>15} | {'DB Rows':>15} | {'Status':>10}")
    print("-" * 80)
    
    all_match = True
    
    for table, filename in FILES.items():
        file_path = os.path.join(BASE_PATH, filename)
        
        source_count = count_file_rows(file_path)
        db_count = count_db_rows(table)
        
        if isinstance(source_count, int) and isinstance(db_count, int):
            if source_count == db_count:
                status = "MATCH"
            else:
                status = "MISMATCH"
                all_match = False
        else:
            status = "ERROR"
            all_match = False
        
        src_str = f"{source_count:,}" if isinstance(source_count, int) else str(source_count)[:15]
        db_str = f"{db_count:,}" if isinstance(db_count, int) else str(db_count)[:15]
        
        print(f"{table:<25} | {src_str:>15} | {db_str:>15} | {status:>10}")
    
    print("=" * 80)
    
    if all_match:
        print("\n[SUCCESS] All tables verified - Data integrity confirmed!")
        print("You can now connect Power BI to the MySQL database.")
    else:
        print("\n[WARNING] Some tables have mismatched counts. Please review.")
    
    print("\nDatabase: airpure_aqi_db")
    print("Tables: aqi_daily, disease_outbreak, vehicle_registration, population")

if __name__ == "__main__":
    main()
