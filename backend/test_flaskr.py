from ctypes import cast
import os
import unittest
import json
from urllib import response
from flask_sqlalchemy import SQLAlchemy
from setting import DB_NAME, DB_USER, DB_PASSWORD
from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = DB_NAME
        self.database_path = "postgresql://{}:{}@{}/{}".format(DB_USER, DB_PASSWORD, "localhost:5433", self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {"question": "What does the Acronym winnie Stand for?", "answer": "winnie", 
        "difficulty":4,"category": "Art"}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):        
        response = self.client().get("/categories")
        data = json.loads(response.data)

        self.assertEqual(response.status_code,200)
        self.assertEqual(data["success"],True)
        self.assertTrue(data["categories"])


    def test_get_paginated_questions(self):
        response = self.client().get("/questions")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["current_category"])
        self.assertTrue(data["categories"])

    def test_404_sent_requesting_beyond_valid_page(self):
        response = self.client().get("/questions?page=1000")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_delete_question(self):
        question = {}
        with self.app.app_context():
            question = Question.query.first().format()
        response = self.client().delete(f"/questions/{question['id']}")
        self.assertEqual(response.status_code, 200)
        with self.app.app_context():
            quest = Question.query.filter(Question.id==question['id']).one_or_none()
            self.assertIsNone(quest)

    def test_404_delete_none_existing_question(self):
        max_id = 100000
        with self.app.app_context():
            q = Question.query.order_by(Question.id.desc()).first()
            if q:
                max_id = q.id
        response = self.client().delete(f"/questions/{max_id + 2}")
        self.assertEqual(response.status_code, 404)

        

    def test_create_new_question(self):
        response = self.client().post("/questions", json=self.new_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code,200)
        self.assertEqual(data["success"],True)
        self.assertTrue(len(data["questions"]))
 
    def test_get_question_search_with_results(self):
        response = self.client().post("/questions", json={"search": "what"})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
       

    def test_search_questions_with_no_response(self):
        response = self.client().post('/questions/search', json={'search_term': 'applejack'})
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(result['questions'])



    def test_get_paginated_categories_questions(self):
        response = self.client().get("/categories/1/questions")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertGreater(len(data['questions']), 0)
        self.assertEqual(data['current_category'], ' Science')
        

    def test_paginated_categories_question_not_exist(self):
        response = self.client().get("/categories/7/questions")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_play_quiz(self):
        
        response = self.client().post("/quizzes",json={"quiz_category":{"type":"Science","id":1},"previous_questions":[1,4,7]})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
     
        
    def test_unable_to_play_quiz(self):
        response = self.client().post("/quizzes")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")


        # error message
        
if __name__ == "__main__":
    unittest.main()