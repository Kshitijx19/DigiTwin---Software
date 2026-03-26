from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import Base, engine
from app.models.space import Space
from app.models.utilization import Utilization
from app.models.schedule import Schedule
from app.models.feedback import Feedback
from app.models.maintenance import MaintenanceAlert
from app.models.user import User

from app.routers.spaces import router as spaces_router
from app.routers.utilization import router as utilization_router
from app.routers.optimization import router as optimization_router
from app.routers.feedback import router as feedback_router
from app.routers.maintenance import router as maintenance_router
from app.routers.auth import router as auth_router
from app.routers.reports import router as reports_router

app = FastAPI(title="DigiTwin API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(spaces_router)
app.include_router(utilization_router)
app.include_router(optimization_router)
app.include_router(feedback_router)
app.include_router(maintenance_router)
app.include_router(auth_router)
app.include_router(reports_router)


@app.get("/")
def home():
    return {"message": "DigiTwin backend running "}