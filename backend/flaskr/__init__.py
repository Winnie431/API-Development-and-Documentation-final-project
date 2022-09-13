import os
from tkinter.messagebox import QUESTION
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy import cast, String

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    db = SQLAlchemy(app)
    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """       
    # CORS(app, resources={r"*/questions/*": {"origins":"*"}})
    CORS(app)
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,PATCH"
        )
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    def paginate(request, selection):
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in selection]
        current_questions = questions[start:end]

        return current_questions
    
    @app.route("/categories")
    def retrieve_categories():
        try:
            categories= db.session.query(Category).order_by(Category.type).all()
            
            category = [category.format() for category in categories]

            if len(category) == 0:
                abort(404)

            return jsonify(
                {
                    "success": True,
                    "categories": category
                }
            )
        except:
            abort(404)

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route("/questions")
    def retrieve_questions():
        try:
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate(request, selection)
            
            # current_categories=Question.query.with_entities(Question.category).filter(Question.id).all()
            # current_category = [current_category.format() for current_category in current_categories]

            categories= Category.query.order_by(Category.id).all()
            category = [category.format() for category in categories]

            if len(current_questions) == 0:
                abort(404)

            return jsonify(
                {
                    "success": True,
                    "questions": current_questions,
                    "total_questions": len(Question.query.all()),
                    "current_category": current_questions,
                    "categories":category
                }
            )
        except:
            abort(404)

            
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate(request, selection)

            categories= Category.query.order_by(Category.id).all()
            category = [category.format() for category in categories]


            return jsonify(
                {
                    "success": True,
                    "deleted": question_id,
                    "questions": current_questions,
                    "total_questions": len(Question.query.all()),
                    "current_category": current_questions,
                    "categories":category
                }
            )

        except:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route("/questions", methods=["POST"])
    def create_question():      
         try:         
            body= request.get_json()
           
            #initially we set the values if they does not exist to none
            new_question = body.get("question",None)
            new_answer = body.get("answer",None)
            new_difficulty = body.get("difficulty",None)
            new_category = body.get("category",None)
        
            question = Question(
                question = new_question,
                answer = new_answer,
                difficulty= new_difficulty,
                category = new_category 
                )

            question.insert()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate(request, selection)

            categories= Category.query.order_by(Category.id).all() 
            category = [category.format() for category in categories]


            return jsonify({
                    "success": True,
                    "questions": current_questions,
                    "total_questions": len(Question.query.all()),
                    "current_category": current_questions,
                    "categories":category     
            })            
         except:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods = ['POST'])
    def search_question():
        body= request.get_json()
     
        search = body.get('searchTerm',None)
        # print(f'search input ',body)
        try:
            selection = Question.query.filter(Question.question.ilike(f'%{search}%'))

            questions = paginate(request, selection)

            return jsonify({
                    "success":True,               
                    "questions": questions,
                    "totalQuestions":  len(questions),
                    "currentCategory": questions
                })
        except:
            abort(404)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def get_category_questions(category_id):
        try:
            category = Category.query.filter(Category.id == category_id).one_or_none()
            if category is None:
                abort(404)
  
            selection = Question.query.filter(Question.category == cast (category_id,String)).limit(QUESTIONS_PER_PAGE).all()
            # print(f'question per category ',selection)
            questions = paginate(request,selection)
            return jsonify(
                    {
                        "success": True,
                        "questions": questions,
                        "total_questions":len(questions),
                        "current_category": category.type
                        
                    }
                )
        except:
          abort(404)


    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        try:
            body= request.get_json()
            
            quiz_category = body.get('quiz_category',None)

            previous_questions = body.get('previous_questions',None)
            query =  Question.query
            # we get the list of the selected category if they exist
            if int(quiz_category['id'])!=0:
                category = Category.query.filter(Category.id == quiz_category.get('id')).first()

                if category is None:
                    abort(404)
            # we query the questions based on the categories
                query = query.filter(Question.category == cast(quiz_category['id'],String))

            # we collect the questions which are not in the list of the previous questions
            if previous_questions:
                query= query.filter(Question.id.notin_(previous_questions))
            # we get the questions randomly
            question = query.order_by(db.func.random()).first()

    #  return questions if the exist else we return an empty string
            return jsonify(
                    {
                        'success': True,
                        'question': question.format() if question else ""
                    }
                )
        except:
            abort(404)


    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(405)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 405, "message": "method not allowed"}),
            405,
        )



    return app

