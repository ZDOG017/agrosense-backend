-- AgroSense Smart Farming Database Management System
-- CMPE344 Database Management Systems and Programming II
-- 01_schema.sql

DROP TABLE IF EXISTS harvest_records CASCADE;
DROP TABLE IF EXISTS treatments CASCADE;
DROP TABLE IF EXISTS tasks CASCADE;
DROP TABLE IF EXISTS irrigation_schedules CASCADE;
DROP TABLE IF EXISTS sensor_readings CASCADE;
DROP TABLE IF EXISTS sensors CASCADE;
DROP TABLE IF EXISTS crops CASCADE;
DROP TABLE IF EXISTS fields CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS roles CASCADE;

CREATE TABLE roles (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role_id INTEGER NOT NULL REFERENCES roles(role_id),
    status VARCHAR(20) NOT NULL DEFAULT 'Active',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT ck_users_status CHECK (status IN ('Active', 'Inactive'))
);

CREATE TABLE fields (
    field_id SERIAL PRIMARY KEY,
    field_name VARCHAR(100) NOT NULL,
    location VARCHAR(100),
    area_hectares NUMERIC(10, 2) NOT NULL,
    soil_type VARCHAR(50),
    status VARCHAR(50) NOT NULL DEFAULT 'Healthy',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT ck_fields_area_positive CHECK (area_hectares > 0),
    CONSTRAINT ck_fields_status CHECK (
        status IN ('Healthy', 'Needs Irrigation', 'Under Treatment', 'Ready for Harvest')
    )
);

CREATE TABLE crops (
    crop_id SERIAL PRIMARY KEY,
    field_id INTEGER NOT NULL REFERENCES fields(field_id) ON DELETE CASCADE,
    crop_name VARCHAR(100) NOT NULL,
    planting_date DATE NOT NULL,
    expected_harvest_date DATE,
    growth_stage VARCHAR(50) NOT NULL DEFAULT 'Seedling',
    water_requirement_mm NUMERIC(10, 2),
    status VARCHAR(30) NOT NULL DEFAULT 'Active',
    CONSTRAINT ck_crops_growth_stage CHECK (
        growth_stage IN ('Seedling', 'Vegetative', 'Flowering', 'Fruiting', 'Harvest Ready')
    ),
    CONSTRAINT ck_crops_status CHECK (status IN ('Active', 'Harvested', 'Failed'))
);

CREATE TABLE sensors (
    sensor_id SERIAL PRIMARY KEY,
    field_id INTEGER NOT NULL REFERENCES fields(field_id) ON DELETE CASCADE,
    sensor_type VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Online',
    installed_date DATE NOT NULL DEFAULT CURRENT_DATE,
    CONSTRAINT ck_sensors_type CHECK (
        sensor_type IN ('Soil Moisture', 'Temperature', 'Humidity', 'pH', 'Light', 'Water Level')
    ),
    CONSTRAINT ck_sensors_status CHECK (status IN ('Online', 'Offline', 'Maintenance'))
);

CREATE TABLE sensor_readings (
    reading_id SERIAL PRIMARY KEY,
    sensor_id INTEGER NOT NULL REFERENCES sensors(sensor_id) ON DELETE CASCADE,
    reading_value NUMERIC(10, 2) NOT NULL,
    unit VARCHAR(20) NOT NULL,
    reading_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    alert_level VARCHAR(20) NOT NULL DEFAULT 'Normal',
    CONSTRAINT ck_sensor_readings_alert_level CHECK (alert_level IN ('Normal', 'Warning', 'Critical'))
);

CREATE TABLE irrigation_schedules (
    irrigation_id SERIAL PRIMARY KEY,
    field_id INTEGER NOT NULL REFERENCES fields(field_id) ON DELETE CASCADE,
    scheduled_time TIMESTAMP NOT NULL,
    duration_minutes INTEGER NOT NULL,
    water_amount_liters NUMERIC(10, 2) NOT NULL,
    mode VARCHAR(20) NOT NULL DEFAULT 'Manual',
    status VARCHAR(20) NOT NULL DEFAULT 'Scheduled',
    created_by INTEGER REFERENCES users(user_id),
    CONSTRAINT ck_irrigation_duration_positive CHECK (duration_minutes > 0),
    CONSTRAINT ck_irrigation_water_positive CHECK (water_amount_liters > 0),
    CONSTRAINT ck_irrigation_mode CHECK (mode IN ('Manual', 'Automatic')),
    CONSTRAINT ck_irrigation_status CHECK (status IN ('Scheduled', 'Completed', 'Cancelled'))
);

CREATE TABLE tasks (
    task_id SERIAL PRIMARY KEY,
    assigned_to INTEGER REFERENCES users(user_id),
    field_id INTEGER REFERENCES fields(field_id) ON DELETE SET NULL,
    task_title VARCHAR(150) NOT NULL,
    description TEXT,
    priority VARCHAR(20) NOT NULL DEFAULT 'Medium',
    status VARCHAR(20) NOT NULL DEFAULT 'Pending',
    due_date DATE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT ck_tasks_priority CHECK (priority IN ('Low', 'Medium', 'High')),
    CONSTRAINT ck_tasks_status CHECK (status IN ('Pending', 'In Progress', 'Completed', 'Cancelled'))
);

CREATE TABLE treatments (
    treatment_id SERIAL PRIMARY KEY,
    field_id INTEGER NOT NULL REFERENCES fields(field_id) ON DELETE CASCADE,
    crop_id INTEGER REFERENCES crops(crop_id) ON DELETE SET NULL,
    treatment_type VARCHAR(50) NOT NULL,
    material_used VARCHAR(100),
    quantity NUMERIC(10, 2),
    unit VARCHAR(20),
    treatment_date DATE NOT NULL DEFAULT CURRENT_DATE,
    cost NUMERIC(10, 2) NOT NULL DEFAULT 0,
    responsible_user_id INTEGER REFERENCES users(user_id),
    CONSTRAINT ck_treatments_type CHECK (
        treatment_type IN ('Fertilizer', 'Pesticide', 'Soil Improvement', 'Disease Control')
    ),
    CONSTRAINT ck_treatments_quantity_non_negative CHECK (quantity >= 0),
    CONSTRAINT ck_treatments_cost_non_negative CHECK (cost >= 0)
);

CREATE TABLE harvest_records (
    harvest_id SERIAL PRIMARY KEY,
    crop_id INTEGER NOT NULL REFERENCES crops(crop_id) ON DELETE CASCADE,
    field_id INTEGER NOT NULL REFERENCES fields(field_id) ON DELETE CASCADE,
    harvest_date DATE NOT NULL DEFAULT CURRENT_DATE,
    quantity_kg NUMERIC(10, 2) NOT NULL,
    quality_grade VARCHAR(10),
    price_per_kg NUMERIC(10, 2) NOT NULL,
    revenue NUMERIC(12, 2),
    CONSTRAINT ck_harvest_quantity_positive CHECK (quantity_kg > 0),
    CONSTRAINT ck_harvest_price_non_negative CHECK (price_per_kg >= 0),
    CONSTRAINT ck_harvest_quality_grade CHECK (quality_grade IN ('A', 'B', 'C'))
);
