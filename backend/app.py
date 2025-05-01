from flask import Flask
from flask_cors import CORS
from models import db, Student, Drive, Notification
from routes import student_bp, admin_bp
import os

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///campus_placement.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Register blueprints
app.register_blueprint(student_bp, url_prefix='/api')
app.register_blueprint(admin_bp, url_prefix='/api/admin')

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True) 