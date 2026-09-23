from fastapi import FastAPI
from app.api.routes.health import router as health_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Enterprise Work Platform API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}