from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class DepartmentCategory(str, Enum):
    GOVERNMENT = "government"
    HEALTH = "health"
    EDUCATION = "education"
    TRANSPORT = "transport"
    FINANCE = "finance"
    SOCIAL = "social"


class ServiceCategory(str, Enum):
    DOCUMENTATION = "documentation"
    LICENSING = "licensing"
    REGISTRATION = "registration"
    CERTIFICATION = "certification"
    INFORMATION = "information"


class Department(BaseModel):
    id: int
    name: str
    category: DepartmentCategory
    description: str
    head: str
    email: EmailStr
    phone: str
    address: str
    established: Optional[int] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Department of Health",
                "category": "health",
                "description": "Responsible for public health services",
                "head": "Dr. Sarah Johnson",
                "email": "health@gov.example",
                "phone": "+1-555-0100",
                "address": "123 Health St, Capital City",
                "established": 1950
            }
        }


class Service(BaseModel):
    id: int
    name: str
    category: ServiceCategory
    description: str
    department_id: int
    processing_time: str
    fee: Optional[float] = 0.0
    is_online: bool = True
    requirements: List[str] = []
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Passport Application",
                "category": "documentation",
                "description": "Apply for a new passport",
                "department_id": 1,
                "processing_time": "15-20 business days",
                "fee": 150.0,
                "is_online": True,
                "requirements": ["Birth certificate", "ID proof", "Address proof"]
            }
        }


class ContactForm(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, pattern=r"^\+?[\d\s\-\(\)]+$")
    subject: str = Field(..., min_length=5, max_length=200)
    message: str = Field(..., min_length=10, max_length=2000)
    department_id: Optional[int] = None
    
    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()
    
    @validator('message')
    def message_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Message cannot be empty')
        return v.strip()
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john@example.com",
                "phone": "+1-555-0123",
                "subject": "Inquiry about passport services",
                "message": "I would like to know more about the passport application process.",
                "department_id": 1
            }
        }


class ContactSubmission(ContactForm):
    id: int
    submitted_at: datetime
    status: str = "pending"


class DepartmentListResponse(BaseModel):
    total: int
    departments: List[Department]


class ServiceListResponse(BaseModel):
    total: int
    services: List[Service]
    
    
class ContactResponse(BaseModel):
    success: bool
    message: str
    submission_id: Optional[int] = None
