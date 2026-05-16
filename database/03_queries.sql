-- AgroSense Smart Farming Database Management System
-- 03_queries.sql
-- Management queries used by the report endpoints.

WITH latest_moisture AS (
    SELECT
        se.field_id,
        sr.sensor_id,
        sr.reading_value,
        sr.alert_level,
        sr.reading_time,
        ROW_NUMBER() OVER (
            PARTITION BY se.field_id
            ORDER BY sr.reading_time DESC, sr.reading_id DESC
        ) AS row_num
    FROM sensor_readings sr
    JOIN sensors se ON se.sensor_id = sr.sensor_id
    WHERE se.sensor_type = 'Soil Moisture'
)
SELECT
    f.field_id,
    f.field_name,
    f.location,
    lm.sensor_id,
    lm.reading_value AS latest_moisture,
    lm.alert_level,
    lm.reading_time
FROM latest_moisture lm
JOIN fields f ON f.field_id = lm.field_id
WHERE lm.row_num = 1
  AND lm.reading_value < 40
ORDER BY lm.reading_value ASC, f.field_name ASC;

SELECT
    f.field_id,
    f.field_name,
    COUNT(i.irrigation_id) AS irrigation_count,
    COALESCE(SUM(i.water_amount_liters), 0) AS total_water_liters,
    COALESCE(SUM(i.duration_minutes), 0) AS total_duration_minutes
FROM fields f
LEFT JOIN irrigation_schedules i ON i.field_id = f.field_id
GROUP BY f.field_id, f.field_name
ORDER BY total_water_liters DESC, f.field_name ASC;

SELECT
    c.crop_id,
    c.crop_name,
    f.field_name,
    c.expected_harvest_date,
    c.growth_stage,
    c.status
FROM crops c
JOIN fields f ON f.field_id = c.field_id
WHERE c.status = 'Active'
  AND c.expected_harvest_date IS NOT NULL
  AND c.expected_harvest_date <= CURRENT_DATE + INTERVAL '7 days'
ORDER BY c.expected_harvest_date ASC, c.crop_name ASC;

SELECT
    u.user_id,
    u.full_name,
    r.role_name,
    COUNT(t.task_id) AS total_tasks,
    COUNT(CASE WHEN t.status = 'Completed' THEN 1 END) AS completed_tasks,
    COUNT(CASE WHEN t.status IN ('Pending', 'In Progress') THEN 1 END) AS open_tasks
FROM users u
JOIN roles r ON r.role_id = u.role_id
LEFT JOIN tasks t ON t.assigned_to = u.user_id
GROUP BY u.user_id, u.full_name, r.role_name
ORDER BY completed_tasks DESC, total_tasks DESC, u.full_name ASC;

SELECT
    s.sensor_id,
    s.sensor_type,
    s.status,
    s.installed_date,
    f.field_name,
    f.location
FROM sensors s
JOIN fields f ON f.field_id = s.field_id
WHERE s.status IN ('Offline', 'Maintenance')
ORDER BY s.status ASC, f.field_name ASC, s.sensor_id ASC;

SELECT
    c.crop_id,
    c.crop_name,
    COUNT(h.harvest_id) AS harvest_count,
    COALESCE(SUM(h.quantity_kg), 0) AS total_quantity_kg,
    COALESCE(SUM(h.revenue), 0) AS total_revenue,
    COALESCE(AVG(h.revenue), 0) AS average_revenue
FROM crops c
LEFT JOIN harvest_records h ON h.crop_id = c.crop_id
GROUP BY c.crop_id, c.crop_name
HAVING COUNT(h.harvest_id) > 0
ORDER BY total_revenue DESC, c.crop_name ASC;

SELECT
    f.field_id,
    f.field_name,
    COUNT(t.treatment_id) AS treatment_count,
    COALESCE(SUM(t.cost), 0) AS total_treatment_cost
FROM fields f
LEFT JOIN treatments t ON t.field_id = f.field_id
GROUP BY f.field_id, f.field_name
ORDER BY total_treatment_cost DESC, f.field_name ASC;
