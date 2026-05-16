-- AgroSense Smart Farming Database Management System
-- 02_seed_data.sql
-- Demo seed data for reports, dashboard statistics, and API testing.

INSERT INTO roles (role_name, description) VALUES
('Admin', 'System administrator with full access'),
('Farm Manager', 'Manages fields, crops, irrigation, and staff'),
('Employee', 'Carries out daily farm operations'),
('Technician', 'Maintains sensors and smart farm equipment');

-- Password for all demo accounts: Admin123!
INSERT INTO users (full_name, email, password_hash, role_id, status) VALUES
('Aylin Demir', 'admin@farm.com', '$2b$12$v/QTRBCd1bLHv.Phgp6c/.k1tzTj4XPA9wcYXj4IlZM1ZaFkzA5Me', 1, 'Active'),
('Kemal Yildiz', 'manager@farm.com', '$2b$12$v/QTRBCd1bLHv.Phgp6c/.k1tzTj4XPA9wcYXj4IlZM1ZaFkzA5Me', 2, 'Active'),
('Merve Kaya', 'employee1@farm.com', '$2b$12$v/QTRBCd1bLHv.Phgp6c/.k1tzTj4XPA9wcYXj4IlZM1ZaFkzA5Me', 3, 'Active'),
('Can Arslan', 'employee2@farm.com', '$2b$12$v/QTRBCd1bLHv.Phgp6c/.k1tzTj4XPA9wcYXj4IlZM1ZaFkzA5Me', 3, 'Active'),
('Selin Aksoy', 'tech@farm.com', '$2b$12$v/QTRBCd1bLHv.Phgp6c/.k1tzTj4XPA9wcYXj4IlZM1ZaFkzA5Me', 4, 'Active');

INSERT INTO fields (field_name, location, area_hectares, soil_type, status) VALUES
('North Field', 'Morphou Zone A', 12.50, 'Loamy', 'Needs Irrigation'),
('East Orchard', 'Morphou Zone B', 8.20, 'Sandy Loam', 'Healthy'),
('South Greenhouse', 'Nicosia Zone C', 4.75, 'Clay Loam', 'Under Treatment'),
('West Field', 'Guzelyurt Zone D', 10.00, 'Silt Loam', 'Ready for Harvest'),
('River Plot', 'Kyrenia Zone E', 6.80, 'Loamy', 'Healthy');

INSERT INTO crops (
    field_id, crop_name, planting_date, expected_harvest_date, growth_stage, water_requirement_mm, status
) VALUES
(1, 'Tomato', '2026-02-10', '2026-05-20', 'Fruiting', 18.50, 'Active'),
(2, 'Olive', '2025-11-15', '2026-09-10', 'Vegetative', 12.00, 'Active'),
(3, 'Cucumber', '2026-03-01', '2026-05-24', 'Flowering', 16.25, 'Active'),
(4, 'Wheat', '2025-12-10', '2026-05-18', 'Harvest Ready', 20.00, 'Active'),
(5, 'Strawberry', '2026-01-20', '2026-05-22', 'Fruiting', 14.75, 'Active');

INSERT INTO sensors (field_id, sensor_type, status, installed_date) VALUES
(1, 'Soil Moisture', 'Online', '2026-01-15'),
(1, 'Temperature', 'Online', '2026-01-15'),
(2, 'Soil Moisture', 'Online', '2026-01-20'),
(2, 'Humidity', 'Offline', '2026-01-20'),
(3, 'Soil Moisture', 'Online', '2026-02-01'),
(3, 'pH', 'Maintenance', '2026-02-01'),
(4, 'Soil Moisture', 'Online', '2026-01-10'),
(5, 'Water Level', 'Online', '2026-02-12');

INSERT INTO sensor_readings (sensor_id, reading_value, unit, reading_time, alert_level) VALUES
(1, 22.40, '%', '2026-05-16 07:30:00', 'Critical'),
(1, 27.10, '%', '2026-05-15 07:30:00', 'Warning'),
(1, 35.80, '%', '2026-05-14 07:30:00', 'Warning'),
(2, 29.30, 'C', '2026-05-16 07:35:00', 'Normal'),
(2, 28.70, 'C', '2026-05-15 07:35:00', 'Normal'),
(3, 41.50, '%', '2026-05-16 08:00:00', 'Normal'),
(3, 38.00, '%', '2026-05-15 08:00:00', 'Warning'),
(4, 61.20, '%', '2026-05-16 08:10:00', 'Normal'),
(5, 31.50, '%', '2026-05-16 09:00:00', 'Warning'),
(5, 24.90, '%', '2026-05-15 09:00:00', 'Critical'),
(6, 6.20, 'pH', '2026-05-16 09:15:00', 'Normal'),
(7, 45.80, '%', '2026-05-16 10:00:00', 'Normal'),
(7, 43.10, '%', '2026-05-15 10:00:00', 'Normal'),
(8, 78.40, 'cm', '2026-05-16 10:20:00', 'Normal'),
(8, 76.10, 'cm', '2026-05-15 10:20:00', 'Normal');

INSERT INTO irrigation_schedules (
    field_id, scheduled_time, duration_minutes, water_amount_liters, mode, status, created_by
) VALUES
(1, '2026-05-16 18:00:00', 40, 1800.00, 'Automatic', 'Scheduled', 2),
(2, '2026-05-17 06:00:00', 30, 1250.00, 'Manual', 'Scheduled', 2),
(3, '2026-05-15 17:30:00', 25, 900.00, 'Automatic', 'Completed', 2),
(4, '2026-05-14 05:45:00', 35, 1500.00, 'Manual', 'Completed', 1),
(5, '2026-05-18 06:30:00', 20, 700.00, 'Scheduled', 'Scheduled', 2);

INSERT INTO tasks (
    assigned_to, field_id, task_title, description, priority, status, due_date
) VALUES
(3, 1, 'Inspect low moisture area', 'Check drip lines in North Field and report leak points.', 'High', 'Pending', '2026-05-16'),
(4, 2, 'Prune olive trees', 'Trim overgrown branches in East Orchard.', 'Medium', 'In Progress', '2026-05-18'),
(3, 3, 'Apply greenhouse fertilizer', 'Use balanced fertilizer in cucumber section.', 'High', 'Completed', '2026-05-14'),
(5, 4, 'Repair sensor enclosure', 'Fix exposed wiring on moisture sensor mast.', 'High', 'Pending', '2026-05-17'),
(4, 5, 'Clean water channel', 'Remove debris near the irrigation intake point.', 'Low', 'Completed', '2026-05-13'),
(3, 4, 'Prepare harvest crates', 'Move clean crates to West Field storage area.', 'Medium', 'Pending', '2026-05-17'),
(5, 3, 'Calibrate pH sensor', 'Run calibration for maintenance sensor.', 'Medium', 'In Progress', '2026-05-16'),
(4, 1, 'Check tomato pests', 'Look for leaf spots and early pest activity.', 'Medium', 'Completed', '2026-05-15');

INSERT INTO treatments (
    field_id, crop_id, treatment_type, material_used, quantity, unit, treatment_date, cost, responsible_user_id
) VALUES
(1, 1, 'Fertilizer', 'NPK 20-20-20', 25.00, 'kg', '2026-05-05', 320.00, 2),
(3, 3, 'Disease Control', 'Copper Fungicide', 8.00, 'L', '2026-05-08', 210.00, 5),
(2, 2, 'Soil Improvement', 'Compost Mix', 150.00, 'kg', '2026-04-28', 180.00, 2),
(4, 4, 'Pesticide', 'Aphid Control Spray', 10.00, 'L', '2026-05-02', 260.00, 5),
(5, 5, 'Fertilizer', 'Berry Booster', 18.00, 'kg', '2026-05-09', 145.00, 2);

INSERT INTO harvest_records (
    crop_id, field_id, harvest_date, quantity_kg, quality_grade, price_per_kg, revenue
) VALUES
(4, 4, '2026-05-15', 4200.00, 'A', 2.10, 8820.00),
(5, 5, '2026-05-10', 850.00, 'A', 4.50, 3825.00),
(1, 1, '2026-05-12', 1200.00, 'B', 2.80, 3360.00),
(3, 3, '2026-05-09', 640.00, 'B', 3.20, 2048.00),
(2, 2, '2026-04-30', 1500.00, 'A', 5.60, 8400.00);
