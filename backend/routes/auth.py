from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import jwt
import sqlite3
import json

auth_bp = Blueprint('auth', __name__)

# Secret key for JWT (in production, use a secure secret key)
SECRET_KEY = 'your-secret-key-here'

def get_db_connection():
    conn = sqlite3.connect('campus_placement.db')
    conn.row_factory = sqlite3.Row
    return conn

def generate_token(user_id, user_type):
    payload = {
        'user_id': user_id,
        'user_type': user_type,
        'exp': datetime.utcnow() + timedelta(days=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

@auth_bp.route('/student/login', methods=['POST'])
def student_login():
    data = request.get_json()
    roll_number = data.get('roll_number')
    password = data.get('password')

    print(f"Attempting login for roll number: {roll_number}")  # Debug log

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Find student with matching roll number and password
    cursor.execute('''
        SELECT * FROM students 
        WHERE roll_number = ? AND password = ?
    ''', (roll_number, password))
    
    student = cursor.fetchone()
    conn.close()
    
    if student:
        print(f"Login successful for roll number: {roll_number}")  # Debug log
        # Convert row to dict and remove password
        student_dict = dict(student)
        del student_dict['password']
        
        # Convert skills from JSON string to list
        student_dict['skills'] = json.loads(student_dict['skills'])
        
        token = generate_token(student_dict['id'], 'student')
        return jsonify({
            'token': token,
            'user': student_dict
        }), 200
    else:
        print(f"Login failed for roll number: {roll_number}")  # Debug log
        return jsonify({'message': 'Invalid credentials'}), 401

@auth_bp.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Find admin with matching username and password
    cursor.execute('''
        SELECT * FROM admins 
        WHERE username = ? AND password = ?
    ''', (username, password))
    
    admin = cursor.fetchone()
    conn.close()
    
    if admin:
        # Convert row to dict and remove password
        admin_dict = dict(admin)
        del admin_dict['password']
        
        token = generate_token(admin_dict['id'], 'admin')
        return jsonify({
            'token': token,
            'user': admin_dict
        }), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401 