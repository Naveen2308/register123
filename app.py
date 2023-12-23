from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from pymongo import MongoClient
import hashlib

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Your MongoDB setup goes here
mongo_uri = "mongodb+srv://system:admin@cluster0.3kzqwqf.mongodb.net/registrationsdata?retryWrites=true&w=majority"
client = MongoClient(mongo_uri)
db = client["registrationsdata"]
users_collection = db["users"]

@app.route('/register', methods=['POST'])
def register():
    try:
        # Retrieve user data from the request
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Hash the password using a secure method (e.g., bcrypt)
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Check if the username or email already exists in the database
        existing_user = users_collection.find_one({'$or': [{'username': username}, {'email': email}]})
        if existing_user:
            return jsonify({'error': 'Username or email already exists'}), 400

        # Insert the new user into the database
        user_data = {'username': username, 'email': email, 'password': hashed_password}
        result = users_collection.insert_one(user_data)

        # Return the user ID in a standardized response format
        return jsonify({'data': {'user_id': str(result.inserted_id)}}), 200

    except Exception as e:
        print(f"Error during registration: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


