import pymysql

# Connect to database
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='admin',
    database='airpure_aqi_db'
)

cursor = conn.cursor()

# Check all tables
tables = [
    'dim_state',
    'dim_city', 
    'dim_date',
    'dim_pollutant',
    'dim_population',
    'fact_aqi_daily',
    'fact_disease_outbreak',
    'fact_vehicle_registration'
]

print("="*60)
print("DATABASE RECORD COUNTS")
print("="*60)

for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    print(f"{table:30} {count:>10,} records")

print("="*60)

conn.close()
