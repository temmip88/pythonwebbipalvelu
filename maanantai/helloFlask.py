from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello vaan Teemu!"

app.run(debug=True) # testiä vain
