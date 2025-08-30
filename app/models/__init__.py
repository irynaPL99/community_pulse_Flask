from flask_sqlalchemy import SQLAlchemy


# Этот объект предоставляет функциональность для определения моделей
# (ORM - Object-Relational Mapping),
# выполнения запросов и управления сессиями базы данных
db = SQLAlchemy()

# Объект db связывается с приложением Flask позже, в app/__init__.py,
# с помощью вызова db.init_app(app).
# Это позволяет Flask-SQLAlchemy использовать конфигурацию приложения
# (например, SQLALCHEMY_DATABASE_URI) для подключения к базе данных