from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    def paginated_list(page, to_be_paginated_list):
        start = (page - 1) * 10
        end = start + 10
        return to_be_paginated_list[start:end]

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization, true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories', methods=['GET'])
    def get_categories():
        try:
            categories = Category.query.all()
            data = {
                "success": True,
                "categories": {}
            }
            for category in categories:
                data["categories"][category.id] = category.type
        except ConnectionError:
            abort(503)

        return jsonify(data)

    @app.route('/questions', methods=['GET', 'POST'])
    def questions():
        if request.method == 'GET':
            page = request.args.get('page', 1, type=int)
            data = {
                "questions": [],
                "total_questions": 0,
                "current_category": None,
                "categories": {},
                "success": True
            }
            try:
                categories = Category.query.order_by(Category.id).all()
                questions = Question.query.order_by(Question.id).all()
                paginated_questions = paginated_list(page, questions)
                if len(paginated_questions) == 0:
                    abort(404)

                for question in paginated_questions:
                    data["questions"].append(question.format())

                for category in categories:
                    data["categories"][category.id] = category.type

                data["total_questions"] = len(questions)

            except ConnectionError:
                abort(503)

        elif request.method == 'POST':
            question = request.get_json()['question']
            answer = request.get_json()['answer']
            difficulty = request.get_json()['difficulty']
            category = request.get_json()['category']
            data = {
                'success': True,
                'message': 'Question has been added successfully'
            }

            try:
                query = Question.query.filter_by(question=question)
                existing_question = query.first()
                if existing_question is not None:
                    abort(422)
                else:
                    question = Question(
                        question=question,
                        answer=answer,
                        difficulty=difficulty,
                        category=category)
                    question.insert()
            except ConnectionError:
                abort(503)

        return jsonify(data)

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            data = {
                "success": True,
                "deleted_id": question_id
            }
            if question is None:
                abort(422)
            else:
                question.delete()
        except ConnectionError:
            abort(503)

        return jsonify(data)

    @app.route('/questions/search', methods=['POST'])
    def search_question():
        search_term = request.get_json()['searchTerm']
        data = {
            'success': True,
            'total_questions': 0,
            'questions': [],
            'current_category': None
        }
        try:
            q = Question.query
            q_query = q.filter(Question.question.ilike(f'%{search_term}%'))
            found_questions = q_query.all()
            for question in found_questions:
                data['questions'].append(question.format())
                data['total_questions'] = len(found_questions)

        except ConnectionError:
            abort(503)

        return jsonify(data)

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def questions_by_category(category_id):
        data = {
            'success': True,
            'questions': [],
            'total_questions': 0,
            'current_category': category_id
        }

        try:
            category = Category.query.get(category_id)
            if category is None:
                abort(404)
            else:
                q_query = Question.query.filter_by(category=category_id)
                questions = q_query.order_by(Question.id).all()
                data['total_questions'] = len(questions)
                for question in questions:
                    data['questions'].append(question.format())
        except ConnectionError:
            abort(503)

        return jsonify(data)

    @app.route('/quizzes', methods=['POST'])
    def quizzes():
        previous_question_ids = request.get_json()['previous_questions']
        quiz_category_id = request.get_json()['quiz_category']['id']
        data = {
            'success': True,
            'question': None
        }
        questions = []

        try:
            category = Category.query.get(quiz_category_id)
            if category is None:
                abort(422)

            if quiz_category_id == 0:
                q_query = Question.query
            else:
                q_query = Question.query.filter_by(category=quiz_category_id)

            if len(previous_question_ids) > 0:
                for previous_id in previous_question_ids:
                    q_query = q_query.filter(Question.id != previous_id)

            questions = q_query.all()
            if len(questions) > 0:
                random_int = random.randint(0, len(questions)-1)
                random_question = questions[random_int]
                data['question'] = random_question.format()
        except ConnectionError:
            abort(503)

        return jsonify(data)

    @app.errorhandler(503)
    def db_connectivity_issues(error):
        return jsonify({
            'success': False,
            'error': 503,
            'message': ':-( Issue communicating with the database :-('}), 503

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource does not exist'}), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable'}), 422

    return app
