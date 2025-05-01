from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    roll_number = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    year_of_graduation = db.Column(db.Integer, nullable=False)
    cgpa = db.Column(db.Float, nullable=False)
    resume_url = db.Column(db.String(255))
    skills = db.Column(db.Text, default='[]')  # Store as JSON string
    projects = db.Column(db.Text)
    internships = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def get_skills(self):
        return json.loads(self.skills)

    def has_skills(self, required_skills):
        student_skills = set(self.get_skills())
        return all(skill.lower() in student_skills for skill in required_skills)

    def to_dict(self):
        return {
            'id': self.id,
            'roll_number': self.roll_number,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'department': self.department,
            'year_of_graduation': self.year_of_graduation,
            'cgpa': self.cgpa,
            'resume_url': self.resume_url,
            'skills': self.get_skills(),
            'projects': self.projects,
            'internships': self.internships,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Drive(db.Model):
    __tablename__ = 'drives'
    
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    eligibility_criteria = db.Column(db.Text, nullable=False)
    required_skills = db.Column(db.Text, default='[]')  # Store as JSON string
    package_details = db.Column(db.Text, nullable=False)
    drive_date = db.Column(db.DateTime, nullable=False)
    registration_deadline = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='upcoming')  # upcoming, ongoing, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_required_skills(self):
        return json.loads(self.required_skills)
    
    def to_dict(self):
        return {
            'id': self.id,
            'company_name': self.company_name,
            'job_title': self.job_title,
            'job_description': self.job_description,
            'eligibility_criteria': self.eligibility_criteria,
            'required_skills': self.get_required_skills(),
            'package_details': self.package_details,
            'drive_date': self.drive_date.isoformat(),
            'registration_deadline': self.registration_deadline.isoformat(),
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.String(50), nullable=False)  # drive, general, important
    drive_id = db.Column(db.Integer, db.ForeignKey('drives.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'message': self.message,
            'notification_type': self.notification_type,
            'drive_id': self.drive_id,
            'created_at': self.created_at.isoformat()
        } 