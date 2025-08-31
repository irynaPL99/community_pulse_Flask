from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from app.models.questions import Question, Category
from app.models import db
from app.schemas.categories import CategoryCreate, CategoryUpdate, CategoryUpdateResponse, CategoryResponse
from app.schemas.categories import CategoryDeleteResponse

categories_bp = Blueprint('categories', __name__, url_prefix='/categories')

@categories_bp.route('/', methods=['POST'])
def create_category():
    """
    Creates a new category.
    """
    data = request.get_json()
    if not data:    # Pydantic автоматически проверяет наличие и корректность name
        return jsonify({'error': 'No name provided'}), 400

    try:
        category_data = CategoryCreate(**data)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    try:
        name = category_data.name.strip()
        if not name:    # Pydantic не проверяет пустые строки после обрезки
            return jsonify({'error': 'Name cannot be empty'}), 400

        # Проверка уникальности имени (из-за unique=True в модели)
        existing_category = Category.query.filter_by(name=name).first()
        if existing_category:
            return jsonify({'error': 'Category with this name already exists'}), 400

        category = Category(name=name)
        db.session.add(category)
        db.session.commit()

        # Формирование ответа с данными из сохраненного объекта
        category_response = CategoryResponse(id=category.id, name=category.name)
        response_data = CategoryUpdateResponse(
            message='Category created successfully:',
            data=category_response
        )
        return jsonify(response_data.model_dump()), 201  # model_dump() ->dict

    except Exception as e:
        db.session.rollback()
        print(f"Error creating category: {str(e)}")  # Для отладки, можно убрать
        return jsonify({'error': 'Internal server error'}), 500

@categories_bp.route('/<int:id>', methods=['PUT'])
def update_category(id):
    """
    Updates a category's name by id.
    """
    category = Category.query.get(id)
    if not category:
        return jsonify({'error': 'Category with that id does not exist'}), 404

    data = request.get_json()
    if not data:     # Pydantic автоматически проверяет наличие и корректность name
        return jsonify({'error': 'No name provided'}), 400

    try:
        category_data = CategoryUpdate(**data)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    try:
        name = category_data.name.strip()
        if not name:
            return jsonify({'error': 'Name cannot be empty'}), 400

        # Проверка уникальности имени (кроме текущей категории)
        existing_category = Category.query.filter_by(name=name).first()
        if existing_category and existing_category.id != id:
            return jsonify({'error': 'Category with this name already exists'}), 400

        category.name = name
        db.session.commit()

        # Формирование ответа с сообщением и данными
        category_response = CategoryResponse(id=category.id, name=category.name)
        response_data = CategoryUpdateResponse(
            message='Category updated successfully:',
            data=category_response
        )
        return jsonify(response_data.model_dump()), 200 # model_dump() ->dict
    except Exception as e:
        db.session.rollback()
        print(f"Error updating category: {str(e)}")  # Для отладки, можно убрать
        return jsonify({'error': 'Internal server error'}), 500

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

    try:
        db.session.delete(category)
        db.session.commit()

        # Формирование ответа с использованием Pydantic
        response_data = CategoryDeleteResponse(
            message='Category deleted successfully:',
            id=id
        )
        return jsonify(response_data.model_dump()), 200 # model_dump()->dict
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting category: {str(e)}")  # Для отладки, можно убрать
        return jsonify({'error': 'Internal server error'}), 500


@categories_bp.route('/', methods=['GET'])
def get_all_categories():
    """
    Returns a list of all categories.
    """
    categories = Category.query.all()
    data_categories = []
    for item in categories:
        try:
            #  Сериализуем объекты SQLAlchemy в Pydantic модели с валидацией
            res = CategoryResponse.model_validate(item)
            res = res.model_dump()  # -> dict
            data_categories.append(res)
        except ValidationError as e:
            continue

    return jsonify({
        'message': 'All categories:',
        'total': len(data_categories),
        'data': data_categories
    }), 200