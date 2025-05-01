from app import app
from init_db import init_db

if __name__ == '__main__':
    # Initialize the database with dummy data
    init_db()
    
    # Start the Flask server
    app.run(debug=True) 