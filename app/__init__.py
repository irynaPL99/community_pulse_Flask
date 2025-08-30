from flask import Flask
from flask_migrate import Migrate
from .models import db

from config import DevelopmentConfig, ProductionConfig, TestingConfig
from .routes.questions import questions_bp
from .routes.response import response_bp

from .models.response import Response
from .models.questions import Statistic, Question

import os


config_mapping = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
}

def create_app():
    env = os.getenv('FLASK_ENV', 'development')

    # получаем класс конфигурации из словаря "config_mapping".
    # Если env ('invalid') - не соответствует ни одному ключу в config_mapping,
    # используется DevelopmentConfig как значение по умолчанию
    config = config_mapping.get(env, DevelopmentConfig)

    # Аргумент __name__ указывает Flask, где искать шаблоны,
    # статические файлы и другие ресурсы относительно
    # расположения текущего модуля (app/__init__.py)
    app = Flask(__name__)

    #Загружает настройки из объекта config (например, DevelopmentConfig, ProductionConfig или TestingConfig)
    # в конфигурацию приложения app.config.
    # Объект config — это класс из файла config.py, содержащий атрибуты,
    # такие как DEBUG, SECRET_KEY, SQLALCHEMY_DATABASE_URI.
    app.config.from_object(config)

    # Метод db.init_app(app) связывает объект SQLAlchemy
    # (определенный как db = SQLAlchemy() в app/models/__init__.py)
    # с конкретным экземпляром Flask-приложения (app)
    db.init_app(app)

    # миграция всегда после связи БД с api
    migrate = Migrate()
    migrate.init_app(app, db)
    # commands for migration:
    # 1) flask db init - инициализирует миграции
    # 2) flask db migrate -m "name migration" -> /instance/test.db
    # 3) flask db upgrade -> update(create) in BD
    # flask db downgrade - откат последней миграции

    # Метод app.register_blueprint() связывает маршруты Blueprint с приложением,
    # делая их доступными для обработки HTTP-запросов
    app.register_blueprint(questions_bp)
    app.register_blueprint(response_bp)

    return app