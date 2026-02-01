# Database Setup Guide

## Prerequisites

✅ MySQL Workbench installed  
✅ Python 3.8+ installed  
✅ Data files in `AQI_dataset_Original/Dataful_Datasets/`

---

## Step 1: Install Python Dependencies

Open PowerShell in the project directory and run:

```powershell
cd d:\FEB_AQI_P2\scripts\python
pip install -r requirements.txt
```

This will install:
- `pandas` - Data manipulation
- `pymysql` - MySQL connector
- `sqlalchemy` - Database ORM
- `openpyxl` - Excel file support
- `mysql-connector-python` - Alternative MySQL connector

---

## Step 2: Configure Database Connection

### Option A: Using MySQL Workbench (GUI)

1. Open MySQL Workbench
2. Connect to your local MySQL instance
3. Note your MySQL root password (you'll need it)

### Option B: Using Command Line

```powershell
mysql -u root -p
# Enter your password when prompted
```

---

## Step 3: Update ETL Script with Your Password

Edit `etl_aqi_data.py` and update the MySQL password:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'YOUR_MYSQL_PASSWORD_HERE',  # ← Update this
    'database': 'airpure_aqi_db',
    'port': 3306
}
```

---

## Step 4: Run the ETL Script

### Method 1: Using PowerShell

```powershell
cd d:\FEB_AQI_P2\scripts\python
python etl_aqi_data.py
```

### Method 2: Using Python IDE

1. Open `etl_aqi_data.py` in VS Code, PyCharm, or your preferred IDE
2. Run the script

---

## What the ETL Script Does

The script will:

1. ✅ **Drop and recreate** the `airpure_aqi_db` database
2. ✅ **Create tables**:
   - `dim_state` - State dimension
   - `dim_city` - City dimension with tier classification
   - `dim_date` - Date dimension (2022-2026)
   - `dim_pollutant` - Pollutant reference
   - `dim_population` - Population projections
   - `fact_aqi_daily` - Daily AQI measurements
   - `fact_disease_outbreak` - Disease outbreak data
   - `fact_vehicle_registration` - Vehicle registration data

3. ✅ **Load data** from CSV/Excel files
4. ✅ **Clean and transform** data (handle missing values, parse dates, classify cities)
5. ✅ **Create relationships** between tables

---

## Expected Output

```
============================================================
🚀 AirPure Innovations - AQI Analytics ETL
============================================================

✅ Database connection established successfully!
✅ SQL schema executed successfully

📅 Generating Date Dimension...
✅ Date dimension populated: 1,826 records

🌍 Loading AQI Daily Data...
📊 Raw records: 500,000+
📍 Populating State Dimension...
✅ States populated: 36 records
🏙️ Populating City Dimension...
✅ Cities populated: 300+ records
💾 Loading AQI fact data...
✅ AQI fact data loaded: 500,000+ records

🏥 Loading Disease Outbreak Data...
✅ Disease fact data loaded: 50,000+ records

🚗 Loading Vehicle Registration Data...
✅ Vehicle fact data loaded: 100,000+ records

👥 Loading Population Projection Data...
✅ Population dimension data loaded: 15,000+ records

============================================================
✅ ETL Process Completed Successfully!
============================================================

📊 Database Summary:
   dim_state: 36 records
   dim_city: 300+ records
   dim_date: 1,826 records
   fact_aqi_daily: 500,000+ records
   fact_disease_outbreak: 50,000+ records
   fact_vehicle_registration: 100,000+ records
   dim_population: 15,000+ records
```

---

## Step 5: Verify Data in MySQL Workbench

1. Open MySQL Workbench
2. Connect to your local MySQL instance
3. Select `airpure_aqi_db` database
4. Run sample queries:

```sql
-- Check AQI data
SELECT * FROM fact_aqi_daily LIMIT 10;

-- Check states
SELECT * FROM dim_state;

-- Check cities
SELECT * FROM dim_city WHERE is_metro = 1;

-- Check date dimension
SELECT * FROM dim_date WHERE is_weekend = 1 LIMIT 10;
```

---

## Troubleshooting

### Error: "Access denied for user 'root'@'localhost'"

**Solution**: Update the password in `DB_CONFIG` in `etl_aqi_data.py`

---

### Error: "No module named 'pandas'"

**Solution**: Install dependencies:
```powershell
pip install -r requirements.txt
```

---

### Error: "File not found"

**Solution**: Verify data files are in the correct location:
```
d:\FEB_AQI_P2\AQI_dataset_Original\Dataful_Datasets\
```

---

### Error: "Connection refused"

**Solution**: 
1. Ensure MySQL service is running
2. Check MySQL port (default: 3306)
3. Verify firewall settings

---

## Next Steps

After successful ETL:

1. ✅ Create analytical SQL views
2. ✅ Connect Power BI to MySQL
3. ✅ Build dashboards

---

*Last Updated: February 1, 2026*
