from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Lista de pacientes (simulada en memoria)
pacientes = []

# Lista de citas
citas = []

# Clínicas y horarios
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
def index():
    return redirect(url_for("agenda"))

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
        return redirect(url_for("agenda"))
    return render_template("nueva_cita.html", clinicas=clinicas, horarios=horarios, pacientes=[p["nombre"] for p in pacientes])
