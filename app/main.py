from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.priority_controller import router as priority_router

app = FastAPI(title="ERPNext Priority Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(priority_router)

@app.get("/")
def root():
    return {"status": "OK"}
