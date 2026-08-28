from flask import Flask, render_template, request, redirect, url_for
from datetime import date

app = Flask(__name__)

# Datos simulados
pacientes = []
citas = []

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

@app.route("/")
def inicio():
    hoy = date.today().strftime("%Y-%m-%d")
    odontologos = [
        {"nombre": "Luis", "citas": sum(1 for c in citas if "Luis" in c.get("clinica", ""))},
        {"nombre": "Angie", "citas": sum(1 for c in citas if "Angie" in c.get("clinica", ""))}
    ]
    citas_hoy = [c for c in citas if hoy in c.get("horario", "")]
    return render_template("inicio.html", hoy=hoy, odontologos=odontologos, citas_hoy=citas_hoy)

@app.route("/agenda")
def agenda():
    return render_template("agenda.html", citas=citas)

@app.route("/pacientes")
def lista_pacientes():
    return render_template("pacientes.html", pacientes=pacientes)

@app.route("/nuevo_paciente", methods=["GET", "POST"])
def nuevo_paciente():
    if request.method == "POST":
        nombre = request.form["nombre"]
        telefono = request.form["telefono"]
        nacimiento = request.form["nacimiento"]
        notas = request.form["notas"]
        pacientes.append({"nombre": nombre, "telefono": telefono, "nacimiento": nacimiento, "notas": notas})
        return redirect(url_for("lista_pacientes"))
    return render_template("nuevo_paciente.html")

@app.route("/eliminar_paciente/<int:index>")
def eliminar_paciente(index):
    if 0 <= index < len(pacientes):
        pacientes.pop(index)
    return redirect(url_for("lista_pacientes"))

@app.route("/nueva_cita", methods=["GET", "POST"])
def nueva_cita():
    if request.method == "POST":
        paciente = request.form["paciente"]
        clinica = request.form["clinica"]
        horario = request.form["horario"]
        notas = request.form.get("notas", "")
        citas.append({"paciente": paciente, "clinica": clinica, "horario": horario, "notas": notas})
        return redirect(url_for("inicio"))
    return render_template("nueva_cita.html", clinicas=clinicas, horarios=horarios, pacientes=[p["nombre"] for p in pacientes])
