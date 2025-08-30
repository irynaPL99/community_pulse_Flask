from . import db


class Response(db.Model):
    __tablename__ = 'responses'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    is_agree = db.Column(db.Boolean, nullable=False, default=False)
    #устанавливает связь "многие-к-одному" (много ответов могут относиться к одному вопросу)
    # nullable=False - всегда иметь значение (не может быть NULL)

    def __repr__(self):
        return f'Response {self.id=}, question_id: {self.question_id=}, is_agree: {self.is_agree=}'

    def __str__(self):
        return f'Response for question_id  {self.question_id}: {"Agree" if self.is_agree else "Disagree"} '
