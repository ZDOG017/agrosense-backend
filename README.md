# AgroSense: Smart Farming Database Management System Backend

## Project Title

AgroSense Smart Farming Database Management System

## Short Description

AgroSense is a FastAPI and PostgreSQL backend built for the CMPE344 Database Management Systems and Programming II course at Cyprus International University. It manages smart farm operations including users, roles, fields, crops, sensors, sensor readings, irrigation schedules, tasks, treatments, harvest records, dashboard statistics, and management reports.

## Technologies Used

- FastAPI
- PostgreSQL
- Supabase PostgreSQL
- SQLAlchemy
- Pydantic
- JWT authentication
- Passlib with bcrypt password hashing
- Render deployment

## Database Tables Summary

The project contains 10 main tables:

1. `roles`
2. `users`
3. `fields`
4. `crops`
5. `sensors`
6. `sensor_readings`
7. `irrigation_schedules`
8. `tasks`
9. `treatments`
10. `harvest_records`

These tables include:

- Primary keys
- Foreign keys
- Check constraints
- Default values
- One-to-many relationships
- Cascading delete rules where appropriate

## How To Run Locally

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Copy `.env.example` to `.env` and update the values.
5. Make sure PostgreSQL is running and the database exists.
6. Start the FastAPI development server:

```bash
uvicorn app.main:app --reload
```

7. Open Swagger documentation:

- `http://127.0.0.1:8000/docs`

## Environment Variables

Create a `.env` file with:

```env
DATABASE_URL=postgresql://username:password@host:port/database
SECRET_KEY=change_this_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## How To Run SQL Scripts In Supabase

Recommended execution order:

1. Run [database/01_schema.sql](/Users/soltan/Documents/Projects/agrosense-backend/database/01_schema.sql)
2. Run [database/04_functions_triggers.sql](/Users/soltan/Documents/Projects/agrosense-backend/database/04_functions_triggers.sql)
3. Run [database/02_seed_data.sql](/Users/soltan/Documents/Projects/agrosense-backend/database/02_seed_data.sql)
4. Review [database/03_queries.sql](/Users/soltan/Documents/Projects/agrosense-backend/database/03_queries.sql)

You can paste each file into the Supabase SQL editor and execute it.

## API Documentation Link

- Local docs: `http://127.0.0.1:8000/docs`
- Render docs: `https://your-agrosense-backend.onrender.com/docs`

## Deployment Instructions For Render

1. Push the repository to GitHub.
2. Create a new Web Service in Render.
3. Connect the GitHub repository.
4. Render will use [render.yaml](/Users/soltan/Documents/Projects/agrosense-backend/render.yaml).
5. Set environment variables in Render:
   `DATABASE_URL`, `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`
6. Use this start command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Example Test Accounts

The seed script creates these demo accounts:

- Admin: `admin@farm.com`
- Farm Manager: `manager@farm.com`
- Employee: `employee1@farm.com`
- Employee: `employee2@farm.com`
- Technician: `tech@farm.com`

Demo password for all accounts:

- `Admin123!`

## Core API Modules

- Authentication
- Roles and users
- Fields and crops
- Sensors and sensor readings
- Irrigation schedules
- Employee tasks
- Treatments
- Harvest records
- Dashboard summary
- Management reports

## Project Requirements Satisfied

This backend satisfies the CMPE344 requirements:

1. At least 6 tables: implemented 10 tables.
2. Users table for login: implemented.
3. User groups and roles: Admin, Farm Manager, Employee, Technician.
4. PK, FK, constraints, defaults, and relationships: implemented in SQL schema and ORM models.
5. DDL and DML scripts: included.
6. 5 to 7 SQL management queries: included 7 report queries.
7. At least 5 procedural SQL blocks: included 7 PL/pgSQL functions, procedures, and triggers.
8. Insert, update, delete, and view APIs: implemented across major entities.
9. Deployable online: Render configuration included.
10. Clear documentation for frontend integration: README and frontend API contract included.

## Project Structure

```text
agrosense-backend/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── config.py
│   ├── auth.py
│   ├── models/
│   ├── schemas/
│   ├── routes/
│   └── services/
├── database/
│   ├── 01_schema.sql
│   ├── 02_seed_data.sql
│   ├── 03_queries.sql
│   └── 04_functions_triggers.sql
├── screenshots/
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
├── render.yaml
└── frontend_api_contract.md
```
