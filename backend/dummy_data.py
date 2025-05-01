# Dummy data for testing
STUDENTS = [
    {
        "id": 1,
        "roll_number": "2023001",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "1234567890",
        "department": "Computer Science",
        "year_of_graduation": 2024,
        "cgpa": 8.5,
        "skills": ["Python", "JavaScript", "React", "SQL"],
        "projects": "E-commerce website, Chat application",
        "internships": "Software Developer at Tech Corp",
        "is_placed": False,
        "password": "password123"  # In production, this should be hashed
    },
    {
        "id": 2,
        "roll_number": "2023002",
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@example.com",
        "phone": "9876543210",
        "department": "Information Technology",
        "year_of_graduation": 2024,
        "cgpa": 9.0,
        "skills": ["Java", "Spring Boot", "MySQL", "AWS"],
        "projects": "Library Management System, Weather App",
        "internships": "Backend Developer at Data Systems",
        "is_placed": True,
        "password": "password123"
    },
    {
        "id": 3,
        "roll_number": "2023003",
        "first_name": "Alex",
        "last_name": "Johnson",
        "email": "alex.johnson@example.com",
        "phone": "5551234567",
        "department": "Electronics",
        "year_of_graduation": 2024,
        "cgpa": 8.2,
        "skills": ["C++", "Embedded Systems", "Python", "MATLAB"],
        "projects": "Smart Home System, IoT Device",
        "internships": "Embedded Systems Engineer at Tech Solutions",
        "is_placed": False,
        "password": "password123"
    }
]

ADMINS = [
    {
        "id": 1,
        "username": "admin",
        "password": "admin123",  # In production, this should be hashed
        "name": "Admin User",
        "email": "admin@example.com",
        "role": "super_admin"
    },
    {
        "id": 2,
        "username": "placement_officer",
        "password": "placement123",
        "name": "Placement Officer",
        "email": "placement@example.com",
        "role": "placement_officer"
    }
]

DRIVES = [
    {
        "id": 1,
        "company_name": "Tech Solutions Inc.",
        "job_title": "Software Engineer",
        "job_description": "Looking for skilled software engineers with experience in web development",
        "eligibility_criteria": "CGPA >= 7.5, 2024 batch",
        "required_skills": ["Python", "JavaScript", "React", "SQL"],
        "package_details": "12 LPA",
        "drive_date": "2024-03-15T10:00:00",
        "registration_deadline": "2024-03-10T23:59:59",
        "status": "upcoming"
    },
    {
        "id": 2,
        "company_name": "Data Systems Ltd.",
        "job_title": "Backend Developer",
        "job_description": "Seeking backend developers with experience in Java and Spring Boot",
        "eligibility_criteria": "CGPA >= 8.0, 2024 batch",
        "required_skills": ["Java", "Spring Boot", "MySQL", "AWS"],
        "package_details": "15 LPA",
        "drive_date": "2024-03-20T10:00:00",
        "registration_deadline": "2024-03-15T23:59:59",
        "status": "upcoming"
    },
    {
        "id": 3,
        "company_name": "Embedded Tech",
        "job_title": "Embedded Systems Engineer",
        "job_description": "Looking for engineers with experience in embedded systems and IoT",
        "eligibility_criteria": "CGPA >= 7.0, 2024 batch",
        "required_skills": ["C++", "Embedded Systems", "Python", "MATLAB"],
        "package_details": "10 LPA",
        "drive_date": "2024-03-25T10:00:00",
        "registration_deadline": "2024-03-20T23:59:59",
        "status": "upcoming"
    }
]

APPLICATIONS = [
    {
        "id": 1,
        "student_id": 1,
        "drive_id": 1,
        "application_date": "2024-03-01T14:30:00",
        "status": "pending"
    },
    {
        "id": 2,
        "student_id": 2,
        "drive_id": 2,
        "application_date": "2024-03-02T10:15:00",
        "status": "accepted"
    }
] 