from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_cors import CORS
from flask_session import Session
from werkzeug.utils import secure_filename
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import requests
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Enable CORS
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# Configure file uploads
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configure Main database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Configure Session
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SESSION_SQLALCHEMY'] = db

# Initialize Admin and Session
admin = Admin(app)
Session(app)

# Example for database
""""
# Define a User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# Add User model to Flask-Admin to view in /admin route
admin.add_view(ModelView(User, db.session))
""" 

# OAuth configuration
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    authorize_redirect_uri='http://localhost:5000/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid profile email'}
)

@app.route('/')
def index():
    return 'If you see this, Flask is running'

@app.route('/auth', methods=['POST'])
def auth():
    try:
        token = request.json.get('token')
        if not token:
            return jsonify({'error': 'Missing token'}), 400

        # Verify the token with Google
        response = requests.get(f'https://oauth2.googleapis.com/tokeninfo?id_token={token}')
        user_info = response.json()
        print(user_info)

        if 'error' in user_info:
            return jsonify({'error': 'Invalid token'}), 400

        # Process the user information as needed
        return jsonify({
            'name': user_info.get('name', 'No name found'),
            'email': user_info.get('email', 'No email found'),
            'imageUrl': user_info.get('picture', 'No picture found')
        })
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and file.filename.endswith('.pdf'):
        filename = secure_filename(file.filename)
        # Simulate sending the file to the AI API for processing, For now, we'll just return a success message with the filename
        return jsonify({'filename': filename, 'message': 'File uploaded and processed successfully'}), 200
    return jsonify({'error': 'Invalid file type'}), 400


if __name__ == '__main__':
     with app.app_context():
        db.create_all()
        app.run(debug=True)
