from flask import Flask, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form


app = Flask(__name__)
app.secret_key = "Ib0iT5ieguxoof0Xu5hi4Neengosai"
db = SQLAlchemy(app)

class Sammakot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)
    year = db.Column(db.String, nullable=False)


CommentForm = model_form(Sammakot, base_class=FlaskForm, db_session=db.session)

@app.before_first_request
def initMe():
    db.create_all()

    db.session.add(Sammakot(name = "Apustaja", country = "Fin", year = "2010"))
    db.session.add(Sammakot(name = "Lättä", country = "Fin", year = "2011"))
    db.session.add(Sammakot(name = "Pepe", country = "US", year = "2007"))

    db.session.commit()


@app.route("/new", methods=["GET", "POST"])
def addForm():
    form = CommentForm()
    return render_template("new.html", form = form)

@app.route("/msg")
def msgPage():
    flash("Clear skies")
    return redirect("/")

@app.route("/anothermsg")
def anotherMsg():
    flash("Cheeky breeky")
    return redirect("/")

@app.route("/")
def index():
    flash("A magical place")
    sammakot = Sammakot.query.all()
    return render_template("index.html", sammakot=sammakot)

if __name__=="__main__":
    app.run()
