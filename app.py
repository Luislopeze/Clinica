from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "clinica_secret"

# Datos en memoria
pacientes = []
citas = []
historial = []

# Clínicas disponibles
clinicas = ["Integral", "Prótesis Total", "Prótesis Removible"]

# Horarios por clínica
horarios = {
    "Integral": {
        "Lunes": "10:00",
        "Martes": "10:00",
        "Miércoles": "10:00",
        "Jueves": "10:00",
        "Viernes": "10:00"
    },
    "Prótesis Total": {
        "Lunes": "12:00",
        "Martes": "12:00",
        "Miércoles": "12:00",
        "Jueves": "12:00",
        "Viernes": "12:00"
    },
    "Prótesis Removible": {
        "Lunes": "16:00",
        "Martes": "16:00",
        "Miércoles": "16:00",
        "Jueves": "16:00",
        "Viernes": "16:00"
    }
}

# Traducción días
dias_es = {
    "Monday": "Lunes",
    "Tuesday": "Martes",
    "Wednesday": "Miércoles",
    "Thursday": "Jueves",
    "Friday": "Viernes",
    "Saturday": "Sábado",
    "Sunday": "Domingo"
}

# Dashboard inicial
@app.route("/")
def dashboard():
    return render_template("dashboard.html", pacientes=pacientes, citas=citas, historial=historial, clinicas=clinicas)

# Agenda
@app.route("/agenda")
def agenda():
    return render_template("agenda.html", citas=citas)

# Historial
@app.route("/historial")
def historial_view():
    return render_template("historial.html", historial=historial)

# Pacientes
@app.route("/pacientes")
def pacientes_view():
    return render_template("pacientes.html", pacientes=pacientes)

@app.route("/nuevo_paciente", methods=["GET", "POST"])
def nuevo_paciente():
    if request.method == "POST":
        folio = "EXP-" + request.form["folio"]
        nombre = request.form["nombre"]
        telefono = request.form["telefono"]
        nacimiento = request.form["nacimiento"]
        notas = request.form.get("notas", "")
        pacientes.append({
            "folio": folio,
            "nombre": nombre,
            "telefono": telefono,
            "nacimiento": nacimiento,
            "notas": notas
        })
        return redirect(url_for("pacientes_view"))
    return render_template("nuevo_paciente.html")

@app.route("/eliminar_paciente/<int:index>")
def eliminar_paciente(index):
    if 0 <= index < len(pacientes):
        pacientes.pop(index)
    return redirect(url_for("pacientes_view"))

# Nueva cita
@app.route("/nueva_cita", methods=["GET", "POST"])
def nueva_cita():
    if request.method == "POST":
        paciente = request.form["paciente"]
        clinica = request.form["clinica"]
        fecha = request.form["fecha"]
        horario = request.form["horario"]
        atendido_por = request.form["atendido_por"]
        notas = request.form.get("notas", "")

        # Validar día de la semana
        dia_semana = datetime.strptime(fecha, "%Y-%m-%d").strftime("%A")
        dia_es = dias_es[dia_semana]

        if dia_es not in horarios[clinica]:
            flash(f"⚠️ La clínica {clinica} no atiende el día {dia_es}.")
            return redirect(url_for("nueva_cita"))

        # Validar cruce de citas
        for c in citas:
            if c["fecha"] == fecha and c["clinica"] == clinica and c["horario"] == horario:
                flash("⚠️ Ya existe una cita en ese horario y clínica.")
                return redirect(url_for("nueva_cita"))

        citas.append({
            "paciente": paciente,
            "clinica": clinica,
            "fecha": fecha,
            "horario": horario,
            "atendido_por": atendido_por,
            "notas": notas
        })
        return redirect(url_for("agenda"))

    return render_template("nueva_cita.html", clinicas=clinicas, horarios=horarios, pacientes=[p["nombre"] for p in pacientes])

# Actualizar cita
@app.route("/actualizar_cita/<int:index>/<accion>")
def actualizar_cita(index, accion):
    if 0 <= index < len(citas):
        cita = citas[index]
        if accion == "completado":
            historial.append(cita)
            citas.pop(index)
        elif accion == "eliminar":
            citas.pop(index)
        elif accion == "reprogramar":
            flash("🔄 Reprograma la cita seleccionando nueva fecha y horario.")
            return redirect(url_for("nueva_cita"))
    return redirect(url_for("agenda"))

if __name__ == "__main__":
    app.run(debug=True)
