from flask import Flask, render_template, redirect, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
bootstrap = Bootstrap5(app)

@app.route("/")
def index():
	return render_template("index.html")



@app.route("/add")
def add():
	return render_template("add.html")


if __name__ == '__main__':
	app.run(debug=True)