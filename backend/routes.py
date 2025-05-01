from flask import Blueprint, request, jsonify
from models import db, Student, Drive, Notification
from datetime import datetime
import json

student_bp = Blueprint('student', __name__)
admin_bp = Blueprint('admin', __name__)

# Student routes
@student_bp.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([student.to_dict() for student in students])

@student_bp.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = Student.query.get_or_404(student_id)
    return jsonify(student.to_dict())

@student_bp.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['roll_number', 'first_name', 'last_name', 'email', 'phone', 
                      'department', 'year_of_graduation', 'cgpa']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Create new student
    student = Student(
        roll_number=data['roll_number'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        phone=data['phone'],
        department=data['department'],
        year_of_graduation=data['year_of_graduation'],
        cgpa=data['cgpa'],
        resume_url=data.get('resume_url'),
        skills=data.get('skills'),
        projects=data.get('projects'),
        internships=data.get('internships')
    )
    
    db.session.add(student)
    db.session.commit()
    
    return jsonify(student.to_dict()), 201

@student_bp.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    student = Student.query.get_or_404(student_id)
    data = request.get_json()
    
    # Update fields if provided
    fields = ['roll_number', 'first_name', 'last_name', 'email', 'phone', 
             'department', 'year_of_graduation', 'cgpa', 'resume_url', 
             'skills', 'projects', 'internships']
    
    for field in fields:
        if field in data:
            setattr(student, field, data[field])
    
    db.session.commit()
    return jsonify(student.to_dict())

@student_bp.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return '', 204

# Admin routes for drives
@admin_bp.route('/drives', methods=['GET'])
def get_drives():
    drives = Drive.query.all()
    return jsonify([drive.to_dict() for drive in drives])

@admin_bp.route('/drives/<int:drive_id>', methods=['GET'])
def get_drive(drive_id):
    drive = Drive.query.get_or_404(drive_id)
    return jsonify(drive.to_dict())

@admin_bp.route('/drives', methods=['POST'])
def create_drive():
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['company_name', 'job_title', 'job_description', 
                      'eligibility_criteria', 'package_details', 
                      'drive_date', 'registration_deadline']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Create new drive
    drive = Drive(
        company_name=data['company_name'],
        job_title=data['job_title'],
        job_description=data['job_description'],
        eligibility_criteria=data['eligibility_criteria'],
        required_skills=json.dumps(data.get('required_skills', [])),
        package_details=data['package_details'],
        drive_date=datetime.fromisoformat(data['drive_date']),
        registration_deadline=datetime.fromisoformat(data['registration_deadline']),
        status=data.get('status', 'upcoming')
    )
    
    db.session.add(drive)
    db.session.commit()
    
    return jsonify(drive.to_dict()), 201

@admin_bp.route('/drives/<int:drive_id>', methods=['PUT'])
def update_drive(drive_id):
    drive = Drive.query.get_or_404(drive_id)
    data = request.get_json()
    
    # Update fields if provided
    fields = ['company_name', 'job_title', 'job_description', 
             'eligibility_criteria', 'package_details', 
             'drive_date', 'registration_deadline', 'status']
    
    for field in fields:
        if field in data:
            if field in ['drive_date', 'registration_deadline']:
                setattr(drive, field, datetime.fromisoformat(data[field]))
            else:
                setattr(drive, field, data[field])
    
    if 'required_skills' in data:
        drive.required_skills = json.dumps(data['required_skills'])
    
    db.session.commit()
    return jsonify(drive.to_dict())

@admin_bp.route('/drives/<int:drive_id>', methods=['DELETE'])
def delete_drive(drive_id):
    drive = Drive.query.get_or_404(drive_id)
    db.session.delete(drive)
    db.session.commit()
    return '', 204

# Admin routes for notifications
@admin_bp.route('/notifications', methods=['GET'])
def get_notifications():
    notifications = Notification.query.all()
    return jsonify([notification.to_dict() for notification in notifications])

@admin_bp.route('/notifications', methods=['POST'])
def create_notification():
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['title', 'message', 'notification_type']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Create new notification
    notification = Notification(
        title=data['title'],
        message=data['message'],
        notification_type=data['notification_type'],
        drive_id=data.get('drive_id')
    )
    
    db.session.add(notification)
    db.session.commit()
    
    return jsonify(notification.to_dict()), 201

@admin_bp.route('/notifications/<int:notification_id>', methods=['DELETE'])
def delete_notification(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    db.session.delete(notification)
    db.session.commit()
    return '', 204

# Skill-based notification routes
@admin_bp.route('/drives/<int:drive_id>/notify-matching-students', methods=['POST'])
def notify_matching_students(drive_id):
    drive = Drive.query.get_or_404(drive_id)
    required_skills = drive.get_required_skills()
    
    # Find students with matching skills
    matching_students = Student.query.filter(
        Student.skills.like(f'%{required_skills[0].lower()}%')
    ).all()
    
    matching_students = [student for student in matching_students 
                        if student.has_skills(required_skills)]
    
    if not matching_students:
        return jsonify({'message': 'No matching students found'}), 404
    
    # Create notification for each matching student
    notifications = []
    for student in matching_students:
        notification = Notification(
            title=f"New Drive Alert: {drive.company_name}",
            message=f"New drive matching your skills: {drive.job_title}. Required skills: {', '.join(required_skills)}",
            notification_type='drive',
            drive_id=drive.id
        )
        db.session.add(notification)
        notifications.append(notification)
    
    db.session.commit()
    
    return jsonify({
        'message': f'Notifications sent to {len(matching_students)} students',
        'notifications': [n.to_dict() for n in notifications]
    }), 201

@admin_bp.route('/students/matching-skills', methods=['POST'])
def get_students_with_skills():
    data = request.get_json()
    required_skills = data.get('skills', [])
    
    if not required_skills:
        return jsonify({'error': 'No skills provided'}), 400
    
    # Find students with matching skills
    matching_students = Student.query.filter(
        Student.skills.like(f'%{required_skills[0].lower()}%')
    ).all()
    
    matching_students = [student for student in matching_students 
                        if student.has_skills(required_skills)]
    
    return jsonify({
        'count': len(matching_students),
        'students': [student.to_dict() for student in matching_students]
    }) 