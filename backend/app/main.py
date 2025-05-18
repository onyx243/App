import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from socketio import AsyncServer, ASGIApp
from .routes import auth, shops, upload, dashboard
from .db import db

load_dotenv()

sio = AsyncServer(async_mode='asgi', cors_allowed_origins='*')
app_fastapi = FastAPI()

app_fastapi.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app_fastapi.include_router(auth.router, prefix='/api/auth')
app_fastapi.include_router(shops.router, prefix='/api/shops')
app_fastapi.include_router(upload.router, prefix='/api/upload')
app_fastapi.include_router(dashboard.router, prefix='/api/dashboard')

app = ASGIApp(sio, other_asgi_app=app_fastapi)

@sio.event
async def connect(sid, environ, auth):
    user_id = auth.get('userId') if auth else None
    if user_id:
        await sio.enter_room(sid, user_id)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
