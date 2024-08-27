from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin
from flask_restx import Api
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from libs.db import DB
import os

app = Flask(__name__)
app.secret_key = os.environ.get('MY_SECRET') # Needed for Flask-Login sessions
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
CORS(app, resources={r"/api/v1/*": {"origins": "*", "supports_credentials": True}})
api = Api(app, version='1.0', title='Oga Quiz O API', description='Oga Quiz O API Documentation', doc='/swagger/')
login_manager = LoginManager()
login_manager.init_app(app)
auth = Auth()
db = DB()

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

@login_manager.user_loader
def load_user(user_id):
    user = db.find_user_by(_id=ObjectId(user_id))
    if user:
        return User(str(user['_id']))
    return None

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

@app.route('/api/v1/auth_session/login', methods=['POST'])
@cross_origin(headers=['Content-Type'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or not password:
        abort(400, description="Missing email or password")
    try:
        user = db.find_user_by(email=email)
        if not user or not check_password_hash(user['hashed_password'], password):
            abort(401, description="Invalid credentials")

        user_obj = User(str(user['_id']))
        login_user(user_obj)

        # Create a session and set a cookie
        session_id = auth.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', str(session_id), httponly=True, secure=False)  # Adjust `secure` based on your environment
        return response

    except ValueError:
        abort(401, description="Invalid credentials")

@app.route('/api/v1/auth_session/logout', methods=['DELETE'])
@cross_origin(headers=['Content-Type'])
def logout():
    user_id = str(current_user.id)  # Ensure this is a string
    auth.destroy_session(user_id)
    return jsonify({}), 204

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
        'answer': request.json['answer']
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
    session = db._db.sessions.find_one({'_id': ObjectId(session_id)})
    if not session:
        abort(404, description="Session not found")
    quiz = db._db.quizzes.find_one({'_id': session['quiz_id']})
    current_question = session['current_question']

    if current_question >= len(quiz['questions']):
        return jsonify({"message": "Quiz completed"}), 400

    correct = quiz['questions'][current_question]['answer'].lower() == request.json['answer'].lower()

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
    if current_question >= len(quiz['questions']):
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