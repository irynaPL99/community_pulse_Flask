# app/scripts/create_default_category.py
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app import create_app, db
from app.models.questions import Category

app = create_app()
with app.app_context():
    if not Category.query.filter_by(name="Общая").first():
        category = Category(name="Общая")
        db.session.add(category)
        db.session.commit()
        print("Категория 'Общая' создана")
    else:
        print("Категория 'Общая' уже существует")