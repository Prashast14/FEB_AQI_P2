-- =====================================================
-- AirPure AQI Analytics - Database Schema v2
-- =====================================================
-- Simplified flat tables for direct CSV/Excel loading
-- No complex dimension/fact relationships
-- =====================================================

DROP DATABASE IF EXISTS airpure_aqi_db;
CREATE DATABASE airpure_aqi_db;
USE airpure_aqi_db;

-- =====================================================
-- Table 1: AQI Daily Data
-- Source: day-wise-state-wise-air-quality-index-aqi...csv
-- =====================================================
CREATE TABLE aqi_daily (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    date DATE,
    state VARCHAR(100),
    area VARCHAR(100),
    monitoring_stations INT,
    prominent_pollutants VARCHAR(255),
    aqi_value DECIMAL(10,2),
    air_quality_status VARCHAR(50),
    unit VARCHAR(200),
    note TEXT,
    INDEX idx_date (date),
    INDEX idx_state (state),
    INDEX idx_area (area),
    INDEX idx_aqi_value (aqi_value)
);

-- =====================================================
-- Table 2: Disease Outbreak Data
-- Source: master-data-state-district-and-disease...csv
-- =====================================================
CREATE TABLE disease_outbreak (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    year INT,
    week INT,
    outbreak_date DATE,
    reporting_date DATE,
    state VARCHAR(100),
    district VARCHAR(100),
    disease_name VARCHAR(255),
    status VARCHAR(50),
    cases INT,
    deaths INT,
    unit VARCHAR(200),
    note TEXT,
    INDEX idx_state (state),
    INDEX idx_disease (disease_name),
    INDEX idx_outbreak_date (outbreak_date)
);

-- =====================================================
-- Table 3: Vehicle Registration Data
-- Source: master-data-state-vehicle-class...csv
-- =====================================================
CREATE TABLE vehicle_registration (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    year INT,
    month INT,
    state VARCHAR(100),
    rto VARCHAR(100),
    vehicle_class VARCHAR(100),
    fuel VARCHAR(50),
    value BIGINT,
    unit VARCHAR(200),
    note TEXT,
    INDEX idx_state (state),
    INDEX idx_year_month (year, month),
    INDEX idx_fuel (fuel),
    INDEX idx_vehicle_class (vehicle_class)
);

-- =====================================================
-- Table 4: Population Data
-- Source: population-projection...xlsx
-- =====================================================
CREATE TABLE population (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    state VARCHAR(100),
    year INT,
    month INT,
    gender VARCHAR(20),
    population_thousands DECIMAL(12,2),
    INDEX idx_state (state),
    INDEX idx_year (year)
);

SELECT 'Schema v2 created successfully!' as Status;
