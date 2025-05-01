from flask import Blueprint, jsonify
from middleware import token_required
import sqlite3
import json

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