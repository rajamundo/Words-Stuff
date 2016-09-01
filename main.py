from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///definitions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *

def get_definition(new_word):
	payload = {'headword': new_word}
	try:
		r = requests.get("http://api.pearson.com/v2/dictionaries/ldoce5/entries", params = payload)
		print(r.url)
		#print(type(r.json()))
		response = r.json()
		results = response['results']
		defs = []
		for entry in results:
			for different_definitions in entry['senses']:
				record = different_definitions['definition']
				for meaning in record:
					defs.append(meaning)
	except Exception as e:
		print(e)

	return defs

@app.route("/", methods=['POST', 'GET'])
def add_word():
	definitions = None
	if request.method == "GET":
		print(url_for('add_word'))

	if request.method == "POST":
		try:
			new_word = request.form['entry']
			new_word = new_word.strip()
			book = request.form['book']
			print(new_word)
			definitions = get_definition(new_word)
			added_word = Word(new_word, book, date.today())
			db.session.add(added_word)
			for entry in definitions:
				db.session.add(Meanings(new_word, entry))
			db.session.commit()
		except Exception as e:
			print(e)
			definitions = ['Word as already been added']

	return render_template('index.html', name = 'words&shit', definitions = definitions)

@app.route("/words", methods=['GET'])
def get_all_words():
	words = Word.query.all()
	#could use below code if definitions wanted on same page as words
    #albumContents = db.session.query( Photo.url, Photo.picid, Photo.date, Contain.sequencenum, Contain.albumid, Contain.caption ).join( Contain, Contain.picid == Photo.picid ).filter( Contain.albumid == albumid ).all( )

	return render_template('words.html', words = words)

@app.route("/definitions", methods=['GET'])
def get_meanings():
	word = request.args.get('word_spelling')
	print(word)
	definitions = Meanings.query.filter_by(word_spelling = word)
	print(definitions)
	return render_template('definitions.html', definitions = definitions)

if __name__ == "__main__":
    app.run(debug=True)