from flask import Flask, render_template, redirect, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm #m
from wtforms.ext.sqlalchemy.orm import model_form #m

SQLALCHEMY_TRACK_MODIFICATIONS=True

app = Flask(__name__)
app.secret_key = "fa7eengauzeeBohVaikoh1Aecae3ei"
db = SQLAlchemy(app) #m

class gunDay(db.Model):
    id = db.Column(db.Integer, primary_key=True) #m
    gunType = db.Column(db.String, nullable=False)
    gunRange = db.Column(db.String, nullable=False)
    visit = db.Column(db.String, nullable=False)

gunRangeForm = model_form(gunDay, base_class=FlaskForm, db_session=db.session) #m

@app.before_first_request #m
def initDB():
    db.create_all()

    addGun = gunDay(gunType="Pistooli", gunRange="Osuva Kamppi", visit="16.5.2020")
    db.session.add(addGun)

    addGun = gunDay(gunType="Pistooli", gunRange="Osuva Tähtitorninmäki", visit="23.6.2020")
    db.session.add(addGun)

    addGun = gunDay(gunType="Revolveri", gunRange="Joensuu SAR", visit="1.10.2020")
    db.session.add(addGun)

    db.session.commit()

@app.route("/<int:id>/edit", methods=["GET", "POST"])
@app.route("/new", methods=["GET", "POST"])
def addNew(id=None):
    addGun = gunDay()
    if id:
        addGun = gunDay.query.get_or_404(id)

    form = gunRangeForm(obj=addGun) #m

    if form.validate_on_submit(): #m
        #addGun = gunDay() #m
        form.populate_obj(addGun) #m

        db.session.add(addGun)
        db.session.commit()

        print("Added a new rangeday")
        flash("Added")
        return redirect("/")

    return render_template("new.html", form=form) #m

@app.route("/<int:id>/delete")
def deleteGun(id):
    addGun = gunDay.query.get_or_404(id)
    db.session.delete(addGun)
    db.session.commit()
    
    flash("Deleted")
    return redirect("/")


@app.route("/")
def index():
    addGuns = gunDay.query.all() #m
    return render_template("index.html", addGuns=addGuns)

if __name__=="__main__":
    app.run()
