import sqlite3
from dummy_data import STUDENTS, ADMINS, DRIVES, APPLICATIONS
import json
from datetime import datetime

def init_db():
    conn = sqlite3.connect('campus_placement.db')
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        roll_number TEXT UNIQUE NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT,
        department TEXT,
        year_of_graduation INTEGER,
        cgpa REAL,
        skills TEXT,
        projects TEXT,
        internships TEXT,
        is_placed BOOLEAN DEFAULT 0,
        password TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        role TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS drives (
        id INTEGER PRIMARY KEY,
        company_name TEXT NOT NULL,
        job_title TEXT NOT NULL,
        job_description TEXT,
        eligibility_criteria TEXT,
        required_skills TEXT,
        package_details TEXT,
        drive_date TEXT NOT NULL,
        registration_deadline TEXT NOT NULL,
        status TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY,
        student_id INTEGER NOT NULL,
        drive_id INTEGER NOT NULL,
        application_date TEXT NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY (student_id) REFERENCES students (id),
        FOREIGN KEY (drive_id) REFERENCES drives (id)
    )
    ''')

    # Insert dummy data
    # Insert students
    for student in STUDENTS:
        cursor.execute('''
        INSERT OR REPLACE INTO students (
            id, roll_number, first_name, last_name, email, phone,
            department, year_of_graduation, cgpa, skills, projects,
            internships, is_placed, password
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            student['id'],
            student['roll_number'],
            student['first_name'],
            student['last_name'],
            student['email'],
            student['phone'],
            student['department'],
            student['year_of_graduation'],
            student['cgpa'],
            json.dumps(student['skills']),
            student['projects'],
            student['internships'],
            student['is_placed'],
            student['password']
        ))

    # Insert admins
    for admin in ADMINS:
        cursor.execute('''
        INSERT OR REPLACE INTO admins (
            id, username, password, name, email, role
        ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            admin['id'],
            admin['username'],
            admin['password'],
            admin['name'],
            admin['email'],
            admin['role']
        ))

    # Insert drives
    for drive in DRIVES:
        cursor.execute('''
        INSERT OR REPLACE INTO drives (
            id, company_name, job_title, job_description,
            eligibility_criteria, required_skills, package_details,
            drive_date, registration_deadline, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            drive['id'],
            drive['company_name'],
            drive['job_title'],
            drive['job_description'],
            drive['eligibility_criteria'],
            json.dumps(drive['required_skills']),
            drive['package_details'],
            drive['drive_date'],
            drive['registration_deadline'],
            drive['status']
        ))

    # Insert applications
    for application in APPLICATIONS:
        cursor.execute('''
        INSERT OR REPLACE INTO applications (
            id, student_id, drive_id, application_date, status
        ) VALUES (?, ?, ?, ?, ?)
        ''', (
            application['id'],
            application['student_id'],
            application['drive_id'],
            application['application_date'],
            application['status']
        ))

    # Commit changes and close connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully with dummy data!") 