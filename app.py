from flask import Flask, render_template, request
from datetime import date

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("agenda.html", hoy=date.today().strftime("%d/%m/%Y"))

@app.route("/pacientes")
def pacientes():
    pacientes = [
        {"nombre": "Juan Pérez", "telefono": "3111234567", "nacimiento": "2000-05-12", "notas": "Valoración inicial"},
        {"nombre": "María López", "telefono": "3119876543", "nacimiento": "1998-09-21", "notas": "Endodoncia"}
    ]
    return render_template("pacientes.html", pacientes=pacientes)

@app.route("/nueva_cita")
def nueva_cita():
    alumnos = ["Luis", "Angie"]
    pacientes = ["Juan Pérez", "María López"]
    return render_template("nueva_cita.html", alumnos=alumnos, pacientes=pacientes)
