from flask import Flask, render_template, redirect, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm 
from wtforms.ext.sqlalchemy.orm import model_form 


app = Flask(__name__)
app.secret_key = "chuHukiechusoo7feekooboi0ungoh"
db = SQLAlchemy(app) 

class osoiteKirja(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)

osoiteForm = model_form(osoiteKirja, base_class=FlaskForm, db_session=db.session)

@app.before_first_request
def initDB():
    db.create_all()

    lisaaHlo = osoiteKirja(name="Pekka", address="Kujala 10", email="foo@bar")
    db.session.add(lisaaHlo)

    db.session.commit()

@app.route("/<int:id>/edit", methods=["GET", "POST"])
@app.route("/new", methods=["GET", "POST"])
def addNew(id=None):
    lisaaHlo = osoiteKirja()
    if id:
        lisaaHlo = osoiteKirja.query.get(id)

    form = osoiteForm(obj=lisaaHlo) 

    if form.validate_on_submit(): 
        
        form.populate_obj(lisaaHlo) 

        db.session.add(lisaaHlo)
        db.session.commit()

        print("Lisätty uusi henkilö")
        flash("Lisätty")
        return redirect("/")

    return render_template("new.html", form=form) 

@app.route("/<int:id>/delete")
def deleteGun(id):
    lisaaHlo = osoiteKirja.query.get_or_404(id)
    db.session.delete(lisaaHlo)
    db.session.commit()
    flash("Poistettu")
    return redirect("/")

@app.route("/")
def index():
    lisaaHlot = osoiteKirja.query.all() 
    return render_template("index.html", lisaaHlot=lisaaHlot)

if __name__=="__main__":
    app.run()
