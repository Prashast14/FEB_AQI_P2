-- =====================================================
-- AirPure Innovations - Analytical SQL Views
-- Purpose: Create views to answer all primary and secondary analysis questions
-- Created: February 1, 2026
-- =====================================================

USE airpure_aqi_db;

-- =====================================================
-- PRIMARY ANALYSIS VIEWS
-- =====================================================

-- ------------------------------------------------------
-- View 1: Top 5 and Bottom 5 Areas by Average AQI
-- Requirement: Areas with data from last 6 months (Dec 2024 - May 2025)
-- ------------------------------------------------------

CREATE OR REPLACE VIEW vw_top_bottom_areas_aqi AS
WITH area_aqi_stats AS (
    SELECT 
        c.city_name,
        s.state_name,
        c.city_tier,
        c.is_metro,
        COUNT(DISTINCT f.date_value) as days_with_data,
        AVG(f.aqi_value) as avg_aqi,
        MIN(f.aqi_value) as min_aqi,
        MAX(f.aqi_value) as max_aqi,
        SUM(CASE WHEN f.air_quality_status IN ('Severe', 'Very Poor') THEN 1 ELSE 0 END) as severe_days,
        f.prominent_pollutants as predominant_pollutant
    FROM 
        fact_aqi_daily f
        JOIN dim_city c ON f.city_id = c.city_id
        JOIN dim_state s ON f.state_id = s.state_id
    WHERE 
        f.date_value >= '2024-12-01' AND f.date_value <= '2025-05-31'
        AND f.aqi_value IS NOT NULL
    GROUP BY 
        c.city_name, s.state_name, c.city_tier, c.is_metro, f.prominent_pollutants
    HAVING 
        days_with_data >= 30  -- At least 30 days of data
),
ranked_areas AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (ORDER BY avg_aqi DESC) as rank_desc,
        ROW_NUMBER() OVER (ORDER BY avg_aqi ASC) as rank_asc
    FROM 
        area_aqi_stats
)
SELECT 
    city_name,
    state_name,
    city_tier,
    CASE WHEN is_metro = 1 THEN 'Yes' ELSE 'No' END as is_metro_city,
    ROUND(avg_aqi, 2) as average_aqi,
    ROUND(min_aqi, 2) as minimum_aqi,
    ROUND(max_aqi, 2) as maximum_aqi,
    severe_days,
    predominant_pollutant,
    CASE 
        WHEN rank_desc <= 5 THEN 'Top 5 Most Polluted'
        WHEN rank_asc <= 5 THEN 'Bottom 5 Least Polluted'
        ELSE 'Middle Range'
    END as category
FROM 
    ranked_areas
WHERE 
    rank_desc <= 5 OR rank_asc <= 5
ORDER BY 
    avg_aqi DESC;

-- ------------------------------------------------------
-- View 2: Top 2 and Bottom 2 Pollutants by State (Southern India)
-- Requirement: Southern states (April 2022 onwards)
-- ------------------------------------------------------

CREATE OR REPLACE VIEW vw_south_india_pollutants AS
WITH pollutant_counts AS (
    SELECT 
        s.state_name,
        f.prominent_pollutants as pollutant,
        COUNT(*) as occurrence_count,
        AVG(f.aqi_value) as avg_aqi_for_pollutant
    FROM 
        fact_aqi_daily f
        JOIN dim_state s ON f.state_id = s.state_id
    WHERE 
        s.region = 'South'
        AND f.date_value >= '2022-04-01'
        AND f.prominent_pollutants IS NOT NULL
    GROUP BY 
        s.state_name, f.prominent_pollutants
),
ranked_pollutants AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (PARTITION BY state_name ORDER BY occurrence_count DESC) as rank_desc,
        ROW_NUMBER() OVER (PARTITION BY state_name ORDER BY occurrence_count ASC) as rank_asc
    FROM 
        pollutant_counts
)
SELECT 
    state_name,
    pollutant,
    occurrence_count,
    ROUND(avg_aqi_for_pollutant, 2) as avg_aqi,
    CASE 
        WHEN rank_desc <= 2 THEN 'Top 2 Most Common'
        WHEN rank_asc <= 2 THEN 'Bottom 2 Least Common'
        ELSE 'Middle Range'
    END as category
FROM 
    ranked_pollutants
WHERE 
    rank_desc <= 2 OR rank_asc <= 2
ORDER BY 
    state_name, occurrence_count DESC;

-- ------------------------------------------------------
-- View 3: Weekend vs Weekday AQI (Metro Cities)
-- Requirement: Last 1 year, metro cities only
-- ------------------------------------------------------

CREATE OR REPLACE VIEW vw_weekend_vs_weekday_aqi AS
WITH metro_aqi AS (
    SELECT 
        c.city_name,
        s.state_name,
        d.is_weekend,
        f.aqi_value,
        f.date_value
    FROM 
        fact_aqi_daily f
        JOIN dim_city c ON f.city_id = c.city_id
        JOIN dim_state s ON f.state_id = s.state_id
        JOIN dim_date d ON f.date_id = d.date_id
    WHERE 
        c.is_metro = 1
        AND f.date_value >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
        AND f.aqi_value IS NOT NULL
)
SELECT 
    city_name,
    state_name,
    ROUND(AVG(CASE WHEN is_weekend = 1 THEN aqi_value END), 2) as avg_weekend_aqi,
    ROUND(AVG(CASE WHEN is_weekend = 0 THEN aqi_value END), 2) as avg_weekday_aqi,
    ROUND(
        (AVG(CASE WHEN is_weekend = 0 THEN aqi_value END) - 
         AVG(CASE WHEN is_weekend = 1 THEN aqi_value END)) /
        AVG(CASE WHEN is_weekend = 0 THEN aqi_value END) * 100, 
        2
    ) as improvement_percentage,
    COUNT(CASE WHEN is_weekend = 1 THEN 1 END) as weekend_days_count,
    COUNT(CASE WHEN is_weekend = 0 THEN 1 END) as weekday_days_count
FROM 
    metro_aqi
GROUP BY 
    city_name, state_name
HAVING 
    avg_weekend_aqi IS NOT NULL AND avg_weekday_aqi IS NOT NULL
ORDER BY 
    improvement_percentage DESC;

-- ------------------------------------------------------
-- View 4: Months with Worst Air Quality by State
-- Requirement: Top 10 states with high distinct areas
-- ------------------------------------------------------

CREATE OR REPLACE VIEW vw_worst_months_by_state AS
WITH state_area_count AS (
    SELECT 
        state_id,
        COUNT(DISTINCT city_id) as distinct_areas
    FROM 
        fact_aqi_daily
    GROUP BY 
        state_id
    ORDER BY 
        distinct_areas DESC
    LIMIT 10
),
monthly_aqi AS (
    SELECT 
        s.state_name,
        d.month,
        d.month_name,
        AVG(f.aqi_value) as avg_monthly_aqi,
        COUNT(DISTINCT f.city_id) as cities_count
    FROM 
        fact_aqi_daily f
        JOIN dim_state s ON f.state_id = s.state_id
        JOIN dim_date d ON f.date_id = d.date_id
    WHERE 
        f.state_id IN (SELECT state_id FROM state_area_count)
        AND f.aqi_value IS NOT NULL
    GROUP BY 
        s.state_name, d.month, d.month_name
),
ranked_months AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (PARTITION BY state_name ORDER BY avg_monthly_aqi DESC) as worst_rank
    FROM 
        monthly_aqi
)
SELECT 
    state_name,
    month_name,
    ROUND(avg_monthly_aqi, 2) as average_aqi,
    cities_count,
    worst_rank
FROM 
    ranked_months
WHERE 
    worst_rank <= 3  -- Top 3 worst months per state
ORDER BY 
    state_name, worst_rank;

-- ------------------------------------------------------
-- View 5: Bengaluru Air Quality Category Distribution
-- Requirement: March - May 2025
-- ------------------------------------------------------

CREATE OR REPLACE VIEW vw_bengaluru_aqi_distribution AS
SELECT 
    f.air_quality_status as category,
    COUNT(DISTINCT f.date_value) as days_count,
    ROUND(COUNT(DISTINCT f.date_value) * 100.0 / 
        (SELECT COUNT(DISTINCT date_value) 
         FROM fact_aqi_daily 
         WHERE city_name = 'Bengaluru' 
         AND date_value BETWEEN '2025-03-01' AND '2025-05-31'), 2) as percentage,
    AVG(f.aqi_value) as avg_aqi,
    MIN(f.aqi_value) as min_aqi,
    MAX(f.aqi_value) as max_aqi
FROM 
    fact_aqi_daily f
WHERE 
    f.city_name IN ('Bengaluru', 'Bangalore')
    AND f.date_value BETWEEN '2025-03-01' AND '2025-05-31'
    AND f.air_quality_status IS NOT NULL
GROUP BY 
    f.air_quality_status
ORDER BY 
    FIELD(f.air_quality_status, 'Good', 'Satisfactory', 'Moderate', 'Poor', 'Very Poor', 'Severe');

-- ------------------------------------------------------
-- View 6: Top 2 Disease Illnesses by State (Past 3 Years)
-- with corresponding Average AQI
-- ------------------------------------------------------

CREATE OR REPLACE VIEW vw_top_diseases_with_aqi AS
WITH disease_stats AS (
    SELECT 
        s.state_name,
        d.disease_illness_name,
        SUM(d.cases) as total_cases,
        SUM(d.deaths) as total_deaths,
        COUNT(*) as outbreak_count,
        MIN(d.outbreak_starting_date) as first_outbreak,
        MAX(d.outbreak_starting_date) as last_outbreak
    FROM 
        fact_disease_outbreak d
        JOIN dim_state s ON d.state_id = s.state_id
    WHERE 
        d.outbreak_starting_date >= DATE_SUB(CURDATE(), INTERVAL 3 YEAR)
    GROUP BY 
        s.state_name, d.disease_illness_name
),
ranked_diseases AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (PARTITION BY state_name ORDER BY total_cases DESC) as disease_rank
    FROM 
        disease_stats
),
state_aqi AS (
    SELECT 
        s.state_name,
        AVG(f.aqi_value) as avg_aqi_3years
    FROM 
        fact_aqi_daily f
        JOIN dim_state s ON f.state_id = s.state_id
    WHERE 
        f.date_value >= DATE_SUB(CURDATE(), INTERVAL 3 YEAR)
    GROUP BY 
        s.state_name
)
SELECT 
    rd.state_name,
    rd.disease_illness_name,
    rd.total_cases,
    rd.total_deaths,
    rd.outbreak_count,
    ROUND(sa.avg_aqi_3years, 2) as avg_state_aqi,
    rd.disease_rank
FROM 
    ranked_diseases rd
    LEFT JOIN state_aqi sa ON rd.state_name = sa.state_name
WHERE 
    rd.disease_rank <= 2
ORDER BY 
    rd.state_name, rd.disease_rank;

-- ------------------------------------------------------
-- View 7: EV Adoption vs AQI Analysis
-- Requirement: Top 5 states with high EV adoption (2024 data)
-- ------------------------------------------------------

CREATE OR REPLACE VIEW vw_ev_adoption_vs_aqi AS
WITH ev_adoption AS (
    SELECT 
        s.state_name,
        SUM(CASE WHEN v.fuel IN ('ELECTRIC', 'PURE EV', 'HYBRID') THEN v.value ELSE 0 END) as ev_count,
        SUM(v.value) as total_vehicles,
        ROUND(SUM(CASE WHEN v.fuel IN ('ELECTRIC', 'PURE EV', 'HYBRID') THEN v.value ELSE 0 END) * 100.0 / 
              NULLIF(SUM(v.value), 0), 2) as ev_adoption_percentage
    FROM 
        fact_vehicle_registration v
        JOIN dim_state s ON v.state_id = s.state_id
    WHERE 
        v.year = 2024
    GROUP BY 
        s.state_name
    HAVING 
        total_vehicles > 0
),
state_aqi_2024 AS (
    SELECT 
        s.state_name,
        AVG(f.aqi_value) as avg_aqi_2024,
        COUNT(DISTINCT f.city_id) as cities_monitored
    FROM 
        fact_aqi_daily f
        JOIN dim_state s ON f.state_id = s.state_id
        JOIN dim_date d ON f.date_id = d.date_id
    WHERE 
        d.year = 2024
        AND f.aqi_value IS NOT NULL
    GROUP BY 
        s.state_name
),
ev_ranked AS (
    SELECT 
        e.*,
        a.avg_aqi_2024,
        a.cities_monitored,
        ROW_NUMBER() OVER (ORDER BY e.ev_adoption_percentage DESC) as ev_rank
    FROM 
        ev_adoption e
        LEFT JOIN state_aqi_2024 a ON e.state_name = a.state_name
)
SELECT 
    state_name,
    ev_count,
    total_vehicles,
    ev_adoption_percentage,
    ROUND(avg_aqi_2024, 2) as average_aqi_2024,
    cities_monitored,
    CASE 
        WHEN ev_rank <= 5 THEN 'High EV Adoption'
        ELSE 'Low EV Adoption'
    END as ev_category
FROM 
    ev_ranked
WHERE 
    avg_aqi_2024 IS NOT NULL
ORDER BY 
    ev_adoption_percentage DESC;

-- =====================================================
-- SUPPORTING ANALYTICAL VIEWS
-- =====================================================

-- ------------------------------------------------------
-- View: City AQI Severity and Risk Score
-- Purpose: Calculate risk scores for market prioritization
-- ------------------------------------------------------

CREATE OR REPLACE VIEW vw_city_severity_risk AS
WITH city_metrics AS (
    SELECT 
        c.city_name,
        s.state_name,
        c.city_tier,
        c.is_metro,
        AVG(f.aqi_value) as avg_aqi,
        MAX(f.aqi_value) as max_aqi,
        SUM(CASE WHEN f.air_quality_status IN ('Severe', 'Very Poor') THEN 1 ELSE 0 END) as severe_days_count,
        COUNT(DISTINCT f.date_value) as total_days_monitored,
        f.prominent_pollutants
    FROM 
        fact_aqi_daily f
        JOIN dim_city c ON f.city_id = c.city_id
        JOIN dim_state s ON f.state_id = s.state_id
    WHERE 
        f.date_value >= '2024-01-01'
        AND f.aqi_value IS NOT NULL
    GROUP BY 
        c.city_name, s.state_name, c.city_tier, c.is_metro, f.prominent_pollutants
),
population_data AS (
    SELECT 
        s.state_name,
        AVG(p.population_thousands) as avg_population_thousands
    FROM 
        dim_population p
        JOIN dim_state s ON p.state_id = s.state_id
    WHERE 
        p.year = 2024 AND p.gender = 'Total'
    GROUP BY 
        s.state_name
)
SELECT 
    cm.city_name,
    cm.state_name,
    cm.city_tier,
    CASE WHEN cm.is_metro = 1 THEN 'Yes' ELSE 'No' END as is_metro_city,
    ROUND(cm.avg_aqi, 2) as average_aqi,
    ROUND(cm.max_aqi, 2) as max_aqi,
    cm.severe_days_count,
    cm.total_days_monitored,
    ROUND(cm.severe_days_count * 100.0 / cm.total_days_monitored, 2) as severe_days_percentage,
    cm.prominent_pollutants,
    ROUND(pd.avg_population_thousands, 2) as state_population_thousands,
    -- Risk Score = (Avg AQI / 100) × (Severe Days %) × Population Factor
    ROUND(
        (cm.avg_aqi / 100) * 
        (cm.severe_days_count * 100.0 / cm.total_days_monitored) * 
        (CASE 
            WHEN cm.city_tier = 'Tier 1' THEN 3
            WHEN cm.city_tier = 'Tier 2' THEN 2
            ELSE 1
        END), 2
    ) as risk_score
FROM 
    city_metrics cm
    LEFT JOIN population_data pd ON cm.state_name = pd.state_name
ORDER BY 
    risk_score DESC;

-- ------------------------------------------------------
-- View: Health Correlation Analysis
-- Purpose: Correlate AQI with health outcomes
-- ------------------------------------------------------

CREATE OR REPLACE VIEW vw_health_aqi_correlation AS
WITH monthly_aqi AS (
    SELECT 
        s.state_name,
        d.year,
        d.month,
        AVG(f.aqi_value) as avg_monthly_aqi
    FROM 
        fact_aqi_daily f
        JOIN dim_state s ON f.state_id = s.state_id
        JOIN dim_date d ON f.date_id = d.date_id
    GROUP BY 
        s.state_name, d.year, d.month
),
monthly_health AS (
    SELECT 
        s.state_name,
        YEAR(d.outbreak_starting_date) as year,
        MONTH(d.outbreak_starting_date) as month,
        SUM(d.cases) as total_monthly_cases,
        SUM(d.deaths) as total_monthly_deaths,
        COUNT(DISTINCT d.disease_illness_name) as disease_types
    FROM 
        fact_disease_outbreak d
        JOIN dim_state s ON d.state_id = s.state_id
    WHERE 
        d.outbreak_starting_date IS NOT NULL
    GROUP BY 
        s.state_name, YEAR(d.outbreak_starting_date), MONTH(d.outbreak_starting_date)
)
SELECT 
    a.state_name,
    a.year,
    a.month,
    ROUND(a.avg_monthly_aqi, 2) as avg_aqi,
    COALESCE(h.total_monthly_cases, 0) as health_cases,
    COALESCE(h.total_monthly_deaths, 0) as health_deaths,
    COALESCE(h.disease_types, 0) as disease_types_count
FROM 
    monthly_aqi a
    LEFT JOIN monthly_health h ON a.state_name = h.state_name 
                                AND a.year = h.year 
                                AND a.month = h.month
WHERE 
    a.year >= 2022
ORDER BY 
    a.state_name, a.year, a.month;

-- ------------------------------------------------------
-- View: Pollutant-Specific Analysis
-- Purpose: Identify dominant pollutants by region
-- ------------------------------------------------------

CREATE OR REPLACE VIEW vw_pollutant_analysis AS
SELECT 
    s.state_name,
    s.region,
    c.city_tier,
    f.prominent_pollutants as pollutant,
    COUNT(*) as occurrence_count,
    AVG(f.aqi_value) as avg_aqi_for_pollutant,
    MIN(f.aqi_value) as min_aqi,
    MAX(f.aqi_value) as max_aqi,
    SUM(CASE WHEN f.air_quality_status IN ('Severe', 'Very Poor') THEN 1 ELSE 0 END) as severe_occurrences
FROM 
    fact_aqi_daily f
    JOIN dim_state s ON f.state_id = s.state_id
    JOIN dim_city c ON f.city_id = c.city_id
WHERE 
    f.prominent_pollutants IS NOT NULL
    AND f.date_value >= '2022-01-01'
GROUP BY 
    s.state_name, s.region, c.city_tier, f.prominent_pollutants
ORDER BY 
    s.region, occurrence_count DESC;

-- ------------------------------------------------------
-- View: Market Size and Demand Estimation
-- Purpose: Estimate market size for air purifier demand
-- ------------------------------------------------------

CREATE OR REPLACE VIEW vw_market_demand_estimation AS
WITH city_aqi_pop AS (
    SELECT 
        c.city_name,
        s.state_name,
        c.city_tier,
        AVG(f.aqi_value) as avg_aqi,
        SUM(CASE WHEN f.air_quality_status IN ('Severe', 'Very Poor', 'Poor') THEN 1 ELSE 0 END) as poor_quality_days,
        COUNT(DISTINCT f.date_value) as total_days,
        AVG(p.population_thousands) as avg_population_thousands
    FROM 
        fact_aqi_daily f
        JOIN dim_city c ON f.city_id = c.city_id
        JOIN dim_state s ON f.state_id = s.state_id
        LEFT JOIN dim_population p ON s.state_id = p.state_id AND p.year = 2024 AND p.gender = 'Total'
    WHERE 
        f.date_value >= '2024-01-01'
    GROUP BY 
        c.city_name, s.state_name, c.city_tier
)
SELECT 
    city_name,
    state_name,
    city_tier,
    ROUND(avg_aqi, 2) as average_aqi,
    poor_quality_days,
    total_days,
    ROUND(poor_quality_days * 100.0 / total_days, 2) as poor_quality_percentage,
    ROUND(avg_population_thousands, 2) as population_thousands,
    -- Market demand score: Higher AQI + More poor days + Larger population = Higher demand
    ROUND(
        (avg_aqi / 10) * 
        (poor_quality_days * 100.0 / total_days) * 
        (avg_population_thousands / 1000) *
        (CASE 
            WHEN city_tier = 'Tier 1' THEN 1.5
            WHEN city_tier = 'Tier 2' THEN 1.2
            ELSE 1.0
        END), 2
    ) as market_demand_score
FROM 
    city_aqi_pop
WHERE 
    avg_population_thousands IS NOT NULL
ORDER BY 
    market_demand_score DESC;

-- =====================================================
-- End of Analytical Views
-- =====================================================

SELECT 'All analytical views created successfully!' as Status;
