#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.session_exp_auth import SessionExpAuth
from api.v1.auth.session_db_auth import SessionDBAuth
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


auth = None
auth_type = getenv('AUTH_TYPE', 'auth')
if auth_type == 'auth':
    auth = Auth()
elif auth_type == 'basic_auth':
    auth = BasicAuth()
elif auth_type == 'session_auth':
    auth = SessionAuth()
elif auth_type == 'session_exp_auth':
    auth = SessionExpAuth()
elif auth_type == 'session_db_auth':
    auth = SessionDBAuth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.route('/api/v1/auth_session/login', methods=['POST'])
def login():
    """Log in a user and create a session"""
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or not password:
        abort(400, description="Missing email or password")
    user = User.search({"email": email})
    if not user or not user[0].is_valid_password(password):
        abort(401, description="Invalid credentials")
    session_id = auth.create_session(user[0].id)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie(os.getenv('SESSION_NAME'), session_id)
    return response


@app.route('/api/v1/auth_session/logout', methods=['DELETE'])
def logout():
    """Log out a user and destroy the session"""
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)


@app.before_request
def authenticate_user():
    """Authenticates a user before processing a request
    """
    if auth:
        excluded_paths = [
            '/api/v1/status/',
            '/api/v1/unauthorized/',
            '/api/v1/forbidden/',
            '/api/v1/auth_session/login/',
        ]
        if auth.require_auth(request.path, excluded_paths):
            if auth.authorization_header(request) is None and auth.session_cookie(request) is None:
                abort(401)
            request.current_user = auth.current_user(request)
            if request.current_user is None:
                abort(403)

# New endpoints for the quiz functionality

@app.route('/api/v1/quizzes', methods=['POST'])
def create_quiz():
    """Create a new quiz"""
    if not request.current_user:
        abort(401)
    if not request.json or 'title' not in request.json:
        abort(400, description="Missing title")
    # Logic to create a new quiz
    return jsonify({"message": "Quiz created successfully"}), 201


@app.route('/api/v1/quizzes/<int:quiz_id>', methods=['GET'])
def get_quiz(quiz_id):
    """Get a specific quiz"""
    if not request.current_user:
        abort(401)
    # Logic to retrieve a quiz by ID
    return jsonify({"quiz_id": quiz_id, "title": "Sample Quiz"})


@app.route('/api/v1/quizzes', methods=['GET'])
def list_quizzes():
    """List all quizzes"""
    if not request.current_user:
        abort(401)
    # Logic to list all quizzes
    return jsonify({"quizzes": [{"id": 1, "title": "Quiz 1"}, {"id": 2, "title": "Quiz 2"}]})


@app.route('/api/v1/quizzes/<int:quiz_id>/question', methods=['POST'])
def add_question(quiz_id):
    """Add a question to a quiz"""
    if not request.current_user:
        abort(401)
    if not request.json or 'question' not in request.json or 'answer' not in request.json:
        abort(400, description="Missing question or answer")
    # Logic to add a question to the quiz
    return jsonify({"message": "Question added successfully"}), 201


@app.route('/api/v1/question/<int:question_id>', methods=['GET'])
def get_question(question_id):
    """Get a specific question"""
    if not request.current_user:
        abort(401)
    # Logic to retrieve a question by ID
    return jsonify({"question_id": question_id, "question": "Sample Question", "answer": "Sample Answer"})


@app.route('/api/v1/quizzes/<int:quiz_id>/start', methods=['POST'])
def start_quiz_session(quiz_id):
    """Start a new quiz session"""
    if not request.current_user:
        abort(401)
    # Logic to start a new quiz session
    return jsonify({"session_id": 1, "quiz_id": quiz_id, "message": "Quiz session started"})


@app.route('/api/v1/quizzes/session/<int:session_id>', methods=['PUT'])
def submit_answer(session_id):
    """Submit an answer for the current question"""
    if not request.current_user:
        abort(401)
    if not request.json or 'answer' not in request.json:
        abort(400, description="Missing answer")
    # Logic to submit an answer and check if it's correct
    return jsonify({"correct": True, "message": "Answer submitted successfully"})


@app.route('/api/v1/quizzes/session/<int:session_id>', methods=['GET'])
def get_next_question(session_id):
    """Get the next question in the quiz"""
    if not request.current_user:
        abort(401)
    # Logic to get the next question in the quiz session
    return jsonify({"question_id": 2, "question": "Next Sample Question"})


@app.route('/api/v1/score/<int:user_id>/<int:quiz_id>', methods=['GET'])
def get_user_score(user_id, quiz_id):
    """Get user's score for a specific quiz"""
    if not request.current_user:
        abort(401)
    # Logic to retrieve the user's score for the given quiz
    return jsonify({"user_id": user_id, "quiz_id": quiz_id, "score": 80})


@app.route('/api/v1/leaderboard/<int:quiz_id>', methods=['GET'])
def get_leaderboard(quiz_id):
    """Get leaderboard for a specific quiz"""
    if not request.current_user:
        abort(401)
    # Logic to retrieve the leaderboard for the given quiz
    return jsonify({"quiz_id": quiz_id, "leaderboard": [
        {"user_id": 1, "score": 95},
        {"user_id": 2, "score": 88},
        {"user_id": 3, "score": 82}
    ]})


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
