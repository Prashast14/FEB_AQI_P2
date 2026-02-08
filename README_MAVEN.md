# AirPure Innovations - Air Quality Intelligence Dashboard

## 📊 Project Overview

Power BI dashboard analyzing India's air quality data. Identifies high-pollution regions, seasonal patterns & disease correlations to guide AirPure Innovations' market expansion strategy.

## 🎯 Business Challenge

AirPure Innovations, an air purifier company, needed data-driven insights to:
- Identify regions with worst air quality for targeted product launches
- Understand pollution patterns (seasonal, weekday vs weekend)
- Correlate air quality with health outcomes (disease outbreaks)
- Analyze EV adoption impact on air quality

## 📈 Dashboard Features

### Executive Summary
- **KPI Cards:** National Avg AQI (116), Total Disease Cases (232K), EV Registrations (4M), Monitoring Stations (40)
- **Interactive Date Slicer** for dynamic filtering
- **AQI Trend Analysis** showing improvement over time
- **Air Quality Distribution** across categories

### 7 Analysis Pages:
| Page | Question Answered |
|------|-------------------|
| Q1 | Top 5 worst and bottom 5 best areas by AQI |
| Q2 | Prominent pollutants in Southern states |
| Q3 | Weekday vs Weekend AQI patterns in metro cities |
| Q4 | Worst months for air quality across states |
| Q5 | Bengaluru air quality category distribution |
| Q6 | Disease outbreaks correlation with AQI levels |
| Q7 | EV adoption impact on air quality |

## 🔑 Key Insights

1. **AQI is improving** - National average declined from ~120 to ~107 (2022-2025)
2. **85% of days have acceptable air quality** (Good/Satisfactory/Moderate)
3. **Delhi has highest AQI (~190)** despite ranking in top 5 for EV registrations
4. **Winter months (Nov-Feb)** show worst air quality
5. **Acute Diarrheal Disease** is the most common outbreak correlating with poor AQI

## 🛠️ Technical Details

| Component | Technology |
|-----------|------------|
| Visualization | Power BI Desktop |
| Database | MySQL (localhost) |
| Data Processing | Python (Pandas, SQLAlchemy) |
| Data Source | Government AQI monitoring data (2015-2025) |

## 📁 Files Included

- `aqi_v2.pbix` - Power BI Dashboard
- `data/` - CSV datasets
- `scripts/` - Python ETL scripts
- `docs/` - Documentation

## 👤 Author

**Prashast Maurya**

---

*Built for Maven Analytics Portfolio Showcase*
