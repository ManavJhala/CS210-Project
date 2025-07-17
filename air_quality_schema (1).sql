-- Create SQL schema for pollution and weather data

CREATE TABLE pollution_data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP,
    location TEXT,
    pm25 FLOAT,
    co FLOAT,
    o3 FLOAT
);

CREATE TABLE weather_data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP,
    location TEXT,
    temperature FLOAT,
    humidity FLOAT,
    wind_speed FLOAT
);

-- Merge tables into a single view
CREATE TABLE merged_data AS
SELECT
    p.timestamp,
    p.location,
    p.pm25,
    p.co,
    p.o3,
    w.temperature,
    w.humidity,
    w.wind_speed
FROM pollution_data p
JOIN weather_data w
ON p.timestamp = w.timestamp AND p.location = w.location;

-- Sample query to extract data for ML or analysis
SELECT 
    timestamp,
    location,
    pm25,
    temperature,
    humidity,
    wind_speed
FROM merged_data
WHERE location = 'Los Angeles'
  AND timestamp BETWEEN '2024-05-01' AND '2024-05-31'
ORDER BY timestamp;
