# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router as booking_router

app = FastAPI(title="Smart Hotel Reservation System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

app.include_router(booking_router)

@app.get("/")
def root():
    return {"status": "ok", "docs": "/docs"}
