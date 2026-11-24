from flask import Flask, render_template, redirect, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap5
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float


# Create instance
app = Flask(__name__)
bootstrap = Bootstrap5(app)


##CREATE DATABASE
class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books-collection.db"

# Create the extension
db = SQLAlchemy(model_class=Base)
# Initialise the app with the extension
db.init_app(app)


##CREATE TABLE
class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Book {self.title}>'

# Create table schema in the database. Requires application context.
with app.app_context():
    db.create_all()


# Collection of all books
all_books = []

# Home page
@app.route("/")
def index():
	result = db.session.execute(db.select(Book).order_by(Book.title))
	all_books = result.scalars().all()
	return render_template("index.html", books=all_books)


# Add books page
@app.route("/add", methods=['GET', 'POST'])
def add():
	if request.method == 'POST':
		new_record = Book(
			title=request.form['title'],
			author=request.form['author'],
			rating=float(request.form['rating'])
		)
		db.session.add(new_record)
		db.session.commit()

		return redirect(url_for('index'))

	return render_template("add.html")


if __name__ == '__main__':
	app.run(debug=True)