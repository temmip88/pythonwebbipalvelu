from flask import Flask, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy #m
from flask_wtf import FlaskForm #m
from wtforms.ext.sqlalchemy.orm import model_form #m

app = Flask(__name__)
app.secret_key = "ier1guvee0fohguuthooth3ahTood7" #m
db = SQLAlchemy(app) #m

class WOWexpansion(db.Model):
    id = db.Column(db.Integer, primary_key=True) #m
    name = db.Column(db.String, nullable=False) #m
    year = db.Column(db.String, nullable=False)

expansionForm = model_form(WOWexpansion, base_class=FlaskForm, db_session=db.session) #m

@app.before_first_request #m
def initDB(): #m
    db.create_all() #m

    expansion = WOWexpansion(name="Classic", year="2004") #m
    db.session.add(expansion) #m

    expansion = WOWexpansion(name="TBC", year="2007")
    db.session.add(expansion)

    expansion = WOWexpansion(name="WotLK", year="2008")
    db.session.add(expansion)

    db.session.commit()

@app.route("/new", methods=["GET", "POST"]) #m
def newExpansion(): #m
    form = expansionForm() #m

    if form.validate_on_submit(): #m
        expansion = WOWexpansion() #m
        form.populate_obj(expansion)

        db.session.add(expansion) #m
        db.session.commit() #m

        print("Added your expansion, thanks.")
        flash("Added")
        return redirect("/")
    
    return render_template("new.html", form=form)

@app.route("/")
def index():
    expansions = WOWexpansion.query.all() #m
    return render_template("index.html", expansions=expansions)

if __name__=="__main__":
    app.run()
