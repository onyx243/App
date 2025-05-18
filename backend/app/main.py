from os import getenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from .routers import auth, shops, upload, dashboard
import socketio

ALLOWED_ORIGINS = getenv('ALLOWED_ORIGINS', '').split(',') if getenv('ALLOWED_ORIGINS') else []

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"] ,
    allow_headers=["*"] ,
)

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins=ALLOWED_ORIGINS)
app_socket = socketio.ASGIApp(sio, other_asgi_app=app)

app.include_router(auth.router, prefix='/api')
app.include_router(shops.router, prefix='/api')
app.include_router(upload.router, prefix='/api')
app.include_router(dashboard.router, prefix='/api')

@app.get('/api/health')
async def health():
    return {'status': 'ok'}

@sio.event
def connect(sid, environ):
    pass

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app_socket, host='0.0.0.0', port=int(getenv('PORT', '8000')))
