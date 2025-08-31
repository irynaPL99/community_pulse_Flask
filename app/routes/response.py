from flask import Blueprint, jsonify, request
from app.models import db
from app.models.response import Response
from app.models.questions import Question


response_bp = Blueprint('response', __name__, url_prefix='/responses')

@response_bp.route('/', methods=['GET'])
def get_responses():
    """
    Returns statistic by responses
    :return:
    """
    try:
        responses = Response.query.all()
        data = [{
            'id': response.id,
            'question_id': response.question_id,
            'is_agree': response.is_agree,
            'question_text': response.question.question if response.question else None
        } for response in responses]
        return jsonify({
            'message': 'All responses:',
            'total': len(responses),
            'responses': data
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve responses'}), 500


@response_bp.route('/', methods=['POST'])
def create_response():
    """
    Creates a new response for a question.
    """
    data = request.get_json()
    if not data or 'question_id' not in data or 'is_agree' not in data:
        return jsonify({'error': 'Missing required fields (question_id, is_agree)'}), 400

    question_id = data['question_id']
    is_agree = data['is_agree']

    # Проверка существования вопроса
    question = Question.query.get(question_id)
    if not question:
        return jsonify({'error': 'Question with that id does not exist'}), 400

    # Валидация is_agree (должно быть булевым значением)
    if not isinstance(is_agree, bool):
        return jsonify({'error': 'is_agree must be a boolean value (true/false)'}), 400

    try:
        response = Response(question_id=question_id, is_agree=is_agree)
        db.session.add(response)
        db.session.commit()

        # Обновление статистики (можно интегрировать здесь или отдельно)
        update_statistics(question_id, is_agree)

        return jsonify({
            'message': 'Response created successfully',
            'id': response.id,
            'question_id': response.question_id,
            'is_agree': response.is_agree
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create response'}), 500

def update_statistics(question_id, is_agree):
    """
    Updates statistics for a question based on the response.
    """
    # глобальная функция, которая включает сохранение в базу данных.
    # обрабатывает создание новой записи и фиксацию изменений
    from app.models.questions import Statistic
    statistic = Statistic.query.filter_by(question_id=question_id).first()
    if not statistic:
        statistic = Statistic(question_id=question_id, agree_count=0, disagree_count=0)
        db.session.add(statistic)

    if is_agree:
        statistic.agree_count += 1
    else:
        statistic.disagree_count += 1

    db.session.commit()