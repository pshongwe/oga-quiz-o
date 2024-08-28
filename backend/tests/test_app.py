import unittest
from app import app, db
from werkzeug.security import generate_password_hash
from bson.objectid import ObjectId

class OgaQuizOAPITestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
        # Insert a test user
        self.test_user = {
            'email': 'testuser@example.com',
            'hashed_password': generate_password_hash('testpassword')
        }
        self.user_id = db._db.users.insert_one(self.test_user).inserted_id
    
    def tearDown(self):
        # Clean up the database after each test
        db._db.users.delete_many({})
        db._db.quizzes.delete_many({})
        db._db.sessions.delete_many({})
    
    def test_signup(self):
        response = self.app.post('/api/v1/auth_session/signup', json={
            'email': 'newuser@example.com',
            'password': 'newpassword'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('User created successfully', response.json['message'])

    def test_login(self):
        response = self.app.post('/api/v1/auth_session/login', json={
            'email': 'testuser@example.com',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('logged in', response.json['message'])
    
    def test_login_invalid_credentials(self):
        response = self.app.post('/api/v1/auth_session/login', json={
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn('Invalid credentials', response.json['error'])

    def test_create_quiz(self):
        # Login first to set the session
        self.app.post('/api/v1/auth_session/login', json={
            'email': 'testuser@example.com',
            'password': 'testpassword'
        })
        
        response = self.app.post('/api/v1/quizzes/', json={
            'title': 'Sample Quiz',
            'options': ['Option 1', 'Option 2', 'Option 3', 'Option 4'],
            'correctAnswer': 'Option 1'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Quiz created successfully', response.json['message'])
    
    def test_get_quiz(self):
        quiz_id = db._db.quizzes.insert_one({
            'title': 'Sample Quiz',
            'options': ['Option 1', 'Option 2', 'Option 3', 'Option 4'],
            'correctAnswer': 'Option 1'
        }).inserted_id
        
        response = self.app.get(f'/api/v1/quizzes/{quiz_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['title'], 'Sample Quiz')

    def test_add_question_to_quiz(self):
        quiz_id = db._db.quizzes.insert_one({
            'title': 'Sample Quiz',
            'options': ['Option 1', 'Option 2', 'Option 3', 'Option 4'],
            'correctAnswer': 'Option 1'
        }).inserted_id
        
        response = self.app.post(f'/api/v1/quizzes/{quiz_id}/question', json={
            'question': 'Sample Question?',
            'correctAnswer': 'Option 1'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Question added successfully', response.json['message'])
    
    def test_start_quiz_session(self):
        quiz_id = db._db.quizzes.insert_one({
            'title': 'Sample Quiz',
            'options': ['Option 1', 'Option 2', 'Option 3', 'Option 4'],
            'correctAnswer': 'Option 1'
        }).inserted_id
        
        response = self.app.post(f'/api/v1/quizzes/{quiz_id}/start')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Quiz session started', response.json['message'])

    def test_get_leaderboard(self):
        quiz_id = db._db.quizzes.insert_one({
            'title': 'Sample Quiz',
            'options': ['Option 1', 'Option 2', 'Option 3', 'Option 4'],
            'correctAnswer': 'Option 1'
        }).inserted_id

        session_id = db._db.sessions.insert_one({
            'quiz_id': quiz_id,
            'current_question': 0,
            'score': 3
        }).inserted_id

        response = self.app.get(f'/api/v1/leaderboard/{quiz_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('leaderboard', response.json)

if __name__ == '__main__':
    unittest.main()
