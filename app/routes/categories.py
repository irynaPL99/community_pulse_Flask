from flask import Blueprint, jsonify, request
from app.models.questions import Question, Category
from app.models import db


categories_bp = Blueprint('categories', __name__, url_prefix='/categories')


@categories_bp.route('/', methods=['POST'])
def create_category():
    """
    Creates a new category.
    """
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'No name provided'}), 400

    name = data['name'].strip()
    if not name:
        return jsonify({'error': 'Name cannot be empty'}), 400

    # Проверка уникальности имени (из-за unique=True в модели)
    existing_category = Category.query.filter_by(name=name).first()
    if existing_category:
        return jsonify({'error': 'Category with this name already exists'}), 400

    category = Category(name=name)
    db.session.add(category)
    db.session.commit()

    return jsonify({
        'message': 'Category created successfully:',
        'id': category.id,
        'name': category.name
    }), 201

@categories_bp.route('/<int:id>', methods=['PUT'])
def update_category(id):
    """
    Updates a category by id.
    """
    category = Category.query.get(id)
    if not category:
        return jsonify({'error': 'Category with that id does not exist'}), 404

    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'No name provided'}), 400

    name = data['name'].strip()
    if not name:
        return jsonify({'error': 'Name cannot be empty'}), 400

    # Проверка уникальности имени (кроме текущей категории)
    existing_category = Category.query.filter_by(name=name).first()
    if existing_category and existing_category.id != id:
        return jsonify({'error': 'Category with this name already exists'}), 400

    category.name = name
    db.session.commit()

    return jsonify({
        'message': 'Category updated successfully:',
        'id': category.id,
        'name': category.name
    }), 200

@categories_bp.route('/<int:id>', methods=['DELETE'])
def delete_category(id):
    """
    Deletes a category by id.
    """
    category = Category.query.get(id)
    if not category:
        return jsonify({'error': 'Category with that id does not exist'}), 404

    # Проверка, есть ли вопросы, связанные с категорией
    if Question.query.filter_by(category_id=id).count() > 0:
        return jsonify({'error': 'Cannot delete category with associated questions'}), 400

    db.session.delete(category)
    db.session.commit()

    return jsonify({
        'message': 'Category deleted successfully',
        'id': id
    }), 200

@categories_bp.route('/', methods=['GET'])
def get_all_categories():
    """
    Returns a list of all categories.
    """
    categories = Category.query.all()
    data = [{'id': item.id, 'name': item.name} for item in categories]
    return jsonify({
        'message': 'All categories:',
        'total': len(categories),
        'categories': data
    }), 200