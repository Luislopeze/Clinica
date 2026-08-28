from flask import Flask, render_template
from datetime import date

app = Flask(__name__)

@app.route("/")
def index():
    hoy = date.today().strftime("%Y-%m-%d")
    odontologos = [
        {"nombre": "Luis", "citas": 0},
        {"nombre": "Angie", "citas": 0}
    ]
    citas = []
    return render_template("index.html", hoy=hoy, odontologos=odontologos, citas=citas)
