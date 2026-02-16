from typing import List, Optional, Dict
from datetime import datetime
from app.models import Department, Service, ContactSubmission, DepartmentCategory, ServiceCategory


class MockDatabase:
    """Mock database for demonstration purposes"""
    
    def __init__(self):
        self.departments: List[Department] = self._init_departments()
        self.services: List[Service] = self._init_services()
        self.contact_submissions: List[ContactSubmission] = []
        self._submission_counter = 1
    
    def _init_departments(self) -> List[Department]:
        return [
            Department(
                id=1,
                name="Ministry of Home Affairs",
                category=DepartmentCategory.GOVERNMENT,
                description="Responsible for internal security, disaster management, and citizenship services",
                head="Hon. Rajesh Kumar",
                email="home@gov.example",
                phone="+91-11-2309-2001",
                address="North Block, Central Secretariat, New Delhi - 110001",
                established=1947
            ),
            Department(
                id=2,
                name="Department of Health Services",
                category=DepartmentCategory.HEALTH,
                description="Provides healthcare services, medical facilities, and public health programs",
                head="Dr. Priya Sharma",
                email="health@gov.example",
                phone="+91-11-2306-1863",
                address="Nirman Bhawan, Maulana Azad Road, New Delhi - 110011",
                established=1950
            ),
            Department(
                id=3,
                name="Ministry of Education",
                category=DepartmentCategory.EDUCATION,
                description="Oversees educational policies, institutions, and academic standards",
                head="Prof. Anita Desai",
                email="education@gov.example",
                phone="+91-11-2338-6355",
                address="Shastri Bhawan, Dr. Rajendra Prasad Road, New Delhi - 110001",
                established=1947
            ),
            Department(
                id=4,
                name="Transport Authority",
                category=DepartmentCategory.TRANSPORT,
                description="Manages transportation infrastructure, licensing, and traffic regulations",
                head="Mr. Vikram Singh",
                email="transport@gov.example",
                phone="+91-11-2371-8800",
                address="Transport Bhawan, 1 Parliament Street, New Delhi - 110001",
                established=1988
            ),
            Department(
                id=5,
                name="Department of Revenue",
                category=DepartmentCategory.FINANCE,
                description="Handles taxation, revenue collection, and financial administration",
                head="Ms. Kavita Reddy",
                email="revenue@gov.example",
                phone="+91-11-2309-4500",
                address="North Block, Central Secretariat, New Delhi - 110001",
                established=1947
            ),
            Department(
                id=6,
                name="Social Welfare Department",
                category=DepartmentCategory.SOCIAL,
                description="Provides social security, welfare schemes, and community development programs",
                head="Mrs. Meena Patel",
                email="welfare@gov.example",
                phone="+91-11-2338-2054",
                address="Shastri Bhawan, Dr. Rajendra Prasad Road, New Delhi - 110001",
                established=1985
            )
        ]
    
    def _init_services(self) -> List[Service]:
        return [
            Service(
                id=1,
                name="Passport Application",
                category=ServiceCategory.DOCUMENTATION,
                description="Apply for a new passport or renew existing passport",
                department_id=1,
                processing_time="15-20 business days",
                fee=1500.0,
                is_online=True,
                requirements=["Birth certificate", "Address proof", "ID proof", "Photographs"]
            ),
            Service(
                id=2,
                name="Aadhaar Card Enrollment",
                category=ServiceCategory.REGISTRATION,
                description="Register for Aadhaar unique identification number",
                department_id=1,
                processing_time="30-45 days",
                fee=0.0,
                is_online=True,
                requirements=["Proof of identity", "Proof of address", "Date of birth proof"]
            ),
            Service(
                id=3,
                name="Voter ID Registration",
                category=ServiceCategory.REGISTRATION,
                description="Register as a voter and obtain voter ID card",
                department_id=1,
                processing_time="30 days",
                fee=0.0,
                is_online=True,
                requirements=["Age proof (18+)", "Address proof", "Photograph"]
            ),
            Service(
                id=4,
                name="Medical Certificate",
                category=ServiceCategory.CERTIFICATION,
                description="Obtain medical fitness certificate for various purposes",
                department_id=2,
                processing_time="1-2 days",
                fee=200.0,
                is_online=False,
                requirements=["ID proof", "Medical examination"]
            ),
            Service(
                id=5,
                name="Health Insurance Registration",
                category=ServiceCategory.REGISTRATION,
                description="Enroll in government health insurance schemes",
                department_id=2,
                processing_time="7-10 days",
                fee=0.0,
                is_online=True,
                requirements=["Income certificate", "Family details", "Bank account"]
            ),
            Service(
                id=6,
                name="Birth Certificate",
                category=ServiceCategory.CERTIFICATION,
                description="Register birth and obtain birth certificate",
                department_id=2,
                processing_time="3-5 days",
                fee=50.0,
                is_online=True,
                requirements=["Hospital records", "Parent's ID proof"]
            ),
            Service(
                id=7,
                name="School Admission",
                category=ServiceCategory.REGISTRATION,
                description="Apply for admission to government schools",
                department_id=3,
                processing_time="Varies by session",
                fee=0.0,
                is_online=True,
                requirements=["Birth certificate", "Address proof", "Previous school records"]
            ),
            Service(
                id=8,
                name="Scholarship Application",
                category=ServiceCategory.DOCUMENTATION,
                description="Apply for government scholarships and financial aid",
                department_id=3,
                processing_time="60-90 days",
                fee=0.0,
                is_online=True,
                requirements=["Academic records", "Income certificate", "Bank details"]
            ),
            Service(
                id=9,
                name="Driving License",
                category=ServiceCategory.LICENSING,
                description="Apply for or renew driving license",
                department_id=4,
                processing_time="30 days",
                fee=1000.0,
                is_online=True,
                requirements=["Age proof (18+)", "Address proof", "Medical certificate", "Driving test"]
            ),
            Service(
                id=10,
                name="Vehicle Registration",
                category=ServiceCategory.REGISTRATION,
                description="Register new vehicle and obtain registration certificate",
                department_id=4,
                processing_time="7-10 days",
                fee=2500.0,
                is_online=True,
                requirements=["Purchase invoice", "Insurance", "Pollution certificate", "ID proof"]
            ),
            Service(
                id=11,
                name="Tax Filing",
                category=ServiceCategory.DOCUMENTATION,
                description="File income tax returns online",
                department_id=5,
                processing_time="Immediate",
                fee=0.0,
                is_online=True,
                requirements=["PAN card", "Income statements", "Investment proofs"]
            ),
            Service(
                id=12,
                name="PAN Card Application",
                category=ServiceCategory.DOCUMENTATION,
                description="Apply for Permanent Account Number card",
                department_id=5,
                processing_time="15-20 days",
                fee=110.0,
                is_online=True,
                requirements=["ID proof", "Address proof", "Date of birth proof", "Photograph"]
            ),
            Service(
                id=13,
                name="Pension Scheme Enrollment",
                category=ServiceCategory.REGISTRATION,
                description="Enroll in government pension schemes",
                department_id=6,
                processing_time="30 days",
                fee=0.0,
                is_online=True,
                requirements=["Age proof (60+)", "Bank account", "Address proof"]
            ),
            Service(
                id=14,
                name="Disability Certificate",
                category=ServiceCategory.CERTIFICATION,
                description="Obtain disability certificate for benefits and reservations",
                department_id=6,
                processing_time="15 days",
                fee=0.0,
                is_online=False,
                requirements=["Medical examination", "ID proof", "Photographs"]
            )
        ]
    
    def get_all_departments(self) -> List[Department]:
        return self.departments
    
    def get_department_by_id(self, dept_id: int) -> Optional[Department]:
        return next((d for d in self.departments if d.id == dept_id), None)
    
    def get_all_services(self, category: Optional[str] = None, department_id: Optional[int] = None) -> List[Service]:
        services = self.services
        
        if category:
            services = [s for s in services if s.category == category]
        
        if department_id:
            services = [s for s in services if s.department_id == department_id]
        
        return services
    
    def get_service_by_id(self, service_id: int) -> Optional[Service]:
        return next((s for s in self.services if s.id == service_id), None)
    
    def add_contact_submission(self, submission: ContactSubmission) -> ContactSubmission:
        submission.id = self._submission_counter
        submission.submitted_at = datetime.now()
        self._submission_counter += 1
        self.contact_submissions.append(submission)
        return submission


# Global database instance
db = MockDatabase()
