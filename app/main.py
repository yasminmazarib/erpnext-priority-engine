from fastapi import FastAPI
from app.controllers.priority_controller import router as priority_router

app = FastAPI(title="ERPNext Priority Engine")

app.include_router(priority_router)
