from app import create_app, db
from app.models.questions import Category, Question
from app.models.response import Response

app = create_app()
with app.app_context():
    db.create_all()  # На случай, если таблицы ещё не созданы
    # Создаем категорию
    category = Category(name="Общая")
    db.session.add(category)
    db.session.commit()
    # Создаем вопрос
    question = Question(question="Тестовый вопрос", category_id=category.id)
    db.session.add(question)
    db.session.commit()
    # Создаем ответ (опционально)
    response = Response(question_id=question.id, is_agree=True)
    db.session.add(response)
    db.session.commit()