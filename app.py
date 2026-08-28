from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = "clinica_secret"

# 🔧 Conexión a tu base de datos PostgreSQL en Render
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://elsince:KMKUCB87zO04U3RjqNyz8sSdOxoR70xH@dpg-da8b3q0ae00c73cd5sog-a/clinica_db_ov6b"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# 🔧 Modelos (tablas)
class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    folio = db.Column(db.String(50), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    nacimiento = db.Column(db.Date)
    notas = db.Column(db.Text)

class Cita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey("paciente.id"), nullable=False)
    clinica = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    horario = db.Column(db.String(20), nullable=False)
    atendido_por = db.Column(db.String(100))
    notas = db.Column(db.Text)

class Historial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey("paciente.id"), nullable=False)
    clinica = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    horario = db.Column(db.String(20), nullable=False)
    atendido_por = db.Column(db.String(100))
    notas = db.Column(db.Text)

# 🔧 Crear tablas al iniciar la app (Flask 3.0+)
with app.app_context():
    db.create_all()

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
    pacientes = Paciente.query.all()
    citas = Cita.query.all()
    historial = Historial.query.all()
    clinicas = ["Clínica Integral", "Prótesis Total", "Prótesis Removible"]
    return render_template("dashboard.html", pacientes=pacientes, citas=citas, historial=historial, clinicas=clinicas)

# Pacientes
@app.route("/pacientes")
def pacientes_view():
    pacientes = Paciente.query.all()
    return render_template("pacientes.html", pacientes=pacientes)

@app.route("/nuevo_paciente", methods=["GET", "POST"])
def nuevo_paciente():
    if request.method == "POST":
        folio = "EXP-" + request.form["folio"]
        nombre = request.form["nombre"]
        telefono = request.form["telefono"]
        nacimiento = datetime.strptime(request.form["nacimiento"], "%Y-%m-%d").date()
        notas = request.form.get("notas", "")

        nuevo = Paciente(folio=folio, nombre=nombre, telefono=telefono, nacimiento=nacimiento, notas=notas)
        db.session.add(nuevo)
        db.session.commit()
        return redirect(url_for("pacientes_view"))
    return render_template("nuevo_paciente.html")

@app.route("/eliminar_paciente/<int:id>")
def eliminar_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    db.session.delete(paciente)
    db.session.commit()
    return redirect(url_for("pacientes_view"))

# Agenda
@app.route("/agenda")
def agenda():
    citas = Cita.query.all()
    return render_template("agenda.html", citas=citas)

# Nueva cita
@app.route("/nueva_cita", methods=["GET", "POST"])
def nueva_cita():
    pacientes = Paciente.query.all()
    clinicas = ["Clínica Integral", "Prótesis Total", "Prótesis Removible"]
    doctores = ["Luis", "Angie"]  # 👈 opciones fijas

    if request.method == "POST":
        paciente_id = request.form["paciente"]
        clinica = request.form["clinica"]
        fecha = datetime.strptime(request.form["fecha"], "%Y-%m-%d").date()
        horario = request.form["horario"]
        atendido_por = request.form["atendido_por"]
        notas = request.form.get("notas", "")

        nueva = Cita(
            paciente_id=paciente_id,
            clinica=clinica,
            fecha=fecha,
            horario=horario,
            atendido_por=atendido_por,
            notas=notas
        )
        db.session.add(nueva)
        db.session.commit()
        return redirect(url_for("agenda"))

    return render_template("nueva_cita.html", pacientes=pacientes, clinicas=clinicas, doctores=doctores)

# Historial
@app.route("/historial")
def historial_view():
    historial = Historial.query.all()
    return render_template("historial.html", historial=historial)

@app.route("/actualizar_cita/<int:id>/<accion>")
def actualizar_cita(id, accion):
    cita = Cita.query.get_or_404(id)
    if accion == "completado":
        historial = Historial(
            paciente_id=cita.paciente_id,
            clinica=cita.clinica,
            fecha=cita.fecha,
            horario=cita.horario,
            atendido_por=cita.atendido_por,
            notas=cita.notas
        )
        db.session.add(historial)
        db.session.delete(cita)
        db.session.commit()
    elif accion == "eliminar":
        db.session.delete(cita)
        db.session.commit()
    return redirect(url_for("agenda"))

if __name__ == "__main__":
    app.run(debug=True)
