from . import db
from .response import Response


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f'Category: {self.id=}, {self.name=}'

    def __str__(self):
        return self.name

class Question(db.Model):
    __tablename__ = 'questions'
    # Задает имя таблицы в базе данных как questions.
    # Без этой строки SQLAlchemy сгенерировал бы имя таблицы
    # на основе имени класса (question)

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False, unique=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    responses = db.relationship('Response', backref='question', lazy='dynamic')
    #Устанавливает связь !!!"один-ко-многим" с моделью Response !!!
    # (что один вопрос может иметь много ответов).
    # backref='question' создает обратную связь,
    # позволяя обращаться к вопросу из объекта Response
    # (например, response.question).
    # lazy='dynamic' означает, что связанные ответы не загружаются сразу,
    # а возвращаются как объект запроса (Query),
    # который можно дополнительно фильтровать
    # (например, question.responses.filter(...).all()).
    category = db.relationship('Category', backref=db.backref('questions', lazy='dynamic',order_by='Question.id'), lazy='joined')
    # связь "многие-к-одному" между Question и Category.
    # Много вопросов могут относиться к одной категории.
    # !! Полная форма "backref=db.backref(...)" позволяет настроить такие параметры,
    # как lazy, order_by, cascade, и другие, которые недоступны в краткой форме
    # lazy='joined' - чтобы question.category загружался сразу вместе с вопросом (без отдельного запроса)

    # Возвращает строковое представление объекта для отладки
    def __repr__(self):
        return f'Question: id {self.id=}, {self.question=}, category_id {self.category_id=}'

    # Возвращает текст вопроса для более удобного отображения
    def __str__(self):
        return self.question


class Statistic(db.Model):
    __tablename__ = 'statistics'

    # связь "один-к-одному" между вопросом и его статистикой
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), primary_key=True)
    agree_count = db.Column(db.Integer, nullable=False, default=0)
    disagree_count = db.Column(db.Integer, nullable=False, default=0)
    question = db.relationship('Question', backref=db.backref('statistic', uselist=False, lazy='joined'))
    # uselist=False: Указывает, что связь является один-к-одному (one-to-one), а не "один-ко-многим".

    def __repr__(self):
        return f'Statistic: id {self.question_id=}, agree {self.agree_count=}, disagree {self.disagree_count=}'

    def __str__(self):
        return f'id: {self.question_id}, agree: {self.agree_count}, disagree: {self.disagree_count}'

    # update_counts - метод экземпляра класса, который не фиксирует изменения в базе данных
    #def update_counts(self, agree=True):
    #    """update agree_count or disagree_count"""
    #    if agree:
    #        self.agree_count += 1
    #    else:
    #        self.disagree_count += 1