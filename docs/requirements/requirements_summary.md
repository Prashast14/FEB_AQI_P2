# AQI Analytics - Requirements Summary

## Problem Statement

![Problem Statement](file:///d:/FEB_AQI_P2/docs/requirements/problem_statement.png)

### Project Context

**Company**: AirPure Innovations  
**Domain**: Consumer Appliances  
**Function**: Market Research Analytics  
**Role**: Peter Pandey (Data Analyst) / Tony Sharma (COO)

AirPure Innovations is a startup addressing India's air quality crisis. With 14 Indian cities ranking among the world's top 20 most polluted urban centers, the company is developing an air purifier product. Before committing to production and R&D, they need to answer critical business questions.

---

## Critical Business Questions

### 1. Target Pollutants
**Question**: What pollutants or particles should their air purifier target?

**Data Source**: Day-wise AQI data with prominent pollutants (PM2.5, PM10, O3, CO, SO2)

**Approach**: Identify most frequently occurring and highest concentration pollutants across target markets

---

### 2. Essential Features
**Question**: What are the most essential features that should be incorporated into the air purifier?

**Data Source**: Market research, competitor analysis, pollutant patterns

**Approach**: Analyze correlation between air quality issues and required features (e.g., HEPA filters for PM2.5, activated carbon for gases)

---

### 3. High-Demand Cities
**Question**: Which cities have the highest demand for air purifiers, and what is the market size in these regions?

**Data Source**: 
- AQI severity rankings
- Population projections
- City tier classification
- Income levels

**Approach**: Calculate market size using severity × population density × economic indicators

---

### 4. R&D Alignment
**Question**: How can R&D be aligned with localized pollution patterns?

**Data Source**: City-specific pollutant patterns, seasonal variations

**Approach**: Identify pollution patterns by geography and recommend customized solutions

---

## Three Key Analysis Dimensions

### 1. Severity Ranking
Identify cities experiencing persistent or worsening AQI levels.

**Metrics**:
- Average AQI by city (2022-2025)
- AQI trend analysis (improving vs worsening)
- Number of "Severe" and "Very Poor" days

**Data Source**: Delhi, Gurgaon, Noida, Bhopal, Jaipur, Kanpur, Lucknow, Patna, Agra (top polluted cities)

---

### 2. Health Burden Correlation
Quantify the health burden due to pollution and its impact on consumers' well-being.

**Metrics**:
- Disease outbreak correlation with AQI
- Pediatric asthma admissions
- Respiratory illness cases
- Health cost projections

**Data Source**: IDSP disease outbreak data, health-related consequences

---

### 3. Demand Triggers
Examine the relationship between pollution spikes and shifts in consumer behavior related to air purifier searches/purchases.

**Metrics**:
- Pollution emergency incidents
- Seasonal spike patterns
- Consumer awareness levels
- Search trend correlation (if available)

---

## Primary Analysis Requirements

![Primary and Secondary Analysis](file:///d:/FEB_AQI_P2/docs/requirements/analysis_requirements.png)

### Primary Analysis (Based on Available Data)

#### 1. Top and Bottom Areas by AQI
**Requirement**: List the top 5 and bottom 5 areas with highest average AQI

**Timeframe**: Areas with data from last 6 months (December 2024 to May 2025)

**Output**: Ranking table with:
- City name
- State
- Average AQI
- Number of monitoring stations
- Prominent pollutant

---

#### 2. Pollutant Analysis (Southern India)
**Requirement**: List out top 2 and bottom 2 prominent pollutants for each state of southern India

**States**: Karnataka, Tamil Nadu, Kerala, Andhra Pradesh, Telangana

**Timeframe**: April 2022 onwards

**Output**: Table showing:
- State
- Top 2 pollutants (by frequency/concentration)
- Bottom 2 pollutants

---

#### 3. Weekend vs Weekday Analysis
**Requirement**: Does AQI improve on weekends vs weekdays in Indian metro cities?

**Cities**: Delhi, Mumbai, Chennai, Kolkata, Bengaluru, Hyderabad, Ahmedabad, Pune

**Timeframe**: Last 1 year

**Output**:
- Average AQI for weekends
- Average AQI for weekdays
- Improvement percentage
- Statistical significance

---

#### 4. Worst Air Quality Months
**Requirement**: Which months consistently show the worst air quality across Indian states?

**Scope**: Top 10 states with high distinct areas

**Output**:
- Month-wise average AQI
- State-wise worst months
- Seasonal patterns

---

#### 5. Bengaluru Air Quality Distribution
**Requirement**: For the city of Bengaluru, how many days fell under each air quality category?

**Categories**: Good, Moderate, Poor, etc. (between March and May 2025)

**Timeframe**: March 1, 2025 to May 31, 2025

**Output**:
- Category-wise day count
- Percentage distribution
- Trend analysis

---

#### 6. Disease Illness Analysis
**Requirement**: List the top two most reported disease illnesses in each state over the past three years, along with the corresponding average Air Quality Index (AQI)

**Timeframe**: Past 3 years (2022-2024)

**Output**:
- State
- Top 2 diseases
- Case counts
- Average AQI during outbreak periods
- Correlation coefficient

---

#### 7. EV Adoption vs AQI
**Requirement**: List the top 5 states with high EV adoption and analyse if their average AQI is significantly better compared to states with lower EV adoption

**Timeframe**: 2024 population and AQI data

**Analysis**: 
- EV adoption rate calculation
- AQI comparison (high EV vs low EV states)
- Statistical significance testing

---

## Secondary Analysis Requirements

### 1. Age Group Health Impact
**Question**: Which age group is most affected by air pollution-related health outcomes — and how does this vary by city?

**Approach**: 
- Analyze disease data for age-related patterns
- Cross-reference with AQI severity
- Identify vulnerable demographics

---

### 2. Market Differentiators
**Question**: Who are the major competitors in the Indian air purifier market, and what are their key differentiators?

**Deliverables**:
- Market prioritization dashboard
- City risk scores (AQI severity × population density × income)
- Health cost impact projections
- Competitor feature gap matrix

---

### 3. Population-AQI Relationship
**Question**: What is the relationship between India's population and AQI — do larger cities always suffer from worse air quality?

**Analysis**:
- Population vs AQI scatter plot
- City tier classification
- Urban density correlation
- Counterexamples (large cities with good AQI)

---

### 4. AQI Awareness
**Question**: How aware are Indian citizens of what AQI (Air Quality Index) means — and do they understand its health implications?

**Approach**:
- Behavior analysis during pollution spikes
- Search trend analysis (if available)
- Policy awareness indicators
- Educational gap identification

---

### 5. Government Policy Impact
**Question**: Which pollution control policies introduced by the Indian government in the past 5 years have had the most measurable impact on improving air quality — and how have these impacts varied across regions or cities?

**Analysis**:
- Pre/post policy AQI comparison
- Regional effectiveness
- Policy type categorization
- Success factor identification

---

## Critical Questions for Deliverables

### 1. Priority Cities
**Question**: Which Tier 1/2 cities show irreversible AQI degradation?

**Metric**: Cities with consistent worsening trend over 3+ years

---

### 2. Health Burden
**Question**: How do AQI spikes correlate with pediatric asthma admissions?

**Data**: Disease outbreak data filtered for respiratory conditions

---

### 3. Behavior Shifts
**Question**: Do pollution emergencies increase purifier searches/purchases?

**Proxy**: Pollution spike events and consumer behavior indicators

---

### 4. Feature Gap
**Question**: What do existing products lack (e.g., smart AQI syncing, compact designs)?

**Approach**: Competitive analysis + customer need mapping

---

## Data Sources Summary

| Dataset | Time Range | Records | Key Fields |
|---------|------------|---------|------------|
| AQI Daily Data | 2022-2025 | ~500K+ | Date, State, Area, AQI, Pollutants, Status |
| Disease Outbreak | 2022-2025 | ~50K+ | Date, State, District, Disease, Cases, Deaths |
| Vehicle Registration | 2022-2025 | ~100K+ | Month, State, Vehicle Class, Fuel Type, Count |
| Population Projection | 2011-2036 | ~15K+ | Year, State, Gender, Population (thousands) |

---

## Expected Deliverables

### 1. Market Prioritization Dashboard
- City risk scores
- Health cost impact projections
- Competitor feature gap matrix

### 2. Product Requirements Document
- Must-have features (PM2.5/VO2C sensors)
- Tiered pricing models for target segments

### 3. Innovate
- Integrate external data (Google Trends, satellite imagery)
- Video demonstration of dashboard functionality
- City-specific entry simulations

---

## Success Metrics

- ✅ All 7 primary analysis questions answered
- ✅ All 5 secondary analysis questions addressed
- ✅ Critical questions for deliverables resolved
- ✅ Dashboard is self-explanatory and easy to navigate
- ✅ Insights are actionable for business decisions
- ✅ Data is accurate and validated
- ✅ Presentation is creative and concise

---

## Tools & Technologies

- **Database**: MySQL
- **ETL**: Python (pandas, sqlalchemy, pymysql)
- **Analytics**: SQL, Python
- **Visualization**: Power BI Desktop
- **Version Control**: Git/GitHub
- **Documentation**: Markdown, Mermaid diagrams

---

## Timeline

**Target**: 3-4 days for complete implementation

- **Day 1**: Database setup and data import
- **Day 2**: Analytical views and data validation
- **Day 3**: Power BI dashboard development
- **Day 4**: Testing, documentation, video presentation

---

*Document Created: February 1, 2026*  
*Author: Prashast Maurya*  
*Project: AirPure Innovations - AQI Analytics Dashboard*
