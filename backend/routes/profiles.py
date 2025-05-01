from flask import Blueprint, request, jsonify
import jwt
from functools import wraps
import sqlite3
import json

profiles_bp = Blueprint('profiles', __name__)

# Secret key for JWT (should match the one in auth.py)
SECRET_KEY = 'your-secret-key-here'

def get_db_connection():
    conn = sqlite3.connect('campus_placement.db')
    conn.row_factory = sqlite3.Row
    return conn

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = {
                'id': data['user_id'],
                'type': data['user_type']
            }
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

@profiles_bp.route('/student/profile', methods=['GET'])
@token_required
def get_student_profile(current_user):
    if current_user['type'] != 'student':
        return jsonify({'message': 'Unauthorized access'}), 403
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM students WHERE id = ?', (current_user['id'],))
    student = cursor.fetchone()
    conn.close()
    
    if student:
        student_dict = dict(student)
        del student_dict['password']
        student_dict['skills'] = json.loads(student_dict['skills'])
        return jsonify(student_dict), 200
    else:
        return jsonify({'message': 'Student not found'}), 404

@profiles_bp.route('/admin/profile', methods=['GET'])
@token_required
def get_admin_profile(current_user):
    if current_user['type'] != 'admin':
        return jsonify({'message': 'Unauthorized access'}), 403
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM admins WHERE id = ?', (current_user['id'],))
    admin = cursor.fetchone()
    conn.close()
    
    if admin:
        admin_dict = dict(admin)
        del admin_dict['password']
        return jsonify(admin_dict), 200
    else:
        return jsonify({'message': 'Admin not found'}), 404 