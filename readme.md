# DigiTwin – Academic Infrastructure Digital Twin System

DigiTwin is a full-stack web application that models, monitors, and optimizes academic infrastructure such as classrooms and laboratories using the concept of a **Digital Twin**.

It helps institutions track space usage, identify inefficiencies, generate optimization suggestions, collect geo-fenced feedback, and raise predictive maintenance alerts through a role-based dashboard.

---

## Features

### 1. Digital Twin Modeling
- Digitally represents classrooms and laboratories
- Stores details such as capacity, building, room type, and usage data
- Helps visualize infrastructure in a structured and scalable way

### 2. Utilization Analytics
- Tracks actual vs scheduled usage
- Identifies idle and overutilized rooms
- Displays charts, summaries, and room-level insights

### 3. Optimization Engine
- Uses heuristic logic to balance room utilization
- Suggests schedule adjustments
- Ensures compatibility based on capacity, room type, and building

### 4. Feedback + Maintenance System
- Allows geo-fenced issue reporting
- Automatically creates maintenance alerts for reported issues
- Improves responsiveness and infrastructure management

### 5. Role-Based Access Control
- **Admin** → full access
- **Manager** → analytics and optimization access
- **User** → dashboard access and feedback submission

---

## Tech Stack

### Backend
- FastAPI
- Python
- SQLAlchemy
- SQLite

### Frontend
- React (Vite)
- Axios
- Chart.js

---

## Project Structure

```bash
digitwin/
├── backend/
│   ├── venv/                       # create here only
│   ├── requirements.txt
│   ├── .env
│   └── app/
│       ├── __init__.py
│       ├── main.py
│       ├── core/
│       │   ├── __init__.py
│       │   └── config.py
│       ├── db/
│       │   ├── __init__.py
│       │   └── database.py
│       ├── models/
│       │   ├── __init__.py
│       │   ├── user.py
│       │   ├── space.py
│       │   ├── utilization.py
│       │   ├── schedule.py
│       │   ├── feedback.py
│       │   └── maintenance.py
│       ├── schemas/
│       │   ├── __init__.py
│       │   ├── user.py
│       │   ├── space.py
│       │   ├── utilization.py
│       │   ├── schedule.py
│       │   ├── feedback.py
│       │   └── maintenance.py
│       ├── routers/
│       │   ├── __init__.py
│       │   ├── auth.py
│       │   ├── spaces.py
│       │   ├── utilization.py
│       │   ├── dashboard.py
│       │   ├── optimization.py
│       │   ├── feedback.py
│       │   └── maintenance.py
│       ├── services/
│       │   ├── __init__.py
│       │   ├── analytics_service.py
│       │   ├── optimization_service.py
│       │   └── maintenance_service.py
│       └── utils/
│           ├── __init__.py
│           ├── data_generator.py
│           └── security.py
├── frontend/
│   ├── package.json
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── api/
│       │   └── client.js
│       ├── components/
│       │   ├── RoomCard.jsx
│       │   ├── UtilizationChart.jsx
│       │   └── Layout.jsx
│       └── pages/
│           ├── Login.jsx
│           ├── Dashboard.jsx
│           ├── Spaces.jsx
│           ├── Analytics.jsx
│           ├── Optimization.jsx
│           ├── Feedback.jsx
│           └── Maintenance.jsx
├── docs/
│   ├── architecture/
│   ├── diagrams/
│   └── reports/
├── .gitignore
└── README.md

# Installation Guide

## Prerequisites
Make sure you have installed:
- Python 3.9+
- Node.js (v16+)
- npm

## Backend Setup
```bash
cd digitwin/backend
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
```

## Run backend
```bash
python3 -m uvicorn app.main:app --reload
```
Backend will run at:
[http://127.0.0.1:8000](http://127.0.0.1:8000)

**Swagger Docs:**
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Frontend Setup
```bash
cd digitwin/frontend
npm install
npm run dev
```
Frontend will run at:
[http://localhost:5173](http://localhost:5173)

## Default Usage
### Create Users
Go to Swagger → `/auth/register`
Example JSON:
```json
  "username": "admin",
  "password": "1234",
  "role": "admin"

```
### Login via UI
Use:
- Username: admin
- Password: 1234

## How to Use the System
a) Create spaces (classrooms/labs)
b) Generate demo utilization data
d) View analytics dashboard
e) Run optimization Submit feedback
g) Check maintenance alerts 
 
## Optimization Logic 
the system uses a heuristic-based AI approach:
a) Detects overutilized and idle rooms 
b) Matches compatible spaces 
c) Simulates redistribution 
d) Generates recommendations 
 
## Geo-Fencing 
a) Feedback is only accepted if user is near the selected space 
b) Uses Haversine distance calculation 
 
## Demo Data 
synthetic data is generated to simulate real-world usage patterns:
a) Idle spaces 
b) Normal usage 
c) Overutilized spaces 
 
## Future Enhancements
a) Machine learning-based prediction) IoT sensor integration) Real-time scheduling system) Cloud deployment"""