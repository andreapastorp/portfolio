from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/projects/gerrard-street")
def gerrard_street():
    return render_template('projects/gerrard-street.html')

@app.route("/projects/twill-by-maersk")
def twill():
    return render_template('projects/twill-by-maersk.html')

@app.route("/projects/connecting-roommates")
def connecting_roommates():
    return render_template('projects/connecting-roommates.html')

@app.route("/projects/interbank")
def interbank():
    return render_template('projects/interbank.html')
