"""
AirPure Innovations - AQI Analytics ETL Script
Purpose: Extract, Transform, Load data from CSV/Excel to MySQL database
Created: February 1, 2026
Author: Prashast Maurya
"""

import pandas as pd
import pymysql
from sqlalchemy import create_engine
import os
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# =====================================================
# Configuration
# =====================================================

# Database connection parameters
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Change if different
    'password': '',  # UPDATE THIS WITH YOUR MYSQL PASSWORD
    'database': 'airpure_aqi_db',
    'port': 3306
}

# Data file paths
BASE_PATH = r'd:\FEB_AQI_P2\AQI_dataset_Original\Dataful_Datasets'

FILES = {
    'aqi': 'day-wise-state-wise-air-quality-index-aqi-of-major-cities-and-towns-in-india.csv',
    'disease': 'master-data-state-district-and-disease-wise-cases-and-death-reported-due-to-outbreak-of-diseases-as-per-weekly-reports-under-idsp.csv',
    'vehicle': 'master-data-state-vehicle-class-and-fuel-type-wise-total-number-of-vehicles-registered-in-each-month-in-india.csv',
    'population': 'population-projection-of-india-state-and-gender-wise-yearly-projected-urban-population-2011-2036.xlsx'
}

# Metro cities list
METRO_CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Kolkata', 'Bengaluru', 
                'Bangalore', 'Hyderabad', 'Ahmedabad', 'Pune']

# Region mapping for states
STATE_REGIONS = {
    'North': ['Delhi', 'Haryana', 'Punjab', 'Himachal Pradesh', 'Jammu and Kashmir', 
              'Uttarakhand', 'Uttar Pradesh', 'Rajasthan', 'Chandigarh'],
    'South': ['Karnataka', 'Tamil Nadu', 'Kerala', 'Andhra Pradesh', 'Telangana', 
              'Puducherry', 'Lakshadweep'],
    'East': ['West Bengal', 'Odisha', 'Bihar', 'Jharkhand', 'Assam', 
             'Andaman and Nicobar Islands'],
    'West': ['Maharashtra', 'Gujarat', 'Goa', 'Daman and Diu', 'Dadra and Nagar Haveli'],
    'Central': ['Madhya Pradesh', 'Chhattisgarh'],
    'Northeast': ['Arunachal Pradesh', 'Manipur', 'Meghalaya', 'Mizoram', 
                  'Nagaland', 'Sikkim', 'Tripura']
}

# City tier classification (simplified - can be expanded)
TIER1_CITIES = ['Delhi', 'Mumbai', 'Bangalore', 'Bengaluru', 'Chennai', 'Kolkata', 
                'Hyderabad', 'Pune', 'Ahmedabad']
TIER2_CITIES = ['Jaipur', 'Lucknow', 'Kanpur', 'Nagpur', 'Indore', 'Bhopal', 
                'Visakhapatnam', 'Patna', 'Vadodara', 'Ludhiana', 'Agra', 
                'Nashik', 'Faridabad', 'Meerut', 'Rajkot', 'Varanasi', 
                'Srinagar', 'Amritsar', 'Allahabad', 'Ranchi', 'Gwalior', 'Coimbatore']

# =====================================================
# Database Connection
# =====================================================

def create_db_engine():
    """Create SQLAlchemy engine for database connection"""
    try:
        connection_string = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
        engine = create_engine(connection_string, echo=False)
        print("✅ Database connection established successfully!")
        return engine
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        return None

def execute_sql_file(engine, sql_file_path):
    """Execute SQL file to create schema"""
    try:
        with open(sql_file_path, 'r', encoding='utf-8') as file:
            sql_script = file.read()
        
        # Split by semicolon and execute each statement
        statements = [stmt.strip() for stmt in sql_script.split(';') if stmt.strip()]
        
        with engine.connect() as conn:
            for stmt in statements:
                if stmt and not stmt.startswith('--'):
                    conn.execute(stmt)
        
        print(f"✅ SQL schema executed successfully from {sql_file_path}")
        return True
    except Exception as e:
        print(f"❌ Error executing SQL file: {e}")
        return False

# =====================================================
# Dimension Table Population
# =====================================================

def generate_date_dimension(engine, start_date='2022-01-01', end_date='2026-12-31'):
    """Generate date dimension table"""
    print("\n📅 Generating Date Dimension...")
    
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    date_data = []
    for date in date_range:
        date_data.append({
            'date_value': date.date(),
            'year': date.year,
            'quarter': date.quarter,
            'month': date.month,
            'month_name': date.strftime('%B'),
            'week': date.isocalendar()[1],
            'day_of_month': date.day,
            'day_of_week': date.dayofweek + 1,  # 1=Monday, 7=Sunday
            'day_name': date.strftime('%A'),
            'is_weekend': 1 if date.dayofweek >= 5 else 0  # Saturday=5, Sunday=6
        })
    
    df_date = pd.DataFrame(date_data)
    
    # Insert to database
    df_date.to_sql('dim_date', engine, if_exists='append', index=False, method='multi', chunksize=1000)
    
    print(f"✅ Date dimension populated: {len(df_date)} records")
    return df_date

def get_region_for_state(state_name):
    """Get region for a given state"""
    for region, states in STATE_REGIONS.items():
        if state_name in states:
            return region
    return 'Other'

def get_city_tier(city_name):
    """Get tier classification for city"""
    if city_name in TIER1_CITIES:
        return 'Tier 1'
    elif city_name in TIER2_CITIES:
        return 'Tier 2'
    else:
        return 'Tier 3'

def is_metro(city_name):
    """Check if city is metro"""
    return 1 if city_name in METRO_CITIES else 0

# =====================================================
# ETL Functions
# =====================================================

def load_aqi_data(engine):
    """Load AQI daily data"""
    print("\n🌍 Loading AQI Daily Data...")
    
    file_path = os.path.join(BASE_PATH, FILES['aqi'])
    
    # Read CSV
    df = pd.read_csv(file_path, encoding='utf-8')
    
    print(f"📊 Raw records: {len(df)}")
    print(f"📊 Columns: {df.columns.tolist()}")
    
    # Clean column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # Parse date
    df['date_value'] = pd.to_datetime(df['date'], format='%d-%m-%Y', errors='coerce')
    
    # Clean state and area names
    df['state'] = df['state'].str.strip()
    df['area'] = df['area'].str.strip()
    
    # Get unique states and cities
    unique_states = df['state'].unique()
    unique_cities = df[['area', 'state']].drop_duplicates()
    
    # Populate dim_state
    print("\n📍 Populating State Dimension...")
    states_data = []
    for state in unique_states:
        states_data.append({
            'state_name': state,
            'region': get_region_for_state(state)
        })
    
    df_states = pd.DataFrame(states_data)
    df_states.to_sql('dim_state', engine, if_exists='append', index=False, method='multi')
    print(f"✅ States populated: {len(df_states)} records")
    
    # Get state_id mapping
    state_mapping = pd.read_sql("SELECT state_id, state_name FROM dim_state", engine)
    state_dict = dict(zip(state_mapping['state_name'], state_mapping['state_id']))
    
    # Populate dim_city
    print("\n🏙️ Populating City Dimension...")
    cities_data = []
    for _, row in unique_cities.iterrows():
        cities_data.append({
            'city_name': row['area'],
            'state_id': state_dict.get(row['state']),
            'city_tier': get_city_tier(row['area']),
            'is_metro': is_metro(row['area'])
        })
    
    df_cities = pd.DataFrame(cities_data)
    df_cities.to_sql('dim_city', engine, if_exists='append', index=False, method='multi')
    print(f"✅ Cities populated: {len(df_cities)} records")
    
    # Get city_id and date_id mappings
    city_mapping = pd.read_sql("SELECT city_id, city_name, state_id FROM dim_city", engine)
    date_mapping = pd.read_sql("SELECT date_id, date_value FROM dim_date", engine)
    date_mapping['date_value'] = pd.to_datetime(date_mapping['date_value'])
    
    # Prepare fact table data
    df = df.merge(state_mapping, left_on='state', right_on='state_name', how='left')
    df = df.merge(city_mapping, left_on=['area', 'state_id'], right_on=['city_name', 'state_id'], how='left')
    df = df.merge(date_mapping, left_on='date_value', right_on='date_value', how='left')
    
    # Select and rename columns for fact table
    fact_columns = {
        'date_id': 'date_id',
        'state_id': 'state_id',
        'city_id': 'city_id',
        'date_value': 'date_value',
        'state': 'state_name',
        'area': 'city_name',
        'number_of_monitoring_stations': 'number_of_monitoring_stations',
        'prominent_pollutants': 'prominent_pollutants',
        'aqi_value': 'aqi_value',
        'air_quality_status': 'air_quality_status',
        'unit': 'unit',
        'note': 'note'
    }
    
    df_fact = df[list(fact_columns.keys())].rename(columns=fact_columns)
    
    # Handle missing values
    df_fact['aqi_value'] = pd.to_numeric(df_fact['aqi_value'], errors='coerce')
    df_fact = df_fact.dropna(subset=['date_id', 'state_id', 'city_id'])
    
    # Load to database in chunks
    print("\n💾 Loading AQI fact data...")
    df_fact.to_sql('fact_aqi_daily', engine, if_exists='append', index=False, method='multi', chunksize=5000)
    
    print(f"✅ AQI fact data loaded: {len(df_fact)} records")
    
    return df_fact

def load_disease_data(engine):
    """Load disease outbreak data"""
    print("\n🏥 Loading Disease Outbreak Data...")
    
    file_path = os.path.join(BASE_PATH, FILES['disease'])
    
    # Read CSV
    df = pd.read_csv(file_path, encoding='utf-8')
    
    print(f"📊 Raw records: {len(df)}")
    
    # Clean column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # Parse dates
    df['outbreak_starting_date'] = pd.to_datetime(df['outbreak_starting_date'], format='%d-%m-%Y', errors='coerce')
    df['reporting_date'] = pd.to_datetime(df['reporting_date'], format='%d-%m-%Y', errors='coerce')
    
    # Clean state names
    df['state'] = df['state'].str.strip()
    
    # Get state_id mapping
    state_mapping = pd.read_sql("SELECT state_id, state_name FROM dim_state", engine)
    state_dict = dict(zip(state_mapping['state_name'], state_mapping['state_id']))
    
    df['state_id'] = df['state'].map(state_dict)
    
    # Select columns for fact table
    fact_columns = {
        'year': 'year',
        'week': 'week',
        'outbreak_starting_date': 'outbreak_starting_date',
        'reporting_date': 'reporting_date',
        'state_id': 'state_id',
        'state': 'state_name',
        'district': 'district',
        'disease_/_illness_name': 'disease_illness_name',
        'status': 'status',
        'cases': 'cases',
        'deaths': 'deaths',
        'unit': 'unit',
        'note': 'note'
    }
    
    df_fact = df[list(fact_columns.keys())].rename(columns=fact_columns)
    
    # Handle missing values
    df_fact['cases'] = pd.to_numeric(df_fact['cases'], errors='coerce').fillna(0).astype(int)
    df_fact['deaths'] = pd.to_numeric(df_fact['deaths'], errors='coerce').fillna(0).astype(int)
    
    # Load to database
    print("\n💾 Loading disease fact data...")
    df_fact.to_sql('fact_disease_outbreak', engine, if_exists='append', index=False, method='multi', chunksize=5000)
    
    print(f"✅ Disease fact data loaded: {len(df_fact)} records")
    
    return df_fact

def load_vehicle_data(engine):
    """Load vehicle registration data"""
    print("\n🚗 Loading Vehicle Registration Data...")
    
    file_path = os.path.join(BASE_PATH, FILES['vehicle'])
    
    # Read CSV
    df = pd.read_csv(file_path, encoding='utf-8')
    
    print(f"📊 Raw records: {len(df)}")
    
    # Clean column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # Clean state names
    df['state'] = df['state'].str.strip()
    
    # Get state_id mapping
    state_mapping = pd.read_sql("SELECT state_id, state_name FROM dim_state", engine)
    state_dict = dict(zip(state_mapping['state_name'], state_mapping['state_id']))
    
    df['state_id'] = df['state'].map(state_dict)
    
    # Select columns for fact table
    fact_columns = {
        'year': 'year',
        'month': 'month',
        'state_id': 'state_id',
        'state': 'state_name',
        'rto': 'rto',
        'vehicle_class': 'vehicle_class',
        'fuel': 'fuel',
        'value': 'value',
        'unit': 'unit',
        'note': 'note'
    }
    
    df_fact = df[list(fact_columns.keys())].rename(columns=fact_columns)
    
    # Handle missing values
    df_fact['value'] = pd.to_numeric(df_fact['value'], errors='coerce').fillna(0).astype(int)
    
    # Load to database
    print("\n💾 Loading vehicle fact data...")
    df_fact.to_sql('fact_vehicle_registration', engine, if_exists='append', index=False, method='multi', chunksize=5000)
    
    print(f"✅ Vehicle fact data loaded: {len(df_fact)} records")
    
    return df_fact

def load_population_data(engine):
    """Load population projection data"""
    print("\n👥 Loading Population Projection Data...")
    
    file_path = os.path.join(BASE_PATH, FILES['population'])
    
    # Read Excel
    df = pd.read_excel(file_path)
    
    print(f"📊 Raw records: {len(df)}")
    
    # Clean column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # Clean state names
    df['state'] = df['state'].str.strip()
    
    # Get state_id mapping
    state_mapping = pd.read_sql("SELECT state_id, state_name FROM dim_state", engine)
    state_dict = dict(zip(state_mapping['state_name'], state_mapping['state_id']))
    
    df['state_id'] = df['state'].map(state_dict)
    
    # Select columns for dimension table
    dim_columns = {
        'state_id': 'state_id',
        'year': 'year',
        'month': 'month',
        'gender': 'gender',
        'value': 'population_thousands'
    }
    
    df_dim = df[list(dim_columns.keys())].rename(columns=dim_columns)
    
    # Handle missing values
    df_dim['population_thousands'] = pd.to_numeric(df_dim['population_thousands'], errors='coerce')
    df_dim = df_dim.dropna(subset=['state_id'])
    
    # Load to database
    print("\n💾 Loading population dimension data...")
    df_dim.to_sql('dim_population', engine, if_exists='append', index=False, method='multi', chunksize=5000)
    
    print(f"✅ Population dimension data loaded: {len(df_dim)} records")
    
    return df_dim

# =====================================================
# Main Execution
# =====================================================

def main():
    """Main ETL execution function"""
    print("="*60)
    print("🚀 AirPure Innovations - AQI Analytics ETL")
    print("="*60)
    
    # Create database engine
    engine = create_db_engine()
    if not engine:
        print("❌ Failed to create database engine. Exiting.")
        return
    
    # Execute schema SQL
    schema_file = r'd:\FEB_AQI_P2\database\schema\database_schema.sql'
    print(f"\n📂 Executing schema from: {schema_file}")
    
    if not execute_sql_file(engine, schema_file):
        print("❌ Failed to execute schema. Exiting.")
        return
    
    try:
        # Generate date dimension
        generate_date_dimension(engine)
        
        # Load fact and dimension data
        load_aqi_data(engine)
        load_disease_data(engine)
        load_vehicle_data(engine)
        load_population_data(engine)
        
        print("\n"+"="*60)
        print("✅ ETL Process Completed Successfully!")
        print("="*60)
        
        # Print summary statistics
        print("\n📊 Database Summary:")
        with engine.connect() as conn:
            tables = ['dim_state', 'dim_city', 'dim_date', 'fact_aqi_daily', 
                     'fact_disease_outbreak', 'fact_vehicle_registration', 'dim_population']
            
            for table in tables:
                result = conn.execute(f"SELECT COUNT(*) as count FROM {table}")
                count = result.fetchone()[0]
                print(f"   {table}: {count:,} records")
        
    except Exception as e:
        print(f"\n❌ Error during ETL: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        engine.dispose()
        print("\n🔒 Database connection closed")

if __name__ == "__main__":
    main()
