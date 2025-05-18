from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = AsyncIOMotorClient(os.getenv("MONGODB_URI"))
db = client.get_default_database()

from .auth import router as auth_router
from .shops import router as shops_router
from .uploads import router as upload_router
from .dashboard import router as dashboard_router

app.include_router(auth_router, prefix="/api/auth")
app.include_router(shops_router, prefix="/api/shops")
app.include_router(upload_router, prefix="/api/upload")
app.include_router(dashboard_router, prefix="/api/dashboard")

