# Doctor Patient Management System

A backend application built using **FastAPI** for managing Doctors, Patients, Users, Authentication, and Doctor-Patient assignments.

## Technologies Used

* Python
* FastAPI
* Pydantic
* SQLAlchemy
* SQLite
* JWT Authentication
* bcrypt
* Uvicorn
* Swagger UI

## Project Structure

```text
doctor_patient_management_system/
│
├── .env
├── requirements.txt
├── doctor_patient.db
│
└── app/
    ├── __init__.py
    ├── main.py
    ├── database.py
    ├── config.py
    │
    ├── models/
    │   ├── __init__.py
    │   ├── user.py
    │   ├── doctor.py
    │   ├── patient.py
    │   └── assignment.py
    │
    ├── schemas/
    │   ├── __init__.py
    │   ├── auth.py
    │   ├── doctor.py
    │   └── patient.py
    │
    ├── auth/
    │   ├── __init__.py
    │   └── auth.py
    │
    ├── services/
    │   ├── __init__.py
    │   ├── doctor_service.py
    │   └── patient_service.py
    │
    └── routers/
        ├── __init__.py
        ├── auth.py
        ├── doctors.py
        └── patients.py
```

## Features

### Authentication

* User registration
* User login
* JWT authentication
* Password hashing using bcrypt
* Role-based authorization

### Roles

#### Admin

Admin users can:

* Create doctors
* View doctors
* Update doctors
* Deactivate doctors
* Create patients
* View patients
* Assign patients to doctors

#### Doctor

Doctors can:

* Login using username and password
* View doctors
* View their own assigned patients
* View individual patients only when assigned to them

## API Endpoints

### Authentication

| Method | Endpoint         | Description             |
| ------ | ---------------- | ----------------------- |
| POST   | `/auth/register` | Register a user         |
| POST   | `/auth/login`    | Login and get JWT token |

### Doctors

| Method | Endpoint                                     | Description                    |
| ------ | -------------------------------------------- | ------------------------------ |
| POST   | `/doctors`                                   | Create doctor                  |
| GET    | `/doctors`                                   | Get all active doctors         |
| GET    | `/doctors/{doctor_id}`                       | Get doctor by ID               |
| PUT    | `/doctors/{doctor_id}`                       | Update doctor                  |
| DELETE | `/doctors/{doctor_id}`                       | Deactivate doctor              |
| POST   | `/doctors/{doctor_id}/patients/{patient_id}` | Assign patient                 |
| GET    | `/doctors/{doctor_id}/patients`              | Get doctor's assigned patients |

### Patients

| Method | Endpoint                 | Description       |
| ------ | ------------------------ | ----------------- |
| POST   | `/patients`              | Create patient    |
| GET    | `/patients`              | Get all patients  |
| GET    | `/patients/{patient_id}` | Get patient by ID |

## Installation

Clone or download the project and open the project folder in VS Code.

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install fastapi uvicorn sqlalchemy python-jose[cryptography] bcrypt python-dotenv email-validator python-multipart
```

## Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=sqlite:///./doctor_patient.db
SECRET_KEY=my_super_secret_key_123456
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## Run the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The application will run at:

```text
http://127.0.0.1:8000
```

## Swagger Documentation

Open:

```text
http://127.0.0.1:8000/docs
```

Swagger UI can be used to test all API endpoints.

## Testing Flow

### 1. Register Admin

Endpoint:

```text
POST /auth/register
```

Request:

```json
{
  "username": "admin",
  "email": "admin@gmail.com",
  "password": "admin123",
  "role": "admin"
}
```

### 2. Login

Endpoint:

```text
POST /auth/login
```

Use:

```text
username: admin
password: admin123
```

The API returns a JWT access token.

### 3. Authorize Swagger

Click the **Authorize** button in Swagger.

Enter:

```text
username: admin
password: admin123
```

Then click **Authorize**.

### 4. Create Doctor

Endpoint:

```text
POST /doctors
```

Request:

```json
{
  "name": "Dr. Kumar",
  "specialization": "Cardiology",
  "email": "kumar@gmail.com",
  "username": "kumar",
  "password": "doctor123"
}
```

### 5. Create Patient

Endpoint:

```text
POST /patients
```

Request:

```json
{
  "name": "Rahul",
  "age": 25,
  "phone": "9876543210"
}
```

### 6. Assign Patient

Endpoint:

```text
POST /doctors/{doctor_id}/patients/{patient_id}
```

Example:

```text
POST /doctors/1/patients/1
```

### 7. Get Doctor's Patients

Endpoint:

```text
GET /doctors/{doctor_id}/patients
```

Example:

```text
GET /doctors/1/patients
```

## Validation

The application validates:

* Email format
* Unique doctor email
* Unique username
* Unique user email
* Patient age must be greater than 0
* Patient phone must contain 10–15 digits
* Valid JWT token
* Role-based access
* Doctor access to assigned patients only

## Soft Delete

Doctors are not permanently deleted from the database.

When an admin deletes a doctor:

```text
is_active = false
```

This keeps the doctor record in the database while making the doctor inactive.

## Database

The project uses SQLite.

Database file:

```text
doctor_patient.db
```

The main tables are:

```text
users
doctors
patients
assignments
```

## API Documentation

FastAPI automatically provides:

```text
Swagger UI:
http://127.0.0.1:8000/docs

ReDoc:
http://127.0.0.1:8000/redoc
```

## Project Status

The project includes:

* FastAPI application
* SQLite database
* SQLAlchemy models
* Pydantic schemas
* JWT authentication
* Password hashing
* Role-based authorization
* Doctor management
* Patient management
* Doctor-patient assignment
* Input validation
* Soft delete
* Swagger API documentation
