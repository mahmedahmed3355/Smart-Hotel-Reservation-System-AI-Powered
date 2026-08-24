# app/main.py
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import router as booking_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI(title="Smart Hotel Reservation System")
logger.info("Application initialized")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

app.include_router(booking_router)

@app.get("/")
def root():
    return {"status": "ok", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "healthy"}
