from flask import Flask, render_template
import sys

app = Flask(__name__)

@app.route("/")
def index():
    hats = ["shako", "andy visage", "ik helm"]
    return render_template("base.html", hats=hats)

app.run()
