from main import db


class Word(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    spelling = db.Column(db.String(80), primary_key=True)
    date = db.Column(db.DateTime)

    def __init__(self, spelling, date):
        self.spelling = spelling
        self.date = date

    def __repr__(self):
        return '<Word %r>' % self.spelling

class Meanings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word_spelling = db.Column(db.String(80), db.ForeignKey('word.spelling'))
    definition = db.Column(db.String(200))

    def __init__(self, word_spelling, definition):
        self.word_spelling = word_spelling
        self.definition = definition

    def __repr__(self):
        return '<Meanings %r>' % self.definition