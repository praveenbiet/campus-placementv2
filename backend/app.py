from flask import Flask, request, make_response
from flask_cors import CORS
from models import db, Student, Drive, Notification
from routes import student_bp, admin_bp
from routes.auth import auth_bp
import os

app = Flask(__name__)

# Configure CORS for all routes
CORS(app, 
    resources={r"/*": {
        "origins": ["http://localhost:5173"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"],
        "supports_credentials": True,
        "expose_headers": ["Content-Type", "Authorization"],
        "max_age": 3600
    }},
    supports_credentials=True
)

# Add middleware to handle OPTIONS requests
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = make_response()
        return response

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///campus_placement.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Register blueprints
app.register_blueprint(student_bp, url_prefix='/api/student')
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(auth_bp, url_prefix='/api/auth')

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True) 