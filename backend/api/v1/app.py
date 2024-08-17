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
from libs.db import DB
from bson.objectid import ObjectId
import os
from flask_restx import Api
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
api = Api(app, version='1.0', title='Oga Quiz O API', description='Oga Quiz O API Documentation', doc='/swagger/')

auth = Auth()
db = DB() 

@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler """
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(401)
def unauthorized(error) -> str:
    """Unauthorized handler"""
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden(error) -> str:
    """Forbidden handler"""
    return jsonify({"error": "Forbidden"}), 403

@app.route('/api/v1/auth_session/signup', methods=['POST'])
def signup():
    """Sign up a new user"""
    email = request.form.get('email')
    password = request.form.get('password')
    
    if not email or not password:
        abort(400, description="Missing email or password")
    
    # Hash the user's password before storing it
    hashed_password = generate_password_hash(password)
    
    user = db.add_user(email=email, hashed_password=hashed_password)
    if not user:
        abort(400, description="User already exists")
    
    return jsonify({"email": email, "message": "User created successfully"}), 201

@app.route('/api/v1/auth_session/login', methods=['POST'])
def login():
    """Log in a user and create a session"""
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or not password:
        abort(400, description="Missing email or password")
    try:
        user = db.find_user_by(email=email)
        if not user or not check_password_hash(user['hashed_password'], password):
            abort(401, description="Invalid credentials")
        
        # Create a session and get the session ID
        session_id = auth.create_session(str(user['_id']))
        print(session_id)
        # Use a default session name
        session_name = 'session_id'  # Default to 'session_id'
        print(session_name)
        # Create the response and set the cookie with the session ID
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie(session_name, session_id)
        return response
    except ValueError:
        abort(401, description="Invalid credentials")

@app.route('/api/v1/auth_session/logout', methods=['DELETE'])
def logout():
    """Log out a user and destroy the session"""
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)

# New endpoints for the quiz functionality

@app.route('/api/v1/quizzes', methods=['POST'])
def create_quiz():
    """Create a new quiz"""
    if not request.current_user:
        abort(401)
    if not request.json or 'title' not in request.json:
        abort(400, description="Missing title")
    quiz = {
        'title': request.json['title'],
        'questions': []
    }
    result = db._db.quizzes.insert_one(quiz)
    return jsonify({"message": "Quiz created successfully", "id": str(result.inserted_id)}), 201

@app.route('/api/v1/quizzes/<quiz_id>', methods=['GET'])
def get_quiz(quiz_id):
    """Get a specific quiz"""
    if not request.current_user:
        abort(401)
    try:
        quiz = db._db.quizzes.find_one({'_id': ObjectId(quiz_id)})
        if quiz:
            quiz['_id'] = str(quiz['_id'])
            return jsonify(quiz)
        abort(404, description="Quiz not found")
    except Exception:
        abort(400, description="Invalid quiz ID")

@app.route('/api/v1/quizzes', methods=['GET'])
def list_quizzes():
    """List all quizzes"""
    quizzes = list(db._db.quizzes.find({}, {'title': 1}))
    for quiz in quizzes:
        quiz['_id'] = str(quiz['_id'])
    return jsonify(quizzes)

@app.route('/api/v1/quizzes/<quiz_id>/question', methods=['POST'])
def add_question(quiz_id):
    """Add a question to a quiz"""
    if not request.current_user:
        abort(401)
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
    """Get a specific question"""
    if not request.current_user:
        abort(401)
    quiz = db._db.quizzes.find_one({'_id': ObjectId(quiz_id)})
    if quiz and 0 <= question_index < len(quiz.get('questions', [])):
        return jsonify(quiz['questions'][question_index])
    abort(404, description="Question not found")

@app.route('/api/v1/quizzes/<quiz_id>/start', methods=['POST'])
def start_quiz_session(quiz_id):
    """Start a new quiz session"""
    if not request.current_user:
        abort(401)
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
    """Submit an answer for the current question"""
    if not request.current_user:
        abort(401)
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
    """Get the next question in the quiz"""
    if not request.current_user:
        abort(401)
    session = db._db.sessions.find_one({'_id': ObjectId(session_id)})
    if not session:
        abort(404, description="Session not found")
    quiz = db._db.quizzes.find_one({'_id': session['quiz_id']})

    current_question = session['current_question']
    if current_question >= len(quiz['questions']):
        return jsonify({"message": "Quiz completed"})

    return jsonify({"question": quiz['questions'][current_question]['question']})

@app.route('/api/v1/score/<session_id>', methods=['GET'])
def get_user_score(session_id):
    """Get user's score for a specific quiz session"""
    if not request.current_user:
        abort(401)
    session = db._db.sessions.find_one({'_id': ObjectId(session_id)})
    if not session:
        abort(404, description="Session not found")
    return jsonify({"sessionid": session_id, "score": session['score']})

@app.route('/api/v1/leaderboard/<quiz_id>', methods=['GET'])
def get_leaderboard(quiz_id):
    """Get leaderboard for a specific quiz"""
    if not request.current_user:
        abort(401)
    leaderboard = list(db._db.sessions.find(
        {'quiz_id': ObjectId(quiz_id)},
        {'_id': 0, 'score': 1}
    ).sort('score', -1).limit(10))
    return jsonify({"quiz_id": quiz_id, "leaderboard": leaderboard})

if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(debug=True, host=host, port=port)
