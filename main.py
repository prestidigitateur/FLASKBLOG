from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

##CREATE DATABASE
uri = os.environ.get('DATABASE_URL')
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
#Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
db.create_all()

@app.route("/")
def hello():
    all_entries = db.session.query(Entry).all()
    return render_template("index.html", entries = all_entries)
@app.route("/<int:number>")
def num(number):
    return render_template("num.html", n = number)
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method=="POST":
        t = request.form['title']
        p = request.form['price']
        entry = Entry(title = t, price = p)
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('hello'))
    return render_template('add.html')
@app.route("/delete")
def delete():
    id = request.args.get('id')
    entry = Entry.query.get(id)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for("hello"))

app.run(debug=True)