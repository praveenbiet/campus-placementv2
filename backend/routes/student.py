from flask import Blueprint, jsonify, request
from middleware import token_required
import sqlite3
import json
from datetime import datetime

student_bp = Blueprint('student', __name__)

def get_db_connection():
    conn = sqlite3.connect('campus_placement.db')
    conn.row_factory = sqlite3.Row
    return conn

@student_bp.route('/profile', methods=['GET', 'OPTIONS'])
@token_required
def get_profile(current_user):
    if current_user['user_type'] != 'student':
        return jsonify({'message': 'Unauthorized access'}), 403

    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM students WHERE id = ?', (current_user['user_id'],))
    student = cursor.fetchone()
    conn.close()
    
    if student:
        student_dict = dict(student)
        del student_dict['password']  # Remove sensitive information
        student_dict['skills'] = json.loads(student_dict['skills'])
        return jsonify(student_dict), 200
    else:
        return jsonify({'message': 'Student not found'}), 404

@student_bp.route('/drives', methods=['GET', 'OPTIONS'])
@token_required
def get_drives(current_user):
    if current_user['user_type'] != 'student':
        return jsonify({'message': 'Unauthorized access'}), 403

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get all drives
    cursor.execute('''
        SELECT d.*, c.name as company_name 
        FROM drives d
        JOIN companies c ON d.company_id = c.id
        WHERE d.drive_date >= date('now')
        ORDER BY d.drive_date ASC
    ''')
    drives = cursor.fetchall()
    
    # Get student's applications
    cursor.execute('''
        SELECT drive_id 
        FROM applications 
        WHERE student_id = ?
    ''', (current_user['user_id'],))
    applied_drive_ids = [row['drive_id'] for row in cursor.fetchall()]
    
    conn.close()
    
    drives_list = []
    for drive in drives:
        drive_dict = dict(drive)
        drive_dict['status'] = 'upcoming' if datetime.strptime(drive_dict['drive_date'], '%Y-%m-%d').date() > datetime.now().date() else 'ongoing'
        drive_dict['applied'] = drive_dict['id'] in applied_drive_ids
        drives_list.append(drive_dict)
    
    return jsonify(drives_list), 200

@student_bp.route('/drives/<int:drive_id>/apply', methods=['POST', 'OPTIONS'])
@token_required
def apply_to_drive(current_user, drive_id):
    if current_user['user_type'] != 'student':
        return jsonify({'message': 'Unauthorized access'}), 403

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if drive exists
    cursor.execute('SELECT * FROM drives WHERE id = ?', (drive_id,))
    drive = cursor.fetchone()
    if not drive:
        conn.close()
        return jsonify({'message': 'Drive not found'}), 404
    
    # Check if already applied
    cursor.execute('''
        SELECT * FROM applications 
        WHERE student_id = ? AND drive_id = ?
    ''', (current_user['user_id'], drive_id))
    if cursor.fetchone():
        conn.close()
        return jsonify({'message': 'Already applied to this drive'}), 400
    
    # Create application
    cursor.execute('''
        INSERT INTO applications (student_id, drive_id, application_date, status)
        VALUES (?, ?, date('now'), 'pending')
    ''', (current_user['user_id'], drive_id))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Successfully applied to drive'}), 201

@student_bp.route('/applications', methods=['GET', 'OPTIONS'])
@token_required
def get_applications(current_user):
    if current_user['user_type'] != 'student':
        return jsonify({'message': 'Unauthorized access'}), 403

    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT a.*, d.job_title, c.name as company_name
        FROM applications a
        JOIN drives d ON a.drive_id = d.id
        JOIN companies c ON d.company_id = c.id
        WHERE a.student_id = ?
        ORDER BY a.application_date DESC
    ''', (current_user['user_id'],))
    
    applications = cursor.fetchall()
    conn.close()
    
    applications_list = []
    for app in applications:
        app_dict = dict(app)
        applications_list.append(app_dict)
    
    return jsonify(applications_list), 200 