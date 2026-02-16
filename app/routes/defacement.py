"""
Defacement Detection API Routes
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.services.baseline_manager import BaselineManager
from app.services.defacement_detector import DefacementDetector

router = APIRouter(prefix="/api/defacement", tags=["defacement"])

baseline_manager = BaselineManager()
detector = DefacementDetector()


class BaselineCreateRequest(BaseModel):
    url: str = "http://localhost:9000"


class DefacementCheckRequest(BaseModel):
    url: str = "http://localhost:9000"


@router.post("/baseline/create")
async def create_baseline(request: BaselineCreateRequest):
    """Create a new baseline snapshot"""
    try:
        baseline = baseline_manager.create_baseline(request.url)
        return {
            "success": True,
            "message": "Baseline created successfully",
            "baseline": {
                "created_at": baseline['created_at'],
                "zones_count": len(baseline['zones']),
                "images_count": len(baseline['images'])
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create baseline: {str(e)}")


@router.get("/baseline/status")
async def get_baseline_status():
    """Check if baseline exists"""
    exists = baseline_manager.baseline_exists()
    baseline = None
    
    if exists:
        baseline = baseline_manager.load_baseline()
    
    return {
        "exists": exists,
        "baseline": {
            "created_at": baseline['created_at'] if baseline else None,
            "zones_count": len(baseline['zones']) if baseline else 0,
            "images_count": len(baseline['images']) if baseline else 0
        } if baseline else None
    }


@router.post("/check")
async def check_defacement(request: DefacementCheckRequest):
    """Check for defacement against baseline"""
    if not baseline_manager.baseline_exists():
        raise HTTPException(status_code=404, detail="No baseline found. Create a baseline first.")
    
    baseline = baseline_manager.load_baseline()
    report = detector.check_defacement(baseline, request.url)
    
    return report


@router.get("/report")
async def get_latest_report():
    """Get the latest defacement report"""
    # For now, just check immediately
    if not baseline_manager.baseline_exists():
        raise HTTPException(status_code=404, detail="No baseline found. Create a baseline first.")
    
    baseline = baseline_manager.load_baseline()
    report = detector.check_defacement(baseline, "http://localhost:9000")
    
    return report


@router.delete("/baseline/reset")
async def reset_baseline():
    """Delete the current baseline"""
    deleted = baseline_manager.delete_baseline()
    
    if deleted:
        return {"success": True, "message": "Baseline deleted successfully"}
    else:
        return {"success": False, "message": "No baseline to delete"}
