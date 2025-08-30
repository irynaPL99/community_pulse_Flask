from flask import Blueprint, jsonify, request
from app.models.questions import Question
from app.models import db


questions_bp = Blueprint('questions', __name__, url_prefix='/questions')


@questions_bp.route('/', methods=['GET'])
def get_questions():
    """
    Returns a list of all questions.
    """
    questions = Question.query.all()
    data = [
        {
            'id': item.id,
            'question': item.question,
            'category_id': item.category_id,
            'category_name': item.category.name if item.category else None
        }
         for item in questions]
    #return jsonify(data)
    return jsonify({
        'message': 'All questions:',
        'data': data
    }), 200


@questions_bp.route('/', methods=['POST'])
def create_question():
    """
    Creates a new question.
    """
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({'error': 'No text provided'}), 400

    question = Question(question=data['question'])
    db.session.add(question)
    db.session.commit()

    return jsonify({'id': question.id, 'question': question.question}), 201


@questions_bp.route('/<int:id>', methods=['GET'])
def get_question(id):
    """
    Returns a question by id.
    """
    question = Question.query.get(id)
    if not question: # question is None
        return jsonify({'error': 'Question with that id does not exist'}), 404

    return jsonify({
        'id': question.id,
        'question': question.question}), 200


@questions_bp.route('/<int:id>', methods=['PUT'])
def update_question(id):
    """
    Updates a question by id.
    """
    question = Question.query.get(id)
    if not question:
        return jsonify({'error': 'Question with that id does not exist'}), 404

    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({'error': 'No question text provided'}), 400

    text = data['question'].strip()
    if not text:
        return jsonify({'error': 'No question text provided'}), 400

    question.question = text
    db.session.commit()
    # return jsonify({'id': question.id, 'question': question.question}), 200
    return jsonify({'message': 'Question updated successfully'}), 200




@questions_bp.route('/<int:id>', methods=['DELETE'])
def delete_question(id):
    """
    Deletes a question by id.
    """
    question = Question.query.get(id)
    if not question: # if question is None
        return jsonify({'error': 'Question with that id does not exist'}), 404

    db.session.delete(question)
    db.session.commit()
    return jsonify({'message': 'Question deleted successfully'}), 200