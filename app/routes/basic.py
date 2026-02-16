from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "OK"}

@router.get("/time")
def current_time():
    return {"server_time": datetime.now()}
