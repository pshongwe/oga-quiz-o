from flask import Flask, jsonify, abort, request, session
from flask_cors import CORS, cross_origin
from flask_restx import Api
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from libs.db import DB
import os
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
app.secret_key = os.environ.get('MY_SECRET')
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*", "supports_credentials": True}})
api = Api(app, version='1.0', title='Oga Quiz O API', description='Oga Quiz O API Documentation', doc='/swagger/')

auth = Auth()
db = DB()

# @auth.verify_password
# def verify_password(email, password):
#     user = db.find_user_by(email=email, password=password)
#     if user and check_password_hash(user['hashed_password'], password):
#         return user['_id']  # Assuming you store `_id` as the user identifier

@app.errorhandler(404)
def not_found(error) -> str:
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(401)
def unauthorized(error) -> str:
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden(error) -> str:
    return jsonify({"error": "Forbidden"}), 403

@app.route('/api/v1/auth_session/signup', methods=['POST'])
def signup():
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or not password:
        abort(400, description="Missing email or password")

    user = auth.register_user(email, password)
    if not user:
        abort(400, description="User already exists")

    return jsonify({"email": email, "message": "User created successfully"}), 201

@cross_origin(headers=['Content-Type'])
def options(self):
    return jsonify(success=True)

# @app.before_request
# def require_login():
#     exclude_paths = ['/api/v1/auth_session/signup', '/api/v1/auth_session/login']
    
#     if not any(request.path.startswith(path) for path in exclude_paths) and 'user_id' not in session:
#         abort(401, description="Unauthorized")

@app.route('/api/v1/auth_session/login', methods=['POST'])
@cross_origin(headers=['Content-Type'])
# @auth.login_required
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or not password:
        abort(400, description="Missing email or password")
    
    user = db.find_user_by(email=email, password=password)
    if not user or not check_password_hash(user['hashed_password'], password):
        abort(401, description="Invalid credentials")

    # Create a session and set a cookie
    session['user_id'] = str(user['_id'])
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie('session_id', str(session.sid), httponly=True, secure=False)  # Adjust `secure` based on your environment
    return response

@app.route('/api/v1/auth_session/logout', methods=['DELETE'])
@cross_origin(headers=['Content-Type'])
# @auth.login_required
def logout():
    session.pop('user_id', None)
    response = jsonify({"message": "Logged out successfully"})
    response.delete_cookie('session_id')
    return response, 204


# New endpoints for the quiz functionality
@app.route('/api/v1/quizzes', methods=['POST'])
@cross_origin(headers=['Content-Type'])
def create_quiz():
    if not request.json or 'title' not in request.json:
        abort(400, description="Missing title")
    quiz = {
        'title': request.json['title'],
        'options': request.json['options'],
        'correctAnswer': request.json['correctAnswer']
    }
    result = db._db.quizzes.insert_one(quiz)
    return jsonify({"message": "Quiz created successfully", "id": str(result.inserted_id)}), 201

@app.route('/api/v1/quizzes/<quiz_id>', methods=['GET'])
@cross_origin(headers=['Content-Type'])
def get_quiz(quiz_id):
    try:
        quiz = db._db.quizzes.find_one({'_id': ObjectId(quiz_id)})
        if quiz:
            quiz['_id'] = str(quiz['_id'])
            return jsonify(quiz)
        abort(404, description="Quiz not found")
    except Exception:
        abort(400, description="Invalid quiz ID")

@app.route('/api/v1/quizzes', methods=['GET'])
@cross_origin(headers=['Content-Type'])
def list_quizzes():
    quizzes = list(db._db.quizzes.find({}, {'title': 1}))
    for quiz in quizzes:
        quiz['_id'] = str(quiz['_id'])
    return jsonify(quizzes)

@app.route('/api/v1/quizzes/<quiz_id>/question', methods=['POST'])
def add_question(quiz_id):
    if not request.json or 'question' not in request.json or 'answer' not in request.json:
        abort(400, description="Missing question or answer")
    question = {
        'question': request.json['question'],
        'correctAnswer': request.json['correctAnswer']
    }
    result = db._db.quizzes.update_one(
        {'_id': ObjectId(quiz_id)},
        {'$push': {'questions': question}}
    )
    if result.modified_count:
        return jsonify({"message": "Question added successfully"}), 201
    abort(404, description="Quiz not found")

@app.route('/api/v1/question/<quiz_id>/<int:question_index>', methods=['GET'])
def get_question(quiz_id, question_index):
    quiz = db._db.quizzes.find_one({'_id': ObjectId(quiz_id)})
    if quiz and 0 <= question_index < len(quiz.get('questions', [])):
        return jsonify(quiz['questions'][question_index])
    abort(404, description="Question not found")

@app.route('/api/v1/quizzes/<quiz_id>/start', methods=['POST'])
def start_quiz_session(quiz_id):
    quiz = db._db.quizzes.find_one({'_id': ObjectId(quiz_id)})
    if not quiz:
        abort(404, description="Quiz not found")
    session = {
        'quiz_id': ObjectId(quiz_id),
        'current_question': 0,
        'score': 0
    }
    result = db._db.sessions.insert_one(session)
    return jsonify({"session_id": str(result.inserted_id), "message": "Quiz session started"})

@app.route('/api/v1/quizzes/session/<session_id>', methods=['PUT'])
def submit_answer(session_id):
    if not request.json or 'answer' not in request.json:
        abort(400, description="Missing answer")
    session_info = db._db.sessions.find_one({'_id': ObjectId(session_id)})
    quiz_info =  db._db.quizzes.find_one({'_id': ObjectId(session_info['quiz_id'])})

    correct = quiz_info['correctAnswer'] == request.json['answer']

    if correct:
        db._db.sessions.update_one(
            {'_id': ObjectId(session_id)},
            {'$inc': {'score': 1, 'current_question': 1}}
        )
    else:
        db._db.sessions.update_one(
            {'_id': ObjectId(session_id)},
            {'$inc': {'current_question': 1}}
        )
    return jsonify({"correct": correct, "message": "Answer submitted successfully"})

@app.route('/api/v1/quizzes/session/<session_id>', methods=['GET'])
def get_next_question(session_id):
    session = db._db.sessions.find_one({'_id': ObjectId(session_id)})
    if not session:
        abort(404, description="Session not found")
    quiz = db._db.quizzes.find_one({'_id': session['quiz_id']})

    current_question = session['current_question']
    if current_question >= len(quiz['options']):
        return jsonify({"message": "Quiz completed"})

    return jsonify({"question": quiz['questions'][current_question]['question']})

@app.route('/api/v1/score/<session_id>', methods=['GET'])
@cross_origin(headers=['Content-Type'])
def get_user_score(session_id):
    session = db._db.sessions.find_one({'_id': ObjectId(session_id)})
    if not session:
        abort(404, description="Session not found")
    return jsonify({"sessionid": session_id, "score": session['score']})

@app.route('/api/v1/leaderboard/<quiz_id>', methods=['GET'])
@cross_origin(headers=['Content-Type'])
def get_leaderboard(quiz_id):
    if not quiz_id:
        return jsonify({ "message": 'No existing quiz id on leaderboard.'}), 400
    leaderboard = list(db._db.sessions.find(
        {'quiz_id': ObjectId(quiz_id)},
        {'_id': 0, 'score': 1}
    ).sort('score', -1).limit(10))
    return jsonify({"quiz_id": quiz_id, "leaderboard": leaderboard})

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
    return response

@app.after_request
def add_security_headers(response):
    response.headers['Referrer-Policy'] = 'no-referrer'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
    return response

@app.after_request
def enforce_https_in_redirects(response):
    # Check if the response is a redirect and the scheme is HTTP
    if response.status_code in (301, 302, 303, 307, 308) and request.url.startswith('http://'):
        if not request.url.startswith('http://localhost'):
            # Replace 'http://' with 'https://' in the Location header
            response.headers['Location'] = response.headers['Location'].replace('http://', 'https://', 1)
    return response

if __name__ == "__main__":
    host = os.getenv("API_HOST", "0.0.0.0")
    port = os.getenv("API_PORT", "5000")
    app.run(debug=True, host=host, port=port)