from flask import Blueprint, jsonify, request
from app.models.questions import Statistic
from app.models import db

statistics_bp = Blueprint('statistics', __name__, url_prefix='/statistics')

@statistics_bp.route('/', methods=['GET'])
def get_all_statistics():
    """
    Returns statistics for all questions.
    """
    try:
        statistics = Statistic.query.all()
        data = [{
            'question_id': item.question_id,
            'agree_count': item.agree_count,
            'disagree_count': item.disagree_count
        } for item in statistics]
        return jsonify({
            'message': 'All statistics:',
            'total': len(statistics),
            'statistics': data
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve statistics'}), 500