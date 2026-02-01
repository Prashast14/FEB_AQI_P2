# Power BI MySQL Connection Guide

## Prerequisites

1. **MySQL ODBC Driver** - Download and install from:
   https://dev.mysql.com/downloads/connector/odbc/

2. **Power BI Desktop** - Latest version installed

---

## Step 1: Install MySQL ODBC Driver

1. Go to: https://dev.mysql.com/downloads/connector/odbc/
2. Download **MySQL Connector/ODBC 8.0** (64-bit)
3. Run the installer and complete setup
4. Restart your computer if prompted

---

## Step 2: Connect Power BI to MySQL

### Option A: Direct MySQL Connection

1. Open **Power BI Desktop**
2. Click **Get Data** > **More...**
3. Search for **MySQL database**
4. Click **Connect**
5. Enter connection details:
   - **Server:** `localhost`
   - **Database:** `airpure_aqi_db`
6. Select **DirectQuery** or **Import** mode
7. Enter credentials:
   - **Username:** `root`
   - **Password:** `admin`
8. Select tables to import:
   - `aqi_daily`
   - `disease_outbreak`
   - `vehicle_registration`
   - `population`

### Option B: Using ODBC (if Direct fails)

1. Open **Control Panel** > **ODBC Data Sources (64-bit)**
2. Click **Add** > Select **MySQL ODBC 8.0 Unicode Driver**
3. Configure:
   - **Data Source Name:** `AirPure_AQI`
   - **TCP/IP Server:** `localhost`
   - **Port:** `3306`
   - **User:** `root`
   - **Password:** `admin`
   - **Database:** `airpure_aqi_db`
4. Click **Test** to verify
5. In Power BI: **Get Data** > **ODBC** > Select `AirPure_AQI`

---

## Step 3: Verify Data in Power BI

After connecting, you should see:
- aqi_daily: **425,971 rows**
- disease_outbreak: **26,553 rows**
- vehicle_registration: **199,552 rows**
- population: **8,892 rows**

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "MySQL connector not found" | Install MySQL ODBC driver and restart Power BI |
| "Access denied" | Check username/password (root/admin) |
| "Cannot connect" | Ensure MySQL service is running |
| "SSL error" | Add `sslmode=disabled` to connection string |

---

## Next: Dashboard Design

Once connected, we'll build these pages:
1. **Executive Summary** - KPIs, national AQI overview
2. **City Analysis** - Top/bottom cities, trends
3. **Health Correlation** - AQI vs disease outbreaks
4. **EV Impact** - EV adoption vs air quality
