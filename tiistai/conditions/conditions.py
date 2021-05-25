from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    hats = ["shako", "andy visage"]
    return render_template("index.html", hats=hats)

app.run()
