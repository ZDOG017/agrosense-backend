-- AgroSense Smart Farming Database Management System
-- 04_functions_triggers.sql
-- PL/pgSQL functions, procedures, and triggers for automation rules.

DROP TRIGGER IF EXISTS trg_set_sensor_alert_level ON sensor_readings;
DROP TRIGGER IF EXISTS trg_update_field_status_on_critical_moisture ON sensor_readings;
DROP TRIGGER IF EXISTS trg_calculate_harvest_revenue ON harvest_records;
DROP TRIGGER IF EXISTS trg_mark_crop_harvested ON harvest_records;

DROP FUNCTION IF EXISTS set_sensor_alert_level();
DROP FUNCTION IF EXISTS update_field_status_on_critical_moisture();
DROP FUNCTION IF EXISTS calculate_harvest_revenue(NUMERIC, NUMERIC);
DROP FUNCTION IF EXISTS apply_harvest_revenue();
DROP FUNCTION IF EXISTS count_completed_tasks_by_employee(INTEGER);
DROP FUNCTION IF EXISTS mark_crop_harvested();
DROP PROCEDURE IF EXISTS mark_irrigation_completed(INTEGER);

CREATE OR REPLACE FUNCTION set_sensor_alert_level()
RETURNS TRIGGER AS $$
DECLARE
    current_sensor_type VARCHAR(50);
BEGIN
    SELECT sensor_type
    INTO current_sensor_type
    FROM sensors
    WHERE sensor_id = NEW.sensor_id;

    IF current_sensor_type = 'Soil Moisture' THEN
        IF NEW.reading_value < 25 THEN
            NEW.alert_level := 'Critical';
        ELSIF NEW.reading_value BETWEEN 25 AND 40 THEN
            NEW.alert_level := 'Warning';
        ELSE
            NEW.alert_level := 'Normal';
        END IF;
    ELSE
        NEW.alert_level := 'Normal';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_set_sensor_alert_level
BEFORE INSERT OR UPDATE ON sensor_readings
FOR EACH ROW
EXECUTE FUNCTION set_sensor_alert_level();

CREATE OR REPLACE FUNCTION update_field_status_on_critical_moisture()
RETURNS TRIGGER AS $$
DECLARE
    related_field_id INTEGER;
    current_sensor_type VARCHAR(50);
BEGIN
    SELECT field_id, sensor_type
    INTO related_field_id, current_sensor_type
    FROM sensors
    WHERE sensor_id = NEW.sensor_id;

    IF current_sensor_type = 'Soil Moisture' AND NEW.alert_level = 'Critical' THEN
        UPDATE fields
        SET status = 'Needs Irrigation'
        WHERE field_id = related_field_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_field_status_on_critical_moisture
AFTER INSERT OR UPDATE ON sensor_readings
FOR EACH ROW
EXECUTE FUNCTION update_field_status_on_critical_moisture();

CREATE OR REPLACE FUNCTION calculate_harvest_revenue(
    p_quantity_kg NUMERIC,
    p_price_per_kg NUMERIC
)
RETURNS NUMERIC AS $$
BEGIN
    RETURN COALESCE(p_quantity_kg, 0) * COALESCE(p_price_per_kg, 0);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION apply_harvest_revenue()
RETURNS TRIGGER AS $$
BEGIN
    NEW.revenue := calculate_harvest_revenue(NEW.quantity_kg, NEW.price_per_kg);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_calculate_harvest_revenue
BEFORE INSERT OR UPDATE ON harvest_records
FOR EACH ROW
EXECUTE FUNCTION apply_harvest_revenue();

CREATE OR REPLACE FUNCTION count_completed_tasks_by_employee(p_user_id INTEGER)
RETURNS INTEGER AS $$
DECLARE
    completed_count INTEGER;
BEGIN
    SELECT COUNT(*)
    INTO completed_count
    FROM tasks
    WHERE assigned_to = p_user_id
      AND status = 'Completed';

    RETURN completed_count;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE mark_irrigation_completed(p_irrigation_id INTEGER)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE irrigation_schedules
    SET status = 'Completed'
    WHERE irrigation_id = p_irrigation_id;
END;
$$;

CREATE OR REPLACE FUNCTION mark_crop_harvested()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE crops
    SET status = 'Harvested',
        growth_stage = 'Harvest Ready'
    WHERE crop_id = NEW.crop_id;

    UPDATE fields
    SET status = 'Ready for Harvest'
    WHERE field_id = NEW.field_id
      AND status <> 'Needs Irrigation';

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_mark_crop_harvested
AFTER INSERT ON harvest_records
FOR EACH ROW
EXECUTE FUNCTION mark_crop_harvested();
