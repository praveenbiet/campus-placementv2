from app import app, db
from models import Student, Drive, Notification
from datetime import datetime, timedelta
import json

def create_dummy_data():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        # Create dummy students
        students = [
            Student(
                roll_number="CS2023001",
                first_name="John",
                last_name="Doe",
                email="john.doe@example.com",
                phone="1234567890",
                department="Computer Science",
                year_of_graduation=2024,
                cgpa=8.5,
                skills=json.dumps(["python", "javascript", "react", "node.js", "sql"]),
                projects="E-commerce website, Chat application",
                internships="Summer internship at Tech Corp"
            ),
            Student(
                roll_number="CS2023002",
                first_name="Jane",
                last_name="Smith",
                email="jane.smith@example.com",
                phone="9876543210",
                department="Computer Science",
                year_of_graduation=2024,
                cgpa=9.0,
                skills=json.dumps(["java", "spring boot", "mysql", "docker"]),
                projects="Library management system, Online quiz platform",
                internships="Internship at Software Solutions"
            ),
            Student(
                roll_number="CS2023003",
                first_name="Mike",
                last_name="Johnson",
                email="mike.johnson@example.com",
                phone="5551234567",
                department="Computer Science",
                year_of_graduation=2024,
                cgpa=8.8,
                skills=json.dumps(["python", "django", "postgresql", "aws"]),
                projects="Social media platform, Weather app",
                internships="Cloud computing internship"
            ),
            Student(
                roll_number="CS2023004",
                first_name="Sarah",
                last_name="Williams",
                email="sarah.williams@example.com",
                phone="4449876543",
                department="Computer Science",
                year_of_graduation=2024,
                cgpa=9.2,
                skills=json.dumps(["javascript", "react", "node.js", "mongodb"]),
                projects="Task management app, E-learning platform",
                internships="Full-stack development internship"
            )
        ]

        # Create dummy drives
        drives = [
            Drive(
                company_name="Tech Corp",
                job_title="Full Stack Developer",
                job_description="Looking for a full stack developer with experience in modern web technologies",
                eligibility_criteria="CGPA >= 8.0, 2024 batch",
                required_skills=json.dumps(["javascript", "react", "node.js"]),
                package_details="12 LPA + Benefits",
                drive_date=datetime.now() + timedelta(days=30),
                registration_deadline=datetime.now() + timedelta(days=15),
                status="upcoming"
            ),
            Drive(
                company_name="Software Solutions",
                job_title="Backend Developer",
                job_description="Seeking backend developers with strong database and API development skills",
                eligibility_criteria="CGPA >= 7.5, 2024 batch",
                required_skills=json.dumps(["python", "django", "postgresql"]),
                package_details="10 LPA + Benefits",
                drive_date=datetime.now() + timedelta(days=45),
                registration_deadline=datetime.now() + timedelta(days=30),
                status="upcoming"
            ),
            Drive(
                company_name="Cloud Systems",
                job_title="Cloud Engineer",
                job_description="Looking for cloud engineers with experience in AWS and DevOps",
                eligibility_criteria="CGPA >= 8.0, 2024 batch",
                required_skills=json.dumps(["aws", "docker", "python"]),
                package_details="15 LPA + Benefits",
                drive_date=datetime.now() + timedelta(days=60),
                registration_deadline=datetime.now() + timedelta(days=45),
                status="upcoming"
            )
        ]

        # Add all objects to session
        for student in students:
            db.session.add(student)
        
        for drive in drives:
            db.session.add(drive)
        
        # Commit to create the records
        db.session.commit()

        # Create some notifications
        notifications = [
            Notification(
                title="New Drive Alert: Tech Corp",
                message="New drive for Full Stack Developer position. Required skills: javascript, react, node.js",
                notification_type="drive",
                drive_id=1
            ),
            Notification(
                title="Important: Resume Submission Deadline",
                message="Last date to submit resumes for upcoming drives is approaching",
                notification_type="important",
                drive_id=None
            )
        ]

        for notification in notifications:
            db.session.add(notification)
        
        db.session.commit()

        print("Dummy data created successfully!")
        print(f"Created {len(students)} students")
        print(f"Created {len(drives)} drives")
        print(f"Created {len(notifications)} notifications")

if __name__ == "__main__":
    create_dummy_data() 