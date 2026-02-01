-- =====================================================
-- AirPure Innovations - AQI Analytics Database Schema
-- =====================================================
-- Database: airpure_aqi_db
-- Purpose: Store and analyze AQI data for market research
-- Created: February 1, 2026
-- =====================================================

-- Create database
DROP DATABASE IF EXISTS airpure_aqi_db;
CREATE DATABASE airpure_aqi_db;
USE airpure_aqi_db;

-- =====================================================
-- DIMENSION TABLES
-- =====================================================

-- Dimension: State
CREATE TABLE dim_state (
    state_id INT AUTO_INCREMENT PRIMARY KEY,
    state_name VARCHAR(100) NOT NULL UNIQUE,
    region VARCHAR(50),  -- North, South, East, West, Central, Northeast
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dimension: City/Area
CREATE TABLE dim_city (
    city_id INT AUTO_INCREMENT PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL,
    state_id INT,
    city_tier VARCHAR(10),  -- Tier 1, Tier 2, Tier 3
    is_metro BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (state_id) REFERENCES dim_state(state_id),
    UNIQUE KEY unique_city_state (city_name, state_id)
);

-- Dimension: Date (for time intelligence)
CREATE TABLE dim_date (
    date_id INT AUTO_INCREMENT PRIMARY KEY,
    date_value DATE NOT NULL UNIQUE,
    year INT,
    quarter INT,
    month INT,
    month_name VARCHAR(20),
    week INT,
    day_of_month INT,
    day_of_week INT,
    day_name VARCHAR(20),
    is_weekend BOOLEAN,
    is_holiday BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dimension: Pollutant
CREATE TABLE dim_pollutant (
    pollutant_id INT AUTO_INCREMENT PRIMARY KEY,
    pollutant_code VARCHAR(20) NOT NULL UNIQUE,
    pollutant_name VARCHAR(100),
    pollutant_category VARCHAR(50),  -- Particulate Matter, Gas, etc.
    health_impact VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dimension: Population
CREATE TABLE dim_population (
    population_id INT AUTO_INCREMENT PRIMARY KEY,
    state_id INT,
    year INT,
    month INT,
    gender VARCHAR(20),  -- Total, Male, Female
    population_thousands DECIMAL(12, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (state_id) REFERENCES dim_state(state_id),
    UNIQUE KEY unique_state_year_month_gender (state_id, year, month, gender)
);

-- =====================================================
-- FACT TABLES
-- =====================================================

-- Fact: Daily AQI Measurements
CREATE TABLE fact_aqi_daily (
    aqi_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    date_id INT,
    state_id INT,
    city_id INT,
    date_value DATE,
    state_name VARCHAR(100),
    city_name VARCHAR(100),
    number_of_monitoring_stations INT,
    prominent_pollutants VARCHAR(255),
    aqi_value DECIMAL(10, 2),
    air_quality_status VARCHAR(50),
    unit VARCHAR(50),
    note TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (state_id) REFERENCES dim_state(state_id),
    FOREIGN KEY (city_id) REFERENCES dim_city(city_id),
    INDEX idx_date (date_value),
    INDEX idx_state (state_id),
    INDEX idx_city (city_id),
    INDEX idx_aqi_value (aqi_value)
);

-- Fact: Disease Outbreak
CREATE TABLE fact_disease_outbreak (
    outbreak_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    year INT,
    week INT,
    outbreak_starting_date DATE,
    reporting_date DATE,
    state_id INT,
    state_name VARCHAR(100),
    district VARCHAR(100),
    disease_illness_name VARCHAR(255),
    status VARCHAR(50),
    cases INT,
    deaths INT,
    unit VARCHAR(50),
    note TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (state_id) REFERENCES dim_state(state_id),
    INDEX idx_state (state_id),
    INDEX idx_disease (disease_illness_name),
    INDEX idx_outbreak_date (outbreak_starting_date)
);

-- Fact: Vehicle Registration
CREATE TABLE fact_vehicle_registration (
    vehicle_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    year INT,
    month INT,
    state_id INT,
    state_name VARCHAR(100),
    rto VARCHAR(100),
    vehicle_class VARCHAR(100),
    fuel VARCHAR(50),
    value INT,
    unit VARCHAR(50),
    note TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (state_id) REFERENCES dim_state(state_id),
    INDEX idx_state (state_id),
    INDEX idx_year_month (year, month),
    INDEX idx_fuel (fuel),
    INDEX idx_vehicle_class (vehicle_class)
);

-- =====================================================
-- Insert Reference Data
-- =====================================================

-- Insert Pollutant Reference Data
INSERT INTO dim_pollutant (pollutant_code, pollutant_name, pollutant_category, health_impact) VALUES
('PM2.5', 'Particulate Matter 2.5', 'Particulate Matter', 'Respiratory issues, heart disease, lung cancer'),
('PM10', 'Particulate Matter 10', 'Particulate Matter', 'Respiratory issues, asthma'),
('O3', 'Ozone', 'Gas', 'Respiratory issues, reduced lung function'),
('NO2', 'Nitrogen Dioxide', 'Gas', 'Respiratory issues, asthma exacerbation'),
('SO2', 'Sulfur Dioxide', 'Gas', 'Respiratory issues, bronchitis'),
('CO', 'Carbon Monoxide', 'Gas', 'Reduced oxygen delivery, cardiovascular issues'),
('NH3', 'Ammonia', 'Gas', 'Eye irritation, respiratory issues');

-- Insert Metro Cities Reference (will be populated during ETL)
-- Metro cities: Delhi, Mumbai, Chennai, Kolkata, Bengaluru, Hyderabad, Ahmedabad, Pune

-- =====================================================
-- End of Schema Creation
-- =====================================================

SELECT 'Database schema created successfully!' as Status;
