import os
import unittest
from unittest.mock import Mock
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}@{}/{}".format('postgres:PONkas23','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    # Get Categories
    def test_get_categories(self):
       # Testing a successful get request for categories
       res = self.client().get('/categories')
       data = json.loads(res.data)
       self.assertEqual(res.status_code, 200)
       self.assertEqual(data["categories"]["1"], 'Science') 
       self.assertEqual(data["success"], True) 

    def test_503_categories(self):
       # Testing a failed get request for categories, database connectivity issues
       requests = Mock()
       requests.get.side_effect = ConnectionError()
       with self.assertRaises(ConnectionError):
           res = requests.get('/categories')
           data = json.loads(res.data)
           self.assertEqual(res.status_code, 503)
           self.assertEqual(data['success'], False) 
           self.assertEqual(data['message'], ':-( Issue communicating with the database :-(')
           self.assertEqual(data['error'], 503)
    
    # Get Questions
    def test_get_questions(self):
        # Testing a successful get request for questions
        res = self.client().get('questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertEqual(data['current_category'], None)
        self.assertTrue(data['questions'])
    
    def test_404_questions(self):
        # Testing a failed get request, page does not exist
        res = self.client().get('questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource does not exist')
        self.assertEqual(data['error'], 404)

    # Delete a Question
    def test_delete_question(self):
        # Testing a question delete
        res = self.client().delete('questions/4')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_id'], 4)

    def test_422_delete_question(self):
        # Testing a fail in deleting a question, due to it not existing
        res = self.client().delete('questions/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')
        self.assertEqual(data['error'], 422) 
    
    # Post a Question
    def test_post_question_422(self):
        # Testing 
        res = self.client().post('questions', json={'question': "What's my name?", 'answer': 'Satas', 'difficulty': 1, 'category': '5'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')
        self.assertEqual(data['error'], 422) 

    def test_post_question(self):
        # Testing a question post
        res = self.client().post('questions', json={'question': "What's my name?", 'answer': 'Satas', 'difficulty': 1, 'category': '5'})
        data = json.loads(res.data)

        added_question = Question.query.filter_by(answer='Satas').first()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Question has been added successfully')
        self.assertEqual(added_question.answer, 'Satas')
        self.assertEqual(added_question.question, "What's my name?")
        self.assertEqual(added_question.difficulty, 1)
        self.assertEqual(added_question.category, 5)
    
    # Post Searched Questions
    def test_post_search_questions(self):
        # Testing a successful post request for searched questions
        res = self.client().post('questions/search', json={'searchTerm': ' '})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], None)
        self.assertTrue(len(data['questions']))

    def test_503_search_questions(self):
       # Testing a failed get request for categories, database connectivity issues
       requests = Mock()
       requests.post.side_effect = ConnectionError()
       with self.assertRaises(ConnectionError):
           res = requests.post('questions/search', json={'searchTerm', 'title'})
           data = json.loads(res.data)
           self.assertEqual(res.status_code, 503)
           self.assertEqual(data['success'], False) 
           self.assertEqual(data['message'], ':-( Issue communicating with the database :-(')
           self.assertEqual(data['error'], 503)

    # Get Questions by Category
    def test_get_questions_by_category(self):
        # Testing a successful get request for questions by Category
        res = self.client().get('categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], 1)
        self.assertTrue(data['questions'])
    
    def test_404_questions_by_category(self):
        # Testing a failed get request, page does not exist
        res = self.client().get('categories/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource does not exist')
        self.assertEqual(data['error'], 404)
    
    # Post Quiz Questions
    def test_post_quizzes(self):
        # Testing a successful post request for quiz questions
        res = self.client().post('quizzes', json={'previous_questions': [], 'quiz_category': {'type': 'Science', 'id': "1"}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_422_quizzes(self):
       # Testing a failed post request for quizzes, category does not exist
        res = self.client().post('quizzes', json={'previous_questions': [], 'quiz_category': {'type': 'Basketball', 'id': "12"}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')
        self.assertEqual(data['error'], 422)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()