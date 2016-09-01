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
	return defs

@app.route("/", methods=['POST', 'GET'])
def add_word():
	definitions = None
	if request.method == "GET":
		print(url_for('add_word'))

	if request.method == "POST":
		new_word = request.form['entry']
		print(new_word)
		definitions = get_definition(new_word)
		added_word = Word(new_word, date.today())
		db.session.add(added_word)
		for entry in definitions:
			db.session.add(Meanings(new_word, entry))
	db.session.commit()

	return render_template('index.html', name = 'words&shit', definitions = definitions)

if __name__ == "__main__":
    app.run(debug=True)