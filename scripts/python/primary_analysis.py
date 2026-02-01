"""
AirPure Innovations - Primary Analysis Script
==============================================
Answers all 7 Primary Analysis questions using CSV data.
Results can be cross-verified with Power BI dashboard.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# =====================================================
# Load Data
# =====================================================

BASE_PATH = r'd:\FEB_AQI_P2\AQI_dataset_Original\Dataful_Datasets'

print("Loading datasets...")
aqi_df = pd.read_csv(f"{BASE_PATH}/day-wise-state-wise-air-quality-index-aqi-of-major-cities-and-towns-in-india.csv")
disease_df = pd.read_csv(f"{BASE_PATH}/master-data-state-district-and-disease-wise-cases-and-death-reported-due-to-outbreak-of-diseases-as-per-weekly-reports-under-idsp.csv", encoding='latin-1')
vehicle_df = pd.read_csv(f"{BASE_PATH}/master-data-state-vehicle-class-and-fuel-type-wise-total-number-of-vehicles-registered-in-each-month-in-india.csv")

# Clean column names
aqi_df.columns = aqi_df.columns.str.strip().str.lower()
disease_df.columns = disease_df.columns.str.strip().str.lower()
vehicle_df.columns = vehicle_df.columns.str.strip().str.lower()

# Parse dates
aqi_df['date'] = pd.to_datetime(aqi_df['date'], format='%d-%m-%Y', errors='coerce')
aqi_df['aqi_value'] = pd.to_numeric(aqi_df['aqi_value'], errors='coerce')

print(f"AQI records: {len(aqi_df):,}")
print(f"Disease records: {len(disease_df):,}")
print(f"Vehicle records: {len(vehicle_df):,}")

# =====================================================
# Q1: Top 5 and bottom 5 areas with highest average AQI
#     (December 2024 to May 2025)
# =====================================================

print("\n" + "="*70)
print("Q1: TOP 5 AND BOTTOM 5 AREAS BY AVERAGE AQI (Dec 2024 - May 2025)")
print("="*70)

q1_start = datetime(2024, 12, 1)
q1_end = datetime(2025, 5, 31)
q1_df = aqi_df[(aqi_df['date'] >= q1_start) & (aqi_df['date'] <= q1_end)].copy()

if len(q1_df) > 0:
    area_avg = q1_df.groupby('area')['aqi_value'].agg(['mean', 'count']).reset_index()
    area_avg.columns = ['area', 'avg_aqi', 'data_points']
    area_avg = area_avg[area_avg['data_points'] >= 30]
    area_avg = area_avg.sort_values('avg_aqi', ascending=False)
    
    print("\n[WORST] TOP 5 AREAS (HIGHEST AQI):")
    top5 = area_avg.head(5)
    for i, row in top5.iterrows():
        print(f"   {row['area']:30} | Avg AQI: {row['avg_aqi']:.1f} | Data points: {row['data_points']}")
    
    print("\n[BEST] BOTTOM 5 AREAS (LOWEST AQI):")
    bottom5 = area_avg.tail(5).sort_values('avg_aqi')
    for i, row in bottom5.iterrows():
        print(f"   {row['area']:30} | Avg AQI: {row['avg_aqi']:.1f} | Data points: {row['data_points']}")
else:
    print("   No data available for Dec 2024 - May 2025. Checking available date range...")
    print(f"   Data range: {aqi_df['date'].min()} to {aqi_df['date'].max()}")

# =====================================================
# Q2: Top 2 and bottom 2 prominent pollutants for 
#     each state of southern India (2022 onwards)
# =====================================================

print("\n" + "="*70)
print("Q2: TOP 2 AND BOTTOM 2 POLLUTANTS FOR SOUTHERN STATES (2022+)")
print("="*70)

southern_states = ['Karnataka', 'Tamil Nadu', 'Kerala', 'Andhra Pradesh', 'Telangana', 'Puducherry']

q2_df = aqi_df[aqi_df['date'] >= datetime(2022, 1, 1)].copy()
q2_df = q2_df[q2_df['state'].isin(southern_states)]

if len(q2_df) > 0:
    for state in southern_states:
        state_df = q2_df[q2_df['state'] == state]
        if len(state_df) == 0:
            continue
            
        pollutants = state_df['prominent_pollutants'].dropna().str.split(',').explode().str.strip()
        counts = pollutants.value_counts()
        
        print(f"\n[STATE] {state}:")
        if len(counts) >= 2:
            print(f"   Top 2 pollutants:    {counts.index[0]} ({counts.iloc[0]}), {counts.index[1]} ({counts.iloc[1]})")
        if len(counts) >= 4:
            print(f"   Bottom 2 pollutants: {counts.index[-2]} ({counts.iloc[-2]}), {counts.index[-1]} ({counts.iloc[-1]})")
        elif len(counts) > 0:
            print(f"   All pollutants: {dict(counts)}")
else:
    print("   No data for southern states from 2022 onwards")

# =====================================================
# Q3: AQI on weekends vs weekdays in metro cities
#     (last 1 year)
# =====================================================

print("\n" + "="*70)
print("Q3: AQI WEEKENDS VS WEEKDAYS IN METRO CITIES (Last 1 Year)")
print("="*70)

metro_cities = ['Delhi', 'Mumbai', 'Chennai', 'Kolkata', 'Bengaluru', 'Bangalore', 
                'Hyderabad', 'Ahmedabad', 'Pune']

latest_date = aqi_df['date'].max()
one_year_ago = latest_date - pd.DateOffset(years=1)

q3_df = aqi_df[(aqi_df['date'] >= one_year_ago) & (aqi_df['area'].isin(metro_cities))].copy()
q3_df['day_of_week'] = q3_df['date'].dt.dayofweek
q3_df['is_weekend'] = q3_df['day_of_week'] >= 5

if len(q3_df) > 0:
    print(f"\n[PERIOD] {one_year_ago.strftime('%Y-%m-%d')} to {latest_date.strftime('%Y-%m-%d')}")
    print(f"\n{'City':<20} | {'Weekday Avg':<12} | {'Weekend Avg':<12} | {'Difference':<12} | {'Better On':<10}")
    print("-" * 70)
    
    for city in metro_cities:
        city_df = q3_df[q3_df['area'] == city]
        if len(city_df) > 10:
            weekday_avg = city_df[~city_df['is_weekend']]['aqi_value'].mean()
            weekend_avg = city_df[city_df['is_weekend']]['aqi_value'].mean()
            diff = weekday_avg - weekend_avg
            better = "Weekend" if diff > 0 else "Weekday"
            print(f"{city:<20} | {weekday_avg:>10.1f} | {weekend_avg:>10.1f} | {abs(diff):>10.1f} | {better:<10}")
    
    overall_weekday = q3_df[~q3_df['is_weekend']]['aqi_value'].mean()
    overall_weekend = q3_df[q3_df['is_weekend']]['aqi_value'].mean()
    print("-" * 70)
    print(f"{'OVERALL':<20} | {overall_weekday:>10.1f} | {overall_weekend:>10.1f} | {abs(overall_weekday-overall_weekend):>10.1f} | {'Weekend' if overall_weekday > overall_weekend else 'Weekday':<10}")

# =====================================================
# Q4: Which months consistently show worst air quality
#     (Top 10 states with high distinct areas)
# =====================================================

print("\n" + "="*70)
print("Q4: MONTHS WITH WORST AIR QUALITY (Top 10 States by Distinct Areas)")
print("="*70)

state_areas = aqi_df.groupby('state')['area'].nunique().sort_values(ascending=False)
top_10_states = state_areas.head(10).index.tolist()

q4_df = aqi_df[aqi_df['state'].isin(top_10_states)].copy()
q4_df['month'] = q4_df['date'].dt.month
q4_df['month_name'] = q4_df['date'].dt.strftime('%B')

if len(q4_df) > 0:
    monthly_avg = q4_df.groupby(['month', 'month_name'])['aqi_value'].mean().reset_index()
    monthly_avg = monthly_avg.sort_values('aqi_value', ascending=False)
    
    print(f"\n{'Rank':<6} | {'Month':<15} | {'Avg AQI':<10}")
    print("-" * 40)
    
    for rank, (_, row) in enumerate(monthly_avg.iterrows(), 1):
        indicator = "[BAD]" if rank <= 3 else "[MED]" if rank <= 6 else "[GOOD]"
        print(f"{indicator} {rank:<2} | {row['month_name']:<15} | {row['aqi_value']:.1f}")
    
    print(f"\n[INFO] Top 10 states analyzed: {', '.join(top_10_states)}")

# =====================================================
# Q5: Bengaluru - Days under each air quality category
#     (March to May 2025)
# =====================================================

print("\n" + "="*70)
print("Q5: BENGALURU - DAYS BY AIR QUALITY CATEGORY (Mar-May 2025)")
print("="*70)

q5_df = aqi_df[
    (aqi_df['area'].isin(['Bengaluru', 'Bangalore'])) & 
    (aqi_df['date'] >= datetime(2025, 3, 1)) & 
    (aqi_df['date'] <= datetime(2025, 5, 31))
].copy()

if len(q5_df) > 0:
    category_counts = q5_df['air_quality_status'].value_counts()
    
    print(f"\n{'Category':<20} | {'Days':<10} | {'Percentage':<10}")
    print("-" * 45)
    
    total_days = len(q5_df)
    for category, count in category_counts.items():
        pct = (count / total_days) * 100
        print(f"{str(category):<20} | {count:<10} | {pct:.1f}%")
    
    print(f"\nTotal days analyzed: {total_days}")
else:
    print("   No data for Bengaluru in Mar-May 2025. Using most recent available data...")
    blr_df = aqi_df[aqi_df['area'].isin(['Bengaluru', 'Bangalore'])]
    if len(blr_df) > 0:
        print(f"   Available date range: {blr_df['date'].min()} to {blr_df['date'].max()}")
        latest = blr_df['date'].max()
        three_months_ago = latest - pd.DateOffset(months=3)
        recent_df = blr_df[blr_df['date'] >= three_months_ago]
        if len(recent_df) > 0:
            print(f"\n   Using period: {three_months_ago.strftime('%Y-%m-%d')} to {latest.strftime('%Y-%m-%d')}")
            category_counts = recent_df['air_quality_status'].value_counts()
            for category, count in category_counts.items():
                print(f"   {str(category):<20} | {count} days")

# =====================================================
# Q6: Top 2 disease outbreaks per state with avg AQI
#     (Last 3 years)
# =====================================================

print("\n" + "="*70)
print("Q6: TOP 2 DISEASE OUTBREAKS PER STATE WITH AVERAGE AQI (Last 3 Years)")
print("="*70)

current_year = datetime.now().year
disease_df['year'] = pd.to_numeric(disease_df['year'], errors='coerce')
q6_disease = disease_df[disease_df['year'] >= current_year - 3].copy()

disease_col = None
for col in disease_df.columns:
    if 'disease' in col.lower() or 'illness' in col.lower():
        disease_col = col
        break

if disease_col and len(q6_disease) > 0:
    q6_disease['cases'] = pd.to_numeric(q6_disease['cases'], errors='coerce').fillna(0)
    state_disease = q6_disease.groupby(['state', disease_col])['cases'].sum().reset_index()
    states = q6_disease['state'].unique()[:10]
    
    aqi_3yr = aqi_df[aqi_df['date'] >= datetime(current_year - 3, 1, 1)]
    state_aqi = aqi_3yr.groupby('state')['aqi_value'].mean()
    
    print(f"\n{'State':<20} | {'Top Disease #1':<25} | {'Top Disease #2':<25} | {'Avg AQI':<10}")
    print("-" * 90)
    
    for state in states:
        state_data = state_disease[state_disease['state'] == state].nlargest(2, 'cases')
        if len(state_data) >= 2:
            d1 = str(state_data.iloc[0][disease_col])[:23]
            d2 = str(state_data.iloc[1][disease_col])[:23]
            avg_aqi = state_aqi.get(state, 'N/A')
            if isinstance(avg_aqi, float):
                avg_aqi = f"{avg_aqi:.1f}"
            print(f"{state:<20} | {d1:<25} | {d2:<25} | {str(avg_aqi):<10}")
else:
    print("   Disease data not available or column not found")

# =====================================================
# Q7: Top 5 EV adoption states - AQI comparison
# =====================================================

print("\n" + "="*70)
print("Q7: TOP 5 EV ADOPTION STATES VS LOW EV STATES - AQI COMPARISON")
print("="*70)

ev_df = vehicle_df[vehicle_df['fuel'].str.lower().str.contains('electric', na=False)].copy()
ev_df['value'] = pd.to_numeric(ev_df['value'], errors='coerce')

if len(ev_df) > 0:
    ev_by_state = ev_df.groupby('state')['value'].sum().sort_values(ascending=False)
    
    top_5_ev = ev_by_state.head(5).index.tolist()
    bottom_5_ev = ev_by_state.tail(5).index.tolist()
    
    state_aqi_all = aqi_df.groupby('state')['aqi_value'].mean()
    
    print("\n[HIGH EV] TOP 5 EV ADOPTION STATES:")
    print(f"{'State':<25} | {'EV Registrations':<20} | {'Avg AQI':<10}")
    print("-" * 60)
    for state in top_5_ev:
        ev_count = ev_by_state.get(state, 0)
        aqi = state_aqi_all.get(state, 'N/A')
        if isinstance(aqi, float):
            aqi_str = f"{aqi:.1f}"
        else:
            aqi_str = str(aqi)
        print(f"{state:<25} | {ev_count:>18,} | {aqi_str:<10}")
    
    avg_aqi_top_ev = state_aqi_all[state_aqi_all.index.isin(top_5_ev)].mean()
    
    print("\n[LOW EV] BOTTOM 5 EV ADOPTION STATES:")
    print(f"{'State':<25} | {'EV Registrations':<20} | {'Avg AQI':<10}")
    print("-" * 60)
    for state in bottom_5_ev:
        ev_count = ev_by_state.get(state, 0)
        aqi = state_aqi_all.get(state, 'N/A')
        if isinstance(aqi, float):
            aqi_str = f"{aqi:.1f}"
        else:
            aqi_str = str(aqi)
        print(f"{state:<25} | {ev_count:>18,} | {aqi_str:<10}")
    
    avg_aqi_bottom_ev = state_aqi_all[state_aqi_all.index.isin(bottom_5_ev)].mean()
    
    print("\n[SUMMARY] COMPARISON:")
    print(f"   Average AQI in Top 5 EV states:    {avg_aqi_top_ev:.1f}")
    print(f"   Average AQI in Bottom 5 EV states: {avg_aqi_bottom_ev:.1f}")
    if avg_aqi_top_ev < avg_aqi_bottom_ev:
        print(f"   [OK] High EV adoption states have {avg_aqi_bottom_ev - avg_aqi_top_ev:.1f} points BETTER air quality")
    else:
        print(f"   [WARN] High EV adoption states have {avg_aqi_top_ev - avg_aqi_bottom_ev:.1f} points WORSE air quality")
else:
    print("   No electric vehicle data found in vehicle registration dataset")

print("\n" + "="*70)
print("ANALYSIS COMPLETE")
print("="*70)
print("\nThese results can be cross-verified with the Power BI dashboard.")
