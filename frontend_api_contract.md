# AgroSense Frontend API Contract

## 1. Backend Base URL

- Local: `http://127.0.0.1:8000`
- Production placeholder: `https://agrosense-backend-0eqo.onrender.com`

## 2. Swagger Docs URL

- Local Swagger: `http://127.0.0.1:8000/docs`
- Production Swagger: `https://agrosense-backend-0eqo.onrender.com/docs`

## 3. Suggested Frontend Pages

- Login Page
- Dashboard Page
- Fields & Crops Page
- Sensors & Readings Page
- Irrigation Page
- Tasks Page
- Reports Page

## 4. Authentication Instructions

1. Log in by sending `POST /auth/login`.
2. Store the returned `access_token` in `localStorage`.
3. Send the token in every protected request:

```http
Authorization: Bearer <token>
```

4. Use `GET /auth/me` after login to restore the session and show the signed-in user.

## 5. Suggested UI Behavior

- Use tables for list pages.
- Use forms or modal forms for create and update operations.
- Add delete buttons with confirmation prompts.
- Use dashboard cards for summary counts.
- Show reports in tables and optional charts.
- Highlight critical sensor alerts and overdue tasks with warning colors.

## 6. Endpoints By Module

### Authentication

- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`

### Roles

- `GET /roles`

### Users

- `GET /users`
- `GET /users/{id}`
- `POST /users`
- `PUT /users/{id}`
- `DELETE /users/{id}`

### Fields

- `GET /fields`
- `GET /fields/{id}`
- `POST /fields`
- `PUT /fields/{id}`
- `DELETE /fields/{id}`

### Crops

- `GET /crops`
- `GET /crops/{id}`
- `POST /crops`
- `PUT /crops/{id}`
- `DELETE /crops/{id}`

### Sensors

- `GET /sensors`
- `GET /sensors/{id}`
- `POST /sensors`
- `PUT /sensors/{id}`
- `DELETE /sensors/{id}`

### Sensor Readings

- `GET /sensor-readings`
- `GET /sensor-readings/{id}`
- `POST /sensor-readings`
- `DELETE /sensor-readings/{id}`

### Irrigation

- `GET /irrigation`
- `GET /irrigation/{id}`
- `POST /irrigation`
- `PUT /irrigation/{id}`
- `DELETE /irrigation/{id}`

### Tasks

- `GET /tasks`
- `GET /tasks/{id}`
- `POST /tasks`
- `PUT /tasks/{id}`
- `DELETE /tasks/{id}`

### Treatments

- `GET /treatments`
- `GET /treatments/{id}`
- `POST /treatments`
- `PUT /treatments/{id}`
- `DELETE /treatments/{id}`

### Harvest Records

- `GET /harvests`
- `GET /harvests/{id}`
- `POST /harvests`
- `PUT /harvests/{id}`
- `DELETE /harvests/{id}`

### Dashboard

- `GET /dashboard/summary`

### Reports

- `GET /reports/low-moisture-fields`
- `GET /reports/water-usage-by-field`
- `GET /reports/crops-ready-for-harvest`
- `GET /reports/tasks-by-employee`
- `GET /reports/offline-sensors`
- `GET /reports/harvest-revenue`
- `GET /reports/treatment-costs`

## 7. Example Requests And Responses

### Login Request

```json
{
  "email": "admin@farm.com",
  "password": "Admin123!"
}
```

### Login Response

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "user_id": 1,
    "full_name": "Aylin Demir",
    "email": "admin@farm.com",
    "role": "Admin"
  }
}
```

### Create Field Request

```json
{
  "field_name": "Demo Field",
  "location": "Nicosia Zone X",
  "area_hectares": 7.5,
  "soil_type": "Loamy",
  "status": "Healthy"
}
```

### Create Crop Request

```json
{
  "field_id": 1,
  "crop_name": "Pepper",
  "planting_date": "2026-05-01",
  "expected_harvest_date": "2026-08-15",
  "growth_stage": "Seedling",
  "water_requirement_mm": 15.0,
  "status": "Active"
}
```

### Create Sensor Reading Request

```json
{
  "sensor_id": 1,
  "reading_value": 23.4,
  "unit": "%"
}
```

### Dashboard Response

```json
{
  "total_fields": 5,
  "active_crops": 5,
  "online_sensors": 6,
  "offline_sensors": 1,
  "critical_alerts": 2,
  "scheduled_irrigations": 3,
  "pending_tasks": 3,
  "total_harvest_kg": 8390,
  "total_revenue": 26453
}
```

### Report Response Example: Low Moisture Fields

```json
[
  {
    "field_id": 1,
    "field_name": "North Field",
    "location": "Morphou Zone A",
    "sensor_id": 1,
    "latest_moisture": 22.4,
    "alert_level": "Critical",
    "reading_time": "2026-05-16T07:30:00"
  }
]
```

## 8. Frontend Notes

- Every module can use the same pattern:
  list page -> create form -> update form -> delete action.
- For admin-style pages, show current role in the UI and optionally hide restricted actions for non-admin users.
- The reports page can combine table views and chart cards using the report endpoints.
- Sensor pages should poll or refresh manually if you want near-real-time behavior.

