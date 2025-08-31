# community_pulse (Flask)
# My Flask Project

## What is this?
This is a web app made with Flask. 
It manages categories, questions, responses, and statistics. 
You can add, update, and delete categories and questions.

## How to Set Up
1. **Install Python**: Make sure Python is on your computer.
2. **Get the code**: Download the project from the repository.
3. **Install tools**: Run `pip install -r requirements.txt` in the terminal.
4. **Set up database**: Run `flask db init`, then `flask db migrate -m "initial migration"`, and `flask db upgrade`.
5. **Start the app**: Use `export FLASK_ENV=development` and `flask run`.
6. **Test it**: Use Postman to send requests (e.g., POST, PUT, DELETE) to `http://127.0.0.1:5000`.

## What Can It Do?
- Add new categories with a name.
- Update category names.
- Delete categories (if no questions are linked).
- Add questions with a category.
- Add "agree" or "disagree" responses.

## Project Files
- `app/`
  - `models/`
    - `__init__.py`: Starts models.
    - `questions.py`: Has Category and Question models.
    - `response.py`: Has Response model.
  - `schemas/`
    - `categories.py`: Pydantic schemas for categories.
    - `questions.py`: Pydantic schemas for questions.
    - `response.py`: Pydantic schemas for responses.
  - `routes/`
    - `categories.py`: Routes for categories.
    - `questions.py`: Routes for questions.
    - `response.py`: Routes for responses.
    - `statistics.py`: Routes for statistics.
  - `__init__.py`: Starts the Flask app.
- `config.py`: Holds app settings.
- `run.py`: Runs the app.
- `requirements.txt`: Lists needed tools.
- `README.md`: This file!

## Important Tips
- Send data in JSON format.
- Look at terminal errors if something fails.
- The app runs at `http://127.0.0.1:5000`.

## Help
If you have issues, check the error messages or ask for help!
