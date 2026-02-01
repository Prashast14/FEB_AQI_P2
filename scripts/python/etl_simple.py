"""
AirPure AQI Analytics - Simple ETL Script
==========================================
Loads all source CSV/Excel files directly into MySQL tables.
No complex transformations - just clean loading for Power BI.
"""

import pandas as pd
import pymysql
from sqlalchemy import create_engine
import os
import sys

# =====================================================
# Configuration
# =====================================================

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'admin',
    'database': 'airpure_aqi_db',
    'port': 3306
}

BASE_PATH = r'd:\FEB_AQI_P2\AQI_dataset_Original\Dataful_Datasets'

FILES = {
    'aqi_daily': {
        'file': 'day-wise-state-wise-air-quality-index-aqi-of-major-cities-and-towns-in-india.csv',
        'type': 'csv',
        'encoding': 'utf-8'
    },
    'disease_outbreak': {
        'file': 'master-data-state-district-and-disease-wise-cases-and-death-reported-due-to-outbreak-of-diseases-as-per-weekly-reports-under-idsp.csv',
        'type': 'csv',
        'encoding': 'latin-1'
    },
    'vehicle_registration': {
        'file': 'master-data-state-vehicle-class-and-fuel-type-wise-total-number-of-vehicles-registered-in-each-month-in-india.csv',
        'type': 'csv',
        'encoding': 'utf-8'
    },
    'population': {
        'file': 'population-projection-of-india-state-and-gender-wise-yearly-projected-urban-population-2011-2036.xlsx',
        'type': 'excel',
        'encoding': None
    }
}

# Column mapping from source to database
COLUMN_MAPPING = {
    'aqi_daily': {
        'date': 'date',
        'state': 'state',
        'area': 'area',
        'number_of_monitoring_stations': 'monitoring_stations',
        'prominent_pollutants': 'prominent_pollutants',
        'aqi_value': 'aqi_value',
        'air_quality_status': 'air_quality_status',
        'unit': 'unit',
        'note': 'note'
    },
    'disease_outbreak': {
        'year': 'year',
        'week': 'week',
        'outbreak_starting_date': 'outbreak_date',
        'reporting_date': 'reporting_date',
        'state': 'state',
        'district': 'district',
        'disease / illness name': 'disease_name',
        'status': 'status',
        'cases': 'cases',
        'deaths': 'deaths',
        'unit': 'unit',
        'note': 'note'
    },
    'vehicle_registration': {
        'year': 'year',
        'month': 'month',
        'state': 'state',
        'rto': 'rto',
        'vehicle_class': 'vehicle_class',
        'fuel': 'fuel',
        'value': 'value',
        'unit': 'unit',
        'note': 'note'
    },
    'population': {
        'state': 'state',
        'year': 'year',
        'month': 'month',
        'gender': 'gender',
        'value': 'population_thousands'
    }
}

# =====================================================
# Helper Functions
# =====================================================

def execute_schema():
    """Execute SQL schema file to create database and tables"""
    print("[1/5] Setting up database schema...")
    
    schema_file = r'd:\FEB_AQI_P2\database\schema\database_schema_v2.sql'
    
    try:
        conn = pymysql.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            port=DB_CONFIG['port'],
            autocommit=True
        )
        cursor = conn.cursor()
        
        with open(schema_file, 'r', encoding='utf-8') as f:
            sql = f.read()
        
        for statement in sql.split(';'):
            stmt = statement.strip()
            if stmt and not stmt.startswith('--'):
                try:
                    cursor.execute(stmt)
                except Exception as e:
                    if 'SELECT' not in stmt.upper():
                        print(f"  Warning: {e}")
        
        conn.close()
        print("  [OK] Database and tables created successfully")
        return True
        
    except Exception as e:
        print(f"  [ERROR] Failed to execute schema: {e}")
        return False

def get_engine():
    """Create SQLAlchemy engine"""
    connection_string = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    return create_engine(connection_string, echo=False)

def load_file(table_name, file_info, engine, column_map):
    """Load a single file into its corresponding table"""
    file_path = os.path.join(BASE_PATH, file_info['file'])
    
    print(f"\n  Loading: {file_info['file'][:50]}...")
    
    # Read file
    try:
        if file_info['type'] == 'csv':
            df = pd.read_csv(file_path, encoding=file_info['encoding'])
        else:
            df = pd.read_excel(file_path)
    except UnicodeDecodeError:
        print(f"    Retrying with latin-1 encoding...")
        df = pd.read_csv(file_path, encoding='latin-1')
    
    print(f"    Source records: {len(df):,}")
    
    # Clean column names (lowercase, strip whitespace)
    df.columns = df.columns.str.strip().str.lower()
    
    # Rename columns to match database schema
    rename_map = {}
    for src_col, db_col in column_map.items():
        src_col_clean = src_col.lower().strip()
        if src_col_clean in df.columns:
            rename_map[src_col_clean] = db_col
    
    df = df.rename(columns=rename_map)
    
    # Keep only columns that exist in mapping
    valid_cols = [col for col in column_map.values() if col in df.columns]
    df = df[valid_cols]
    
    # Parse dates for AQI data
    if table_name == 'aqi_daily' and 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y', errors='coerce')
    
    # Parse dates for disease data
    if table_name == 'disease_outbreak':
        if 'outbreak_date' in df.columns:
            df['outbreak_date'] = pd.to_datetime(df['outbreak_date'], format='%d-%m-%Y', errors='coerce')
        if 'reporting_date' in df.columns:
            df['reporting_date'] = pd.to_datetime(df['reporting_date'], format='%d-%m-%Y', errors='coerce')
    
    # Load to database in chunks
    chunk_size = 5000
    total_chunks = (len(df) // chunk_size) + 1
    
    for i in range(0, len(df), chunk_size):
        chunk = df.iloc[i:i+chunk_size]
        chunk.to_sql(table_name, engine, if_exists='append', index=False)
        current_chunk = (i // chunk_size) + 1
        print(f"    Chunk {current_chunk}/{total_chunks} loaded ({len(chunk):,} records)", end='\r')
    
    print(f"    [OK] Loaded {len(df):,} records to {table_name}                    ")
    return len(df)

# =====================================================
# Main Execution
# =====================================================

def main():
    print("=" * 60)
    print("AirPure AQI Analytics - ETL Process")
    print("=" * 60)
    
    # Step 1: Create database schema
    if not execute_schema():
        print("\n[FAILED] Could not create database. Exiting.")
        sys.exit(1)
    
    # Step 2: Connect to database
    print("\n[2/5] Connecting to database...")
    try:
        engine = get_engine()
        print("  [OK] Connected to MySQL")
    except Exception as e:
        print(f"  [ERROR] Connection failed: {e}")
        sys.exit(1)
    
    # Step 3-6: Load each file
    results = {}
    step = 2
    
    for table_name, file_info in FILES.items():
        step += 1
        print(f"\n[{step}/5] Processing {table_name}...")
        try:
            count = load_file(table_name, file_info, engine, COLUMN_MAPPING[table_name])
            results[table_name] = count
        except Exception as e:
            print(f"  [ERROR] Failed to load {table_name}: {e}")
            results[table_name] = f"ERROR: {e}"
    
    # Summary
    print("\n" + "=" * 60)
    print("ETL COMPLETE - Summary")
    print("=" * 60)
    
    for table, count in results.items():
        if isinstance(count, int):
            print(f"  {table:25} {count:>12,} records")
        else:
            print(f"  {table:25} {count}")
    
    print("=" * 60)
    print("\nNext step: Run verify_counts.py to validate data integrity")
    
    engine.dispose()

if __name__ == "__main__":
    main()
