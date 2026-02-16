from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from app.models import (
    Department, Service, ContactForm, ContactResponse,
    DepartmentListResponse, ServiceListResponse, ContactSubmission
)
from app.database import db
from datetime import datetime

router = APIRouter(prefix="/api", tags=["API"])


@router.get("/departments", response_model=DepartmentListResponse)
async def get_departments():
    """Get all departments"""
    departments = db.get_all_departments()
    return DepartmentListResponse(
        total=len(departments),
        departments=departments
    )


@router.get("/departments/{dept_id}", response_model=Department)
async def get_department(dept_id: int):
    """Get a specific department by ID"""
    department = db.get_department_by_id(dept_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department


@router.get("/services", response_model=ServiceListResponse)
async def get_services(
    category: Optional[str] = Query(None, description="Filter by category"),
    department_id: Optional[int] = Query(None, description="Filter by department ID"),
    online_only: Optional[bool] = Query(None, description="Show only online services")
):
    """Get all services with optional filtering"""
    services = db.get_all_services(category=category, department_id=department_id)
    
    if online_only is not None:
        services = [s for s in services if s.is_online == online_only]
    
    return ServiceListResponse(
        total=len(services),
        services=services
    )


@router.get("/services/{service_id}", response_model=Service)
async def get_service(service_id: int):
    """Get a specific service by ID"""
    service = db.get_service_by_id(service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service


@router.post("/contact", response_model=ContactResponse)
async def submit_contact_form(form: ContactForm):
    """Submit a contact form"""
    try:
        # Create submission
        submission = ContactSubmission(
            id=0,  # Will be set by database
            submitted_at=datetime.now(),
            status="pending",
            **form.dict()
        )
        
        # Save to database
        saved_submission = db.add_contact_submission(submission)
        
        return ContactResponse(
            success=True,
            message="Your message has been received. We will get back to you soon!",
            submission_id=saved_submission.id
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to submit contact form: {str(e)}"
        )


@router.get("/stats")
async def get_stats():
    """Get portal statistics"""
    return {
        "total_departments": len(db.get_all_departments()),
        "total_services": len(db.get_all_services()),
        "online_services": len([s for s in db.get_all_services() if s.is_online]),
        "total_submissions": len(db.contact_submissions),
        "last_updated": datetime.now().isoformat()
    }
