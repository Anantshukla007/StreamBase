# app/main.py
from fastapi import FastAPI
from app.database import init_db
from app.routes import auth, users, videos, comments

app = FastAPI(title="YouTube MVP", version="1.0")

@app.on_event("startup")
async def startup():
    await init_db()

# Register routes
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(videos.router)
app.include_router(comments.router)
