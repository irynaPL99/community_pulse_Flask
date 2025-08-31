from flask import Blueprint, jsonify, request
from app.models.questions import Question, Category, Statistic
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
    return jsonify({
        'message': 'All questions:',
        'total': len(data),
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

    try:
        question = Question(question=data['question'])
        if 'category_id' in data:
            question.category_id = data['category_id']
        db.session.add(question)
        db.session.commit()
        return jsonify({'id': question.id, 'question': question.question, 'category_id': question.category_id}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({'error': 'Internal server error'}), 500


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
        'question': question.question,
        'category_id': question.category_id,
        'category_name': question.category.name if question.category else None
    }), 200


@questions_bp.route('/<int:id>', methods=['PUT'])
def update_question(id):
    """
    Updates a question and category by id.
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

    # update text
    question.question = text

    # update category_id
    if 'category_id' in data:
        new_category_id = data['category_id']
        category = Category.query.get(new_category_id)
        if not category:
            return jsonify({'error': 'Category with that id does not exist'}), 400
        question.category_id = new_category_id
    db.session.commit()

    return jsonify({
        'message': 'Question updated successfully:',
        'question': question.question,
        'category_id': question.category_id,
        'category_name': question.category.name if question.category else None
    }), 200


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

@questions_bp.route('/<int:id>/statistics', methods=['GET'])
def get_question_statistics(id):
    """
    Returns statistics for a specific question by id.
    """
    question = Question.query.get(id)
    if not question:
        return jsonify({'error': 'Question with that id does not exist'}), 404

    statistic = Statistic.query.filter_by(question_id=id).first()
    if not statistic:
        return jsonify({
            'message': 'No statistics available for this question',
            'question_id': id,
            'agree_count': 0,
            'disagree_count': 0
        }), 200

    return jsonify({
        'message': 'Statistics:',
        'question_id': id,
        'agree_count': statistic.agree_count,
        'disagree_count': statistic.disagree_count
    }), 200
