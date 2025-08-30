# tests/test_questions.py
import pytest
from app import create_app, db
from app.models.questions import Question, Category

@pytest.fixture
def app():
    """create test Flask, TestingConfig."""
    app = create_app()
    app.config.from_object('config.TestingConfig')
    with app.app_context():
        db.create_all()  # create tables
        yield app
        db.drop_all()    # drop tables

@pytest.fixture
def client(app):
    """Test client for HTTP-requests."""
    return app.test_client()

def test_get_questions_with_data(client):
    """get questions with data"""
    # test data
    with client.application.app_context():
        # create Category "Общая"
        category = Category(name="Общая")
        db.session.add(category)
        db.session.commit()

        # create questions
        question1 = Question(question="Гамбург - столица Германии?", category_id=category.id)
        question2 = Question(question="Вы любите путешествовать?", category_id=category.id)
        db.session.add_all([question1, question2])
        db.session.commit()

        # run request HTTP
        response = client.get('/questions/')

        # check the answer
        assert response.status_code == 200
        assert response.json['message'] == 'All questions:'
        assert len(response.json['data']) == 2
        assert response.json['data'][0]['question'] == "Гамбург - столица Германии?"
        assert response.json['data'][1]['question'] == "Вы любите путешествовать?"
        assert response.json['data'][0]['id'] == 1
        assert response.json['data'][1]['id'] == 2
        assert response.json['data'][0]['category_id'] == 1
        assert response.json['data'][1]['category_id'] == 1
        assert response.json['data'][0]['category_name'] == "Общая"
        assert response.json['data'][1]['category_name'] == "Общая"