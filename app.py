from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)

# Replace <YOUR_CONNECTION_STRING> with your actual MongoDB Atlas connection string
app.config['MONGO_URI'] = "mongodb+srv://system:admin@cluster0.3kzqwqf.mongodb.net/registrationsdata?retryWrites=true&w=majority"
mongo = PyMongo(app)

# API endpoint for registration
@app.route('/register', methods=['POST'])
def register():
    data = request.form

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Insert registration data into MongoDB
    users_collection = mongo.db.users
    user_id = users_collection.insert_one({
        'username': username,
        'email': email,
        'password': password
    }).inserted_id

    response = {
        'status': 'success',
        'message': 'Registration successful!',
        'user_id': str(user_id)
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
