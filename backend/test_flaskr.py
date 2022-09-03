import os
import unittest
import json
from urllib import response
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.database_path = "postgresql://{}:{}@{}/{}".format("postgres", "postgres", "localhost:5433", self.database_name)
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
        print(f"the categories exist", response)

        self.assertEqual(response.status_code,200)
        self.assertEqual(data["success"],True)
        self.assertTrue(data["categories"])

    def test_categories_does_not_exist(self):        
        response = self.client().get("/categories")
        data = json.loads(response.data)
        print(f"the categories  does not exist", response)

        self.assertEqual(response.status_code,404)
        self.assertEqual(data["success"],False)
        self.assertEqual(len(data["categories"]),0)
        self.assertEqual(data["message"], "resource not found")


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
        print(f'hello testing questions',response)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_delete_question(self):
        response = self.client().delete('/questions/1')
        data = json.loads(response.data)    
        print(json.loads(response)   )
        question = Question.query.filter(Question.id == 1).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(question, None)

    def test_question_does_not_exist(self):
        response = self.client().delete("/questions/500")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_create_new_question(self):
        response = self.client().post("/questions", json=self.new_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code,200)
        self.assertEqual(data["success"],True)
        self.assertTrue(len(data["questions"]))
        

    def test_422_if_book_creation_fails(self):
        response = self.client().post("/questions", json=self.new_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code,422)
        self.assertEqual(data["success"],False)
        self.assertEqual(data["message"], "unprocessable")
      
    def test_get_question_search_with_results(self):
        response = self.client().post("/questions", json={"search": "what"})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
       

    def test_get_questions_search_without_results(self):
        response = self.client().post("/questions", json={"search": "applejacks"})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["total_questions"], 0)
        self.assertEqual(len(data["questions"]), 0)
        self.assertEqual(data["message"], "resource not found")

        # error message
        
if __name__ == "__main__":
    unittest.main()