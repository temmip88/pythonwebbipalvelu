from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

class Sammakot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

@app.before_first_request
def initDB():
    db.create_all()

    db.session.add(Sammakot(name = "Apustaja"))
    db.session.add(Sammakot(name = "Lättä"))
    db.session.add(Sammakot(name = "Pepe"))

    db.session.commit()



@app.route("/")
def index():
    sammakot = Sammakot.query.all()
    return render_template("index.html", sammakot=sammakot)

if __name__=="__main__":
    app.run()
