from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Datos simulados
clinicas = ["Clínica Integral", "Prótesis Total", "Prótesis Removible"]

horarios = {
    "Clínica Integral": [
        "Lunes 4pm - 6pm",
        "Martes 4pm - 6pm",
        "Miércoles 10am - 12pm",
        "Jueves 4pm - 6pm",
        "Viernes 10am - 12pm"
    ],
    "Prótesis Total": [
        "Miércoles 4pm - 6pm",
        "Viernes 12pm - 2pm"
    ],
    "Prótesis Removible": [
        "Lunes 12pm - 2pm",
        "Miércoles 12pm - 2pm"
    ]
}

pacientes = ["Juan Pérez", "María López", "Carlos Ruiz"]

# Lista de citas guardadas
citas = []

@app.route("/")
def index():
    return redirect(url_for("agenda"))

@app.route("/agenda")
def agenda():
    return render_template("agenda.html", citas=citas)

@app.route("/pacientes")
def lista_pacientes():
    return render_template("pacientes.html", pacientes=pacientes)

@app.route("/nueva_cita", methods=["GET", "POST"])
def nueva_cita():
    if request.method == "POST":
        paciente = request.form["paciente"]
        clinica = request.form["clinica"]
        horario = request.form["horario"]
        notas = request.form.get("notas", "")
        citas.append({"paciente": paciente, "clinica": clinica, "horario": horario, "notas": notas})
        return redirect(url_for("agenda"))
    return render_template("nueva_cita.html", clinicas=clinicas, horarios=horarios, pacientes=pacientes)
