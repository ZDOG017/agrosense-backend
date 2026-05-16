from sqlalchemy import text
from sqlalchemy.orm import Session


def get_dashboard_summary(db: Session) -> dict:
    summary_query = text(
        """
        SELECT
            (SELECT COUNT(*) FROM fields) AS total_fields,
            (SELECT COUNT(*) FROM crops WHERE status = 'Active') AS active_crops,
            (SELECT COUNT(*) FROM sensors WHERE status = 'Online') AS online_sensors,
            (SELECT COUNT(*) FROM sensors WHERE status = 'Offline') AS offline_sensors,
            (SELECT COUNT(*) FROM sensor_readings WHERE alert_level = 'Critical') AS critical_alerts,
            (SELECT COUNT(*) FROM irrigation_schedules WHERE status = 'Scheduled') AS scheduled_irrigations,
            (SELECT COUNT(*) FROM tasks WHERE status = 'Pending') AS pending_tasks,
            COALESCE((SELECT SUM(quantity_kg) FROM harvest_records), 0) AS total_harvest_kg,
            COALESCE((SELECT SUM(revenue) FROM harvest_records), 0) AS total_revenue
        """
    )
    return dict(db.execute(summary_query).mappings().one())


def get_low_moisture_fields(db: Session) -> list[dict]:
    query = text(
        """
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
        ORDER BY lm.reading_value ASC, f.field_name ASC
        """
    )
    return [dict(row) for row in db.execute(query).mappings().all()]


def get_water_usage_by_field(db: Session) -> list[dict]:
    query = text(
        """
        SELECT
            f.field_id,
            f.field_name,
            COUNT(i.irrigation_id) AS irrigation_count,
            COALESCE(SUM(i.water_amount_liters), 0) AS total_water_liters,
            COALESCE(SUM(i.duration_minutes), 0) AS total_duration_minutes
        FROM fields f
        LEFT JOIN irrigation_schedules i ON i.field_id = f.field_id
        GROUP BY f.field_id, f.field_name
        ORDER BY total_water_liters DESC, f.field_name ASC
        """
    )
    return [dict(row) for row in db.execute(query).mappings().all()]


def get_crops_ready_for_harvest(db: Session) -> list[dict]:
    query = text(
        """
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
        ORDER BY c.expected_harvest_date ASC, c.crop_name ASC
        """
    )
    return [dict(row) for row in db.execute(query).mappings().all()]


def get_tasks_by_employee(db: Session) -> list[dict]:
    query = text(
        """
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
        ORDER BY completed_tasks DESC, total_tasks DESC, u.full_name ASC
        """
    )
    return [dict(row) for row in db.execute(query).mappings().all()]


def get_offline_sensors(db: Session) -> list[dict]:
    query = text(
        """
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
        ORDER BY s.status ASC, f.field_name ASC, s.sensor_id ASC
        """
    )
    return [dict(row) for row in db.execute(query).mappings().all()]


def get_harvest_revenue_report(db: Session) -> list[dict]:
    query = text(
        """
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
        ORDER BY total_revenue DESC, c.crop_name ASC
        """
    )
    return [dict(row) for row in db.execute(query).mappings().all()]


def get_treatment_costs_by_field(db: Session) -> list[dict]:
    query = text(
        """
        SELECT
            f.field_id,
            f.field_name,
            COUNT(t.treatment_id) AS treatment_count,
            COALESCE(SUM(t.cost), 0) AS total_treatment_cost
        FROM fields f
        LEFT JOIN treatments t ON t.field_id = f.field_id
        GROUP BY f.field_id, f.field_name
        ORDER BY total_treatment_cost DESC, f.field_name ASC
        """
    )
    return [dict(row) for row in db.execute(query).mappings().all()]
