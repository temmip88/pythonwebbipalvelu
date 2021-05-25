from flask import Flask, render_template
import sys

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("base2.html")

@app.route("/foo")
def foo():
    return render_template("foo.html")

app.run()
