from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from routes import auth, tasks
from config import settings
from utils import limiter

routers = [
    auth.router,
    tasks.router,
]

origins = settings.origins

app = FastAPI()
limiter.setup_limiter(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.allowed_hosts)

for router in routers:
    app.include_router(router)
