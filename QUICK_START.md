# Quick Start Guide - Database Setup and Power BI Dashboard

## ✅ What's Ready

I've created all the necessary files for your AQI Analytics project:

### Database Files
1. ✅ **database_schema.sql** - Complete MySQL schema with 8 tables
2. ✅ **create_analytical_views.sql** - 10+ analytical views for dashboard
3. ✅ **etl_aqi_data.py** - Python script to load all data

### Documentation
4. ✅ **DATABASE_SETUP_GUIDE.md** - Step-by-step setup instructions
5. ✅ **requirements_summary.md** - Complete requirements documentation

---

## 🚀 Next Steps (Follow in Order)

### Step 1: Update MySQL Password

Edit `scripts/python/etl_aqi_data.py` (Line 24):

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'YOUR_PASSWORD_HERE',  # ← Change this!
    'database': 'airpure_aqi_db',
    'port': 3306
}
```

---

### Step 2: Run the ETL Script

Open PowerShell and run:

```powershell
cd d:\FEB_AQI_P2\scripts\python
python etl_aqi_data.py
```

**What this does**:
- Creates database `airpure_aqi_db`
- Creates all tables (dim_state, dim_city, dim_date, fact_aqi_daily, etc.)
- Loads ~500K+ AQI records
- Loads disease, vehicle, and population data
- Takes ~5-10 minutes depending on your system

---

### Step 3: Create Analytical Views

After ETL completes successfully, run in MySQL Workbench:

1. Open MySQL Workbench
2. Connect to localhost
3. Open file: `database/queries/create_analytical_views.sql`
4. Click ⚡ Execute
5. All views will be created

---

### Step 4: Verify Data

Run these queries in MySQL Workbench to verify:

```sql
USE airpure_aqi_db;

-- Check record counts
SELECT 
    'dim_state' as table_name, COUNT(*) as records FROM dim_state
UNION ALL
SELECT 'dim_city', COUNT(*) FROM dim_city
UNION ALL
SELECT 'fact_aqi_daily', COUNT(*) FROM fact_aqi_daily
UNION ALL
SELECT 'fact_disease_outbreak', COUNT(*) FROM fact_disease_outbreak
UNION ALL
SELECT 'fact_vehicle_registration', COUNT(*) FROM fact_vehicle_registration;

-- Test analytical views
SELECT * FROM vw_top_bottom_areas_aqi LIMIT 10;
SELECT * FROM vw_weekend_vs_weekday_aqi;
SELECT * FROM vw_ev_adoption_vs_aqi;
```

---

### Step 5: Connect Power BI

1. **Install MySQL ODBC Driver**:
   - Download from: https://dev.mysql.com/downloads/connector/odbc/
   - Install "MySQL Connector/ODBC 8.x" (64-bit)

2. **Open Power BI Desktop**

3. **Get Data**:
   - Click "Get Data" > "More"
   - Search for "MySQL database"
   - Click "Connect"

4. **Connection Settings**:
   - Server: `localhost`
   - Database: `airpure_aqi_db`
   - Click OK

5. **Credentials**:
   - Username: `root`
   - Password: Your MySQL password
   - Click "Connect"

6. **Select Tables**:
   - Check all tables starting with `dim_` and `fact_`
   - Check all views starting with `vw_`
   - Click "Load"

---

### Step 6: Build Dashboard

I'll help you build the dashboard once data is loaded into Power BI!

---

## 📊 Dashboard Pages (Planned)

1. **Executive Summary** - National AQI, top cities, trends
2. **Severity Ranking** - Top/bottom cities by AQI
3. **Health Correlation** - Disease vs AQI analysis
4. **Market Analysis** - Target cities and demand estimation
5. **Pollutant Analysis** - Which pollutants where
6. **Vehicle Impact** - EV adoption vs AQI
7. **Weekend Analysis** - Metro cities patterns
8. **Critical Insights** - Business recommendations

---

## 🆘 Troubleshooting

### "Can't connect to MySQL server"
- Make sure MySQL service is running
-  Check Windows Services for "MySQL" service

### "Access denied for user 'root'"
- Update password in `etl_aqi_data.py`
- Make sure MySQL password is correct

### "Module not found: pandas/pymysql"
- Run: `pip install -r requirements.txt`

### "File not found" during ETL
- Verify CSV files are in: `d:\FEB_AQI_P2\AQI_dataset_Original\Dataful_Datasets\`

---

## 📞 Ready to Proceed?

Tell me when you:
1. ✅ Updated the MySQL password in ETL script
2. ⏳ Are ready to run the ETL (I can help troubleshoot)
3. ⏳ Have installed Power BI Desktop
4. ⏳ Are ready to build the dashboard

---

*Created: February 1, 2026*
