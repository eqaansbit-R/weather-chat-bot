from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.chat import router as chat_router
from app.api.dashboard import router as dashboard_router
from app.api.admin import router as admin_router
from app.config import settings
from app.database import init_db

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Advanced Weather Chat Bot with AI + Dashboard + Admin",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(dashboard_router)
app.include_router(admin_router)

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/")
async def root():
    return {
        "message": "Weather Chat Bot API is running",
        "docs": "/docs"
    }
