import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import uvicorn
import socketio

from .socket import sio
from .auth import init_auth
from .routes import auth as auth_routes
from .routes import shops as shop_routes
from .routes import upload as upload_routes
from .routes import dashboard as dashboard_routes

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] ,
    allow_credentials=True,
    allow_methods=["*"] ,
    allow_headers=["*"] ,
)

init_auth(os.getenv("JWT_SECRET", "secret"))

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(auth_routes.router)
app.include_router(shop_routes.router)
app.include_router(upload_routes.router)
app.include_router(dashboard_routes.router)

@sio.event
async def connect(sid, environ):
    query = environ.get('QUERY_STRING', '')
    if 'userId=' in query:
        user_id = query.split('userId=')[1]
        await sio.save_session(sid, {'userId': user_id})
        await sio.enter_room(sid, user_id)

app = socketio.ASGIApp(sio, app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 3001)))
