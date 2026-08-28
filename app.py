from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "clinica_secret"

# Paciente de prueba
pacientes = [{
    "folio": "EXP-001",
    "nombre": "Juan Pérez",
    "telefono": "3111234567",
    "nacimiento": "2000-05-12",
    "notas": "Paciente de prueba"
}]

citas = []
historial = []

clinicas = ["Clínica Integral", "Prótesis Total", "Prótesis Removible"]
horarios = {
    "Clínica Integral": {
        "Lunes": "4pm - 6pm",
        "Martes": "4pm - 6pm",
        "Miércoles": "10am - 12pm",
        "Jueves": "4pm - 6pm",
        "Viernes": "10am - 12pm"
    },
    "Prótesis Total": {
        "Miércoles": "4pm - 6pm",
        "Viernes": "12pm - 2pm"
    },
    "Prótesis Removible": {
        "Lunes": "12pm - 2pm",
        "Miércoles": "12pm - 2pm"
    }
}

@app.route("/agenda")
def agenda():
    # Ordenar citas por fecha (más próxima primero)
    citas_ordenadas = sorted(citas, key=lambda x: x["fecha"])
    return render_template("agenda.html", citas=citas_ordenadas)

@app.route("/historial")
def historial_consultas():
    return render_template("historial.html", historial=historial)

@app.route("/pacientes")
def lista_pacientes():
    return render_template("pacientes.html", pacientes=pacientes)

@app.route("/nuevo_paciente", methods=["GET", "POST"])
def nuevo_paciente():
    if request.method == "POST":
        folio_num = request.form["folio"]
        folio = f"EXP-{folio_num}"
        nombre = request.form["nombre"]
        telefono = request.form["telefono"]
        nacimiento = request.form["nacimiento"]
        notas = request.form["notas"]
        pacientes.append({
            "folio": folio,
            "nombre": nombre,
            "telefono": telefono,
            "nacimiento": nacimiento,
            "notas": notas
        })
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
        fecha = request.form["fecha"]
        horario = request.form["horario"]
        atendido_por = request.form["atendido_por"]
        notas = request.form.get("notas", "")

        # Validar día de la semana
        dia_semana = datetime.strptime(fecha, "%Y-%m-%d").strftime("%A")
        dias_es = {
            "Monday": "Lunes",
            "Tuesday": "Martes",
            "Wednesday": "Miércoles",
            "Thursday": "Jueves",
            "Friday": "Viernes",
            "Saturday": "Sábado",
            "Sunday": "Domingo"
        }
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

        # 🔹 Redirige a Agenda en lugar de Inicio
        return redirect(url_for("agenda"))

    return render_template("nueva_cita.html", clinicas=clinicas, horarios=horarios, pacientes=[p["nombre"] for p in pacientes])

@app.route("/actualizar_cita/<int:index>/<accion>")
def actualizar_cita(index, accion):
    if 0 <= index < len(citas):
        cita = citas[index]
        if accion == "eliminar":
            citas.pop(index)
        elif accion == "completado":
            historial.append(cita)
            citas.pop(index)
        elif accion == "reprogramar":
            # Borra la cita y redirige a nueva cita
            citas.pop(index)
            return redirect(url_for("nueva_cita"))
    return redirect(url_for("agenda"))
