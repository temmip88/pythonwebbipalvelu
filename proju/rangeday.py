# Used notes from Tero Karvinen course Python Web Service From Idea to Production 
from flask import Flask, render_template, redirect, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, validators

SQLALCHEMY_TRACK_MODIFICATIONS = True

app = Flask(__name__)
app.secret_key = "see0Raefoo4cohM7wei4poihie0aeH"
db = SQLAlchemy(app)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql:///teemuwsgi'


class gunDay(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gunType = db.Column(db.String, nullable=False)
    gunCaliber = db.Column(db.String, nullable=False)
    howMany = db.Column(db.String, nullable=False)
    gunRange = db.Column(db.String, nullable=False)
    visit = db.Column(db.String, nullable=False)


gunRangeForm = model_form(gunDay, base_class=FlaskForm, db_session=db.session)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    passwordHash = db.Column(db.String, nullable=False)

    def setPassword(self, password):
        self.passwordHash = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.passwordHash, password)

    def __str__(self):
        return f"<User {escape(self.email)}>"


class UserForm(FlaskForm):
    email = StringField("email", validators=[validators.Email()])
    password = PasswordField("password", validators=[validators.InputRequired()])


def currentUser():
    try:
        uid = int(session["uid"])
    except:
        return None
    return User.query.get(uid)


app.jinja_env.globals["currentUser"] = currentUser


@app.route("/user/login", methods=["GET", "POST"])
def loginView():
    form = UserForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()

        if not user:
            flash("Login failed.")
            print("No such user")
            return redirect("/user/login")
        if not user.checkPassword(password):
            flash("Wrong password.")
            print("Wrong password")
            return redirect("/user/login")

        session["uid"] = user.id

        flash("Login successful.")
        return redirect("/")

    return render_template("login.html", form=form)


@app.route("/logout")
def logoutView():
    session["uid"] = None
    flash("Logged out")
    return redirect("/")


@app.route("/user/register", methods=["GET", "POST"])
def registerView():
    form = UserForm()

    if form.validate_on_submit():
        
        user = User()

#        if User.query.filter_by(email=email).first():
#            flash("User already exits! Please log in.")
#            return redirect("/user/login")
        user.email = form.email.data
        user.setPassword(password)

        db.session.add(user)
        db.session.commit()

        flash("Registration complete, please log in")
        return redirect("/user/login")

    return render_template("register.html", form=form)


@app.before_first_request
def initDB():
    db.create_all()

    #    addGun = gunDay(gunType="Pistooli", gunCaliber="9mm", howMany="50kpl",  gunRange="Osuva Kamppi", visit="16.5.2020")
    #    db.session.add(addGun)

    #    addGun = gunDay(gunType="Pistooli", gunCaliber="9mm", howMany="50kpl", gunRange="Osuva Tähtitorninmäki", visit="23.6.2020")
    #    db.session.add(addGun)

    #    addGun = gunDay(gunType="Revolveri",gunCaliber=".38", howMany="100kpl", gunRange="Joensuu SAR", visit="1.10.2020")
    #    db.session.add(addGun)

    db.session.commit()


@app.route("/<int:id>/edit", methods=["GET", "POST"])
@app.route("/new", methods=["GET", "POST"])
def addNew(id=None):
    addGun = gunDay()
    if id:
        addGun = gunDay.query.get(id)

    form = gunRangeForm(obj=addGun)

    if form.validate_on_submit():
        # addGun = gunDay()
        form.populate_obj(addGun)

        db.session.add(addGun)
        db.session.commit()

        print("Added a new rangeday")
        flash("Added a new rangeday")
        return redirect("/")

    return render_template("new.html", form=form)


@app.route("/<int:id>/delete")
def deleteGun(id):
    addGun = gunDay.query.get_or_404(id)
    db.session.delete(addGun)
    db.session.commit()
    flash("Deleted")
    return redirect("/")


@app.errorhandler(404)
def notFound(e):
    return render_template("404.html")


@app.route("/")
def index():
    addGuns = gunDay.query.all()
    return render_template("index.html", addGuns=addGuns)


if __name__ == "__main__":
    app.run()
