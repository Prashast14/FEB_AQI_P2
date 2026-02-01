# AirPure Innovations - Power BI Dashboard Plan
## Aligned with Primary & Secondary Analysis Questions

---

## Overview

**Project:** Market Fit Research for Air Purifier Development  
**Data Source:** MySQL database `airpure_aqi_db` via ODBC `FEB_AQI_P2_DB`  
**Cross-verification:** `primary_analysis_results.txt`

---

## Page Structure

| Page | Question | Focus |
|------|----------|-------|
| 1 | Q1 | Top/Bottom 5 Areas by AQI |
| 2 | Q2 | Pollutants in Southern States |
| 3 | Q3 | Weekend vs Weekday Analysis |
| 4 | Q4 | Worst Months for Air Quality |
| 5 | Q5 | Bengaluru Air Quality |
| 6 | Q6 | Disease vs AQI Correlation |
| 7 | Q7 | EV Adoption vs AQI |
| 8 | Summary | Executive Overview |

---

## Page 1: Top 5 & Bottom 5 Areas (Q1)

**Question:** List the top 5 and bottom 5 areas with highest average AQI (Dec 2024 - May 2025)

### Visuals:
1. **Clustered Bar Chart** - Top 5 Worst Areas
   - Y-Axis: `area`
   - X-Axis: `aqi_value` (Average)
   - Filter: Date between Dec 2024 - May 2025
   - Top N: 5

2. **Clustered Bar Chart** - Top 5 Best Areas
   - Same but Bottom N: 5

3. **Card** - Date range filter applied

### DAX Measures:
```dax
Avg AQI = AVERAGE(aqi_daily[aqi_value])
```

### Expected Values (from primary_analysis_results.txt):
- Worst: Byrnihat (265.3), Delhi (227.0), Hajipur (217.1)
- Best: Tirunelveli (33.2), Madikeri (40.2)

---

## Page 2: Southern States Pollutants (Q2)

**Question:** List top 2 and bottom 2 prominent pollutants for each state of southern India (2022+)

### Visuals:
1. **Stacked Bar Chart** - Pollutant frequency by state
   - Y-Axis: `state` (filtered to Karnataka, Tamil Nadu, Kerala, Andhra Pradesh, Telangana, Puducherry)
   - X-Axis: Count
   - Legend: `prominent_pollutants`

2. **Table** - Top/Bottom pollutants summary

### Slicer:
- State selector (Southern states only)
- Date filter (2022+)

### Expected Values:
- Karnataka: PM10 (top), CO (2nd)
- Tamil Nadu: PM10, PM2.5
- Kerala: PM10, PM2.5

---

## Page 3: Weekend vs Weekday (Q3)

**Question:** Does AQI improve on weekends vs weekdays in metro cities? (last 1 year)

### Visuals:
1. **Grouped Bar Chart**
   - Y-Axis: Metro cities (Delhi, Mumbai, Chennai, Kolkata, Bengaluru, Hyderabad, Ahmedabad, Pune)
   - X-Axis: `aqi_value` (Average)
   - Legend: Weekend/Weekday

2. **Card** - Overall weekend improvement

### DAX Measures:
```dax
Is Weekend = IF(WEEKDAY(aqi_daily[date], 2) >= 6, "Weekend", "Weekday")
Weekend Improvement = [Weekday AQI] - [Weekend AQI]
```

### Expected Values:
- Delhi: 9.1 points better on weekends
- Overall: Slight weekend improvement (0.7 points)

---

## Page 4: Worst Months for Air Quality (Q4)

**Question:** Which months consistently show worst air quality? (Top 10 states)

### Visuals:
1. **Heatmap** (Matrix visual)
   - Rows: Months
   - Columns: States
   - Values: `aqi_value` (Average)
   - Conditional formatting: Red (high) to Green (low)

2. **Line Chart** - Monthly AQI trend

### Expected Values:
- Worst: November (182.5), December (174.4), January (167.0)
- Best: August (66.9), July (68.8)

---

## Page 5: Bengaluru Analysis (Q5)

**Question:** How many days fell under each air quality category in Bengaluru? (Mar-May 2025)

### Visuals:
1. **Donut Chart** - Days by category
   - Values: Count of days
   - Legend: `air_quality_status`

2. **Table** - Category breakdown with percentages

### Filter:
- `area` = Bengaluru
- Date: Mar 2025 - May 2025

### Expected Values:
- Satisfactory: 74 days (80.4%)
- Moderate: 13 days (14.1%)
- Good: 5 days (5.4%)

---

## Page 6: Disease vs AQI Correlation (Q6)

**Question:** Top 2 disease outbreaks per state with corresponding average AQI (last 3 years)

### Visuals:
1. **Scatter Plot**
   - X-Axis: Average AQI by state
   - Y-Axis: Disease cases (sum)
   - Size: Deaths
   - Legend: State

2. **Table**
   - Columns: State, Top Disease #1, Top Disease #2, Avg AQI, Total Cases

### Expected Values:
- Acute Diarrheal Disease is #1 in most states
- Higher AQI states (Bihar 149.8, Jharkhand 162.1) correlate with more cases

---

## Page 7: EV Adoption Impact (Q7)

**Question:** Compare AQI of top 5 EV adoption states with low EV adoption states

### Visuals:
1. **Grouped Bar Chart**
   - Categories: High EV States, Low EV States
   - Values: Average AQI

2. **Table** - State-wise EV registrations and AQI

3. **Card** - Key insight (difference in AQI)

### DAX:
```dax
High EV States = {"Uttar Pradesh", "Maharashtra", "Karnataka", "Delhi", "Bihar"}
Low EV States = {"Ladakh", "Arunachal Pradesh", "Nagaland", "Lakshadweep", "Sikkim"}
```

### Expected Values:
- High EV states: 141.9 avg AQI
- Low EV states: 64.1 avg AQI
- Insight: High EV states have WORSE AQI (due to population/industrialization)

---

## Page 8: Executive Summary

### KPI Cards:
| KPI | Measure | Table |
|-----|---------|-------|
| National Avg AQI | AVERAGE(aqi_value) | aqi_daily |
| Cities Monitored | DISTINCTCOUNT(area) | aqi_daily |
| Total Disease Cases | SUM(cases) | disease_outbreak |
| EV Registrations | SUM(value) where fuel='Electric' | vehicle_registration |

### Visuals:
1. **Map** - India with AQI by state
2. **Line Chart** - AQI trend over time
3. **Key Insights** - Text boxes with findings

---

## Color Theme

| AQI Level | Range | Color |
|-----------|-------|-------|
| Good | 0-50 | #00B050 (Green) |
| Satisfactory | 51-100 | #92D050 (Light Green) |
| Moderate | 101-200 | #FFFF00 (Yellow) |
| Poor | 201-300 | #FFC000 (Orange) |
| Very Poor | 301-400 | #FF0000 (Red) |
| Severe | 400+ | #7030A0 (Purple) |

---

## Filters to Add (All Pages)

1. **Date Range** slicer
2. **State** slicer
3. **City/Area** slicer

---

## Verification Checklist

After building each page, verify against:
- `D:\FEB_AQI_P2\primary_analysis_results.txt`

| Page | Expected Value | Power BI Value | Match? |
|------|---------------|----------------|--------|
| 1 | Byrnihat = 265.3 | | |
| 2 | Karnataka PM10 = 16231 | | |
| 3 | Delhi weekend = 193.4 | | |
| 4 | November = 182.5 | | |
| 5 | Satisfactory = 74 days | | |
| 6 | Bihar AQI = 149.8 | | |
| 7 | High EV avg = 141.9 | | |
