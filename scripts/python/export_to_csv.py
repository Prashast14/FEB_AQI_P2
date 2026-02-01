"""
Export MySQL data to CSV for Power BI import
"""
import pandas as pd
from sqlalchemy import create_engine
import os

engine = create_engine('mysql+pymysql://root:admin@localhost:3306/airpure_aqi_db')
output_dir = r'd:\FEB_AQI_P2\powerbi_data'
os.makedirs(output_dir, exist_ok=True)

tables = ['aqi_daily', 'disease_outbreak', 'vehicle_registration', 'population']

for table in tables:
    print(f'Exporting {table}...')
    df = pd.read_sql(f'SELECT * FROM {table}', engine)
    df.to_csv(f'{output_dir}/{table}.csv', index=False)
    print(f'  Saved {len(df):,} rows to {table}.csv')

print('\nExport complete!')
print(f'Files saved to: {output_dir}')
