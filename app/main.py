from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers.priority_controller import router as priority_router
from app.controllers.inventory_controller import router as inventory_router

# 1️⃣ קודם יוצרים את האפליקציה
app = FastAPI(title="ERPNext Priority Engine")

# 2️⃣ Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https://.*\.ngrok-free\.dev|http://localhost:3000|http://127\.0\.0\.1:3000",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3️⃣ Routers
app.include_router(priority_router, tags=["Priority"])
app.include_router(inventory_router, tags=["Inventory"])

# 4️⃣ Root endpoint
@app.get("/")
def root():
    return {"status": "OK"}
