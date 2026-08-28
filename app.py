import os
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime, date
from modules import db, Paciente, Alumno, Cita   # asegúrate que modules.py esté en la raíz

app = Flask(__name__)

# Configuración de la base de datos desde variables de entorno en Render
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "clinica_secret")

# Inicializar SQLAlchemy
db.init_app(app)

# -----------------------------
# RUTAS
# -----------------------------
@app.route("/")
def inicio():
    hoy = date.today().strftime("%Y-%m-%d")
    odontologos = [
        {"nombre": "Luis", "citas": Cita.query.filter_by(atendido_por="Luis", fecha=date.today()).count()},
        {"nombre": "Angie", "citas": Cita.query.filter_by(atendido_por="Angie", fecha=date.today()).count()}
    ]
    citas_hoy = Cita.query.filter_by(fecha=date.today()).all()
    return render_template("inicio.html", hoy=hoy, odontologos=odontologos, citas_hoy=citas_hoy)

@app.route("/dashboard")
def dashboard():
    pacientes = Paciente.query.all()
    citas = Cita.query.all()
    clinicas = list(set([c.clinica for c in citas]))
    historial = []  # luego podemos implementar tabla Historial
    return render_template("dashboard.html", pacientes=pacientes, citas=citas, historial=historial, clinicas=clinicas)

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
        nuevo = Paciente(folio=folio, nombre=nombre, telefono=telefono,
                         fecha_nacimiento=nacimiento, notas=notas)
        db.session.add(nuevo)
        db.session.commit()
        flash("Paciente registrado correctamente")
        return redirect(url_for("pacientes_view"))
    return render_template("nuevo_paciente.html")

@app.route("/agenda")
def agenda_view():
    citas = Cita.query.all()
    return render_template("agenda.html", citas=citas)

@app.route("/nueva_cita", methods=["GET", "POST"])
def nueva_cita():
    pacientes = Paciente.query.all()
    if request.method == "POST":
        paciente_id = request.form["paciente"]
        clinica = request.form["clinica"]
        horario = request.form["horario"]
        fecha = datetime.strptime(request.form["fecha"], "%Y-%m-%d").date()
        atendido_por = request.form["atendido_por"]
        notas = request.form.get("notas", "")
        nueva = Cita(dia=fecha.strftime("%A"),
                     hora_inicio=horario.split("-")[0],
                     hora_fin=horario.split("-")[1],
                     clinica=clinica,
                     paciente_id=paciente_id,
                     alumno_id=None,
                     notas=notas)
        db.session.add(nueva)
        db.session.commit()
        flash("Cita registrada correctamente")
        return redirect(url_for("agenda_view"))
    return render_template("nueva_cita.html", pacientes=pacientes)

@app.route("/historial")
def historial_view():
    historial = []  # más adelante podemos mover citas completadas aquí
    return render_template("historial.html", historial=historial)

# -----------------------------
# EJECUCIÓN
# -----------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
